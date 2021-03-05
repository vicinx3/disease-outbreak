import React from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";

class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this._id = 'chart-' + this.guid();
        this.series = [];

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
        dateAxis.title.text = this.props.xAxisTitle;
        dateAxis.title.fontSize = 18;

        const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.min = 0;
        if ('maxValue' in this.props) valueAxis.max = this.props.maxValue; 
        valueAxis.renderer.labels.template.fill = am4core.color("#001011");
        valueAxis.renderer.grid.template.stroke = am4core.color("#001011");
        valueAxis.title.text = this.props.yAxisTitle;
        valueAxis.title.fontSize = 18;

        const legend = new am4charts.Legend();
        legend.labels.template.fill = am4core.color("#001011");
        chart.legend = legend; 
    
        this.chart = chart; 
        this.componentDidUpdate();
    }

    
    componentWillUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    }

    createSeries(key, data, name="series", bulletTooltipText="Value: [bold]{value}[/]") {
        for (const series of this.series) {
            if (this.props.equal(key, series)) {
                return;
            }
        }
        // New data
        this.series.push(key);

        const series = new am4charts.LineSeries();
        series.dataFields.dateX = "date";
        series.dataFields.valueY = "value";
        series.data = data; 
        series.name = name;
        series.tensionX = 0.85;
        series.tensionY = 0.85;
        series.dataItems.template.locations.dateX = 0;

        const bullet = series.bullets.push(new am4charts.Bullet());
        const dot = bullet.createChild(am4core.Circle);
        bullet.tooltipText = bulletTooltipText;
        dot.width = 10;
        dot.height = 10;
        dot.horizontalCenter = "middle";
        dot.verticalCenter = "middle";

        this.chart.series.push(series);
    }

    componentDidUpdate() {
        // Delete 
        const removeIndices = [];
        this.series.forEach((series, index) => {
            let found = false; 
            for (const data of this.props.data) {
                if (this.props.equal(data, series)) {
                    found = true; 
                }
            }
            if (!found) removeIndices.push(index);
        });
        removeIndices.reverse();
        for (const index of removeIndices) {
            this.chart.series.removeIndex(index).dispose();
            
            this.series.splice(index, 1);
        }

        // Add
        const newData = [];
        for (const data of this.props.data) {
            let found = false; 
            for (const series of this.series) {
                if (this.props.equal(data, series)) {
                    found = true;
                    break;
                }
            }
            if (!found) newData.push(data);
        }

        if ('process' in this.props) {
            this.props.process(newData, this.createSeries); 
        } else {
            for (const data of newData) {
                this.createSeries(data)
            }
        }
    }

    render() {
        return (
            <div id={this._id} style={{height: '600px', width: '72.5%', display: 'inline-block'}}/>         
        )
    }
}

export default LineChart;