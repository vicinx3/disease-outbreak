import React from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import "./PieChart.css";

export default class PieChart extends React.Component {
    constructor(props) {
        super(props);
        this._id = 'chart-' + this.guid();
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
        const chart = am4core.create(this._id, am4charts.PieChart);
        chart.logo.__disabled = true;
        chart.background.fill = '#FFFFFF';

        const series = chart.series.push(new am4charts.PieSeries());
        series.dataFields.category = "category";
        series.dataFields.value = "value";

        series.ticks.template.stroke = am4core.color("#001011");
        series.ticks.template.strokeWidth = 2;
        series.ticks.template.strokeOpacity = 0.5;
        
        series.labels.template.fill = am4core.color("#001011");
        series.labels.template.radius = am4core.percent(15); // Puts label further away
        
        // Colour of lines that split sectors + circumference 
        series.slices.template.stroke = am4core.color("#111111"); 
        series.slices.template.strokeWidth = 1;
        series.slices.template.strokeOpacity = 1;

        // Starting animation
        series.hiddenState.properties.opacity = 1; 
        series.hiddenState.properties.endAngle = -90;
        series.hiddenState.properties.startAngle = -90;

        const label = chart.createChild(am4core.Label);
        label.text = "Note: 'Other' refers to any unlisted disease, 'Remaining' refers to a collation of diseases beyond the top 10."
        label.align = 'center';
        label.y = am4core.percent(96);

        this.chart = chart; 
        this.props.getData(this.setData)
    }

    
    componentWillUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    }

    componentDidUpdate() {
        this.props.getData(this.setData)
    }

    setData = (data) => {
        this.chart.data = data
    }

    render() {
        return (
            <div id = "pieChart">
            <h1 id = "pHeading">Top 10 Most Reported Diseases</h1>
                <div id={this._id} style={{height: '30vmax'}}/>   
            </div>      
        )
    }
}