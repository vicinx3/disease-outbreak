import React from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import { country_conversion } from '../../../static';

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this._id = 'chart-' + this.guid();
        this.filters = [];

        this.createSeries = this.createSeries.bind(this);
    }

    guid() {
        const r4 = () => {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return r4() + r4() + r4() + r4()
    }

    componentDidMount() {
        const chart = am4core.create(this._id, am4charts.XYChart);
        chart.logo.__disabled = true;
        chart.paddingRight = 20;
        chart.background.fill = '#FFFFFF';
        chart.plotContainer.background.stroke = "#001011";

        const valueXAxis = chart.xAxes.push(new am4charts.ValueAxis());
        valueXAxis.dataFields.data = 'total';
        valueXAxis.renderer.labels.template.fill = am4core.color("#001011");
        valueXAxis.renderer.grid.template.stroke = am4core.color("#001011");
        valueXAxis.logarithmic = true;
        valueXAxis.title.text = 'Total Confirmed Cases'
        valueXAxis.title.fontSize = 18;

        const valueYAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueYAxis.min = 5;
        valueYAxis.dataFields.data = 'new';
        valueYAxis.renderer.labels.template.fill = am4core.color("#001011");
        valueYAxis.renderer.grid.template.stroke = am4core.color("#001011");
        valueYAxis.logarithmic = true;
        valueYAxis.title.text = 'New Confirmed Cases (averaged)'
        valueYAxis.title.fontSize = 18;

        const legend = new am4charts.Legend();
        chart.legend = legend; 
        legend.labels.template.fill = am4core.color("#001011");
        
        const cursor = new am4charts.XYCursor();
        chart.cursor = cursor; 

        this.chart = chart; 
    }

    
    componentWillUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    }

    createSeries(key, data, name="series") {
        const series = new am4charts.LineSeries();
        series.dataFields.valueX = "total";
        series.dataFields.valueY = "new";
        series.data = data;
        series.name = name;
        series.id = key.country;
        // series.tensionX = 0.85;
        // series.tensionY = 0.85;
        series.dataItems.template.locations.dateX = 0;

        const bullet = series.bullets.push(new am4charts.Bullet());
        const dot = bullet.createChild(am4core.Circle);
        bullet.tooltipText = "[bold]" + name + "[/]\nNew: {valueY}\nTotal: {valueX}";
        dot.width = 5;
        dot.height = 5;
        dot.horizontalCenter = "middle";
        dot.verticalCenter = "middle";
        
        this.chart.series.push(series);
        this.filters.push(key);
    }

    componentDidUpdate(prevProps) {
        // Delete
        const removeIndices = []
        this.filters.forEach((seriesFilter, index) => {
            let found = false;
            for (const filter of this.props.filters) {
                if (this.props.equal(filter, seriesFilter)) {
                    found = true; 
                    break;
                }
            }
            if (!found) removeIndices.push(index);
        });
        removeIndices.reverse();
        for (const i of removeIndices) {
            this.chart.series.removeIndex(i).dispose();
            this.filters.splice(i, 1);
        }

        // Add 
        const newFilters = [];
        for (const filter of this.props.filters) {
            let found = false; 
            for (const seriesFilter of this.filters) {
                if (this.props.equal(filter, seriesFilter)) {
                    found = true;
                    break;
                }
            }
            if (!found) newFilters.push(filter);
        }
        
        for (const filter of newFilters) {
            console.log(filter);
            this.createSeries(filter, filter.data, country_conversion[filter.country]);
        }
    }

    render() {
        return (
            <div id={this._id} style={{height: '650px', width: '80%', overflow: 'hidden'}}/>         
        )
    }
}
