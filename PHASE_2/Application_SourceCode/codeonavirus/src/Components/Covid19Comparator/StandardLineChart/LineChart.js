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

        const dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.dataFields.date = 'date';
        dateAxis.renderer.labels.template.fill = am4core.color("#001011");
        dateAxis.renderer.grid.template.stroke = am4core.color("#001011");
        dateAxis.title.text = 'Date'
        dateAxis.title.fontSize = 18;

        const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.min = 0;
        if ('maxValue' in this.props) valueAxis.max = this.props.maxValue; 
        valueAxis.renderer.labels.template.fill = am4core.color("#001011");
        valueAxis.renderer.grid.template.stroke = am4core.color("#001011");
        valueAxis.title.text = 'Cases'
        valueAxis.title.fontSize = 18;

        const legend = new am4charts.Legend();
        chart.legend = legend; 
        legend.labels.template.fill = am4core.color("#001011");
        
        const cursor = new am4charts.XYCursor();
        chart.cursor = cursor; 
        cursor.lineY.disabled = true; 

        this.chart = chart; 
    }

    
    componentWillUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    }

    createSeries(key, data, name="series") {
        const series = new am4charts.LineSeries();
        series.dataFields.dateX = "date";
        series.dataFields.valueY = "value";
        series.data = data;
        series.name = name;
        series.id = key.country;
        // series.tensionX = 0.85;
        // series.tensionY = 0.85;
        series.dataItems.template.locations.dateX = 0;

        const bullet = series.bullets.push(new am4charts.Bullet());
        const dot = bullet.createChild(am4core.Circle);
        bullet.tooltipText = `[bold]${name}[/]: {valueY}`;
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
            this.createSeries(filter, filter[this.props.category], country_conversion[filter.country]);
        }

        // Change in offset 
        for (let i = 0; i < this.filters.length; i++) {
            const seriesFilter = this.filters[i];
            const propFilter = this.props.filters[i];


            if (seriesFilter.country === propFilter.country &&
                seriesFilter.offset !== propFilter.offset) {
                
                seriesFilter.offset = propFilter.offset;
                for (const series of this.chart.series) {
                    if (seriesFilter.country === series.id) {
                        series.data = propFilter[this.props.category];
                    }
                }

                console.log("same country, different offset");
            }
        }


        // Category
        if (!prevProps || this.props.category !== prevProps.category) {
            for (const series of this.chart.series) {
                for (const filter of this.filters) {
                    if (filter.country === series.id) {
                        series.data = filter[this.props.category];
                        break;
                    }
                }
            }
        }
    }

    render() {
        return (
            <div id={this._id} style={{height: '650px', width: '80%', overflow: 'hidden'}}/>         
        )
    }
}
