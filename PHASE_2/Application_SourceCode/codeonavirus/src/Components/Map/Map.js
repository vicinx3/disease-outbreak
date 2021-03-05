import React, { Component } from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_worldLow from "@amcharts/amcharts4-geodata/worldLow";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import getMapData from './GeoData';
import "./Map.css";

am4core.useTheme(am4themes_animated);

class Map extends Component {
    componentDidMount() {
        let chart = am4core.create("mapdiv", am4maps.MapChart);
        chart.geodata = am4geodata_worldLow;
        chart.projection = new am4maps.projections.Miller();
        chart.logo.__disabled = true

        var title = chart.titles.create();
        title.text = this.props.title;
        title.textAlign = "middle";
        title.fontSize = 24;
        title.fontFamily = "'Montserrat', sans-serif";
        title.marginTop = 50;
        title.marginBottom = 50;
        title.fill = am4core.color('#00487C')

        var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
        polygonSeries.exclude = ["AQ"];
        polygonSeries.useGeodata = true;
        polygonSeries.nonScalingStroke = true;
        polygonSeries.strokeWidth = 0.5;
        polygonSeries.calculateVisualCenter = true;
        
        var imageSeries = chart.series.push(new am4maps.MapImageSeries());
        imageSeries.dataFields.value = "value";

        imageSeries.events.on("dataitemsvalidated", function() {
            imageSeries.dataItems.each((dataItem) => {
                var mapImage = dataItem.mapImage;
                var circle = mapImage.children.getIndex(0);
                if (mapImage.dataItem.value === 0) {
                    circle.hide(0)
                } else if (circle.isHidden || circle.isHiding) {
                    circle.show();
                }
            })
        })
        
        var imageTemplate = imageSeries.mapImages.template;
        imageTemplate.nonScaling = true
        
        var circle = imageTemplate.createChild(am4core.Circle);
        circle.fillOpacity = 0.7;
        circle.propertyFields.fill = "color";
        circle.tooltipText = "{name}: [bold]{value}[/]";
        
        imageSeries.heatRules.push({
            "target": circle,
            "property": "radius",
            "min": 4,
            "max": 30,
            "dataField": "value"
        })
        
        imageTemplate.adapter.add("latitude", function(latitude, target) {
            var polygon = polygonSeries.getPolygonById(target.dataItem.dataContext.id);
            if(polygon){
                return polygon.visualLatitude;
            }
            return latitude;
        })
        
        imageTemplate.adapter.add("longitude", function(longitude, target) {
            var polygon = polygonSeries.getPolygonById(target.dataItem.dataContext.id);
            if(polygon){
                return polygon.visualLongitude;
            }
            return longitude;
        })  


        this.map = chart; 
        this.data = imageSeries;
        this.poly = polygonSeries;

        this.props.getData(this.updateMap);
    }
    

    updateMap = (info, colour) => {
        var data = getMapData(this.map, colour);
        for (var elem of data) {
            if (elem.id in info) {
                elem.value = info[elem.id];
            }
        }

        this.data.data = data; 
        this.map.invalidateRawData();
    }

    
    componentDidUpdate() {
        this.props.getData(this.updateMap);
    }

    componentWillUnmount() {
        if (this.map) {
            this.map.dispose();
        }
    }

    render() {
        return (
            <div id = "map">
                <div id="mapdiv" style={{ width: "100%", height: "650px" }}></div>
            </div>
        );
    }
}

export default Map