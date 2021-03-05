import React from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import { fetchLineChart } from '../../API/covid';

const categories = ['confirmed', 'recovered', 'deaths'];

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this._id = 'chart-' + this.guid();
        this.series = {};
        this.dateAxis = null;
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
        dateAxis.title.text = 'Date';
        dateAxis.title.fontSize = 18;
        dateAxis.renderer.labels.template.fontSize = 14;
        this.dateAxis = dateAxis;

        const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.min = 0;
        if ('maxValue' in this.props) valueAxis.max = this.props.maxValue; 
        valueAxis.renderer.labels.template.fill = am4core.color("#001011");
        valueAxis.renderer.grid.template.stroke = am4core.color("#001011");
        //valueAxis.renderer.opposite = true; 
        valueAxis.cursorTooltipEnabled= false; 
        valueAxis.renderer.labels.template.fontSize = 14;
        valueAxis.title.text = 'Number of Cases';
        valueAxis.fontSize = 18;

        const legend = new am4charts.Legend();
        chart.legend = legend; 
        legend.labels.template.fill = am4core.color("#001011");
        
        const cursor = new am4charts.XYCursor();
        chart.cursor = cursor; 
        cursor.lineY.disabled = true; 

        // ERIC, please change the colours to be nicer 
        chart.colors.list = [
            am4core.color('#1481BA'),
            am4core.color('#0A8754'),
            am4core.color('#2E2D4D')
        ];
        for (const category of categories) {
            const name = category.charAt(0).toUpperCase() + category.slice(1);
            this.series[category] = chart.series.push(this.createSeries(category, name));
        }

        this.chart = chart; 
        this.componentDidUpdate();
    }

    
    componentWillUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
    }

    createSeries(id, name="series") {
        const series = new am4charts.LineSeries();
        series.dataFields.dateX = "date";
        series.dataFields.valueY = "value";
        series.id= id;
        series.name = name;
        // series.tensionX = 0.85;
        // series.tensionY = 0.85;
        series.dataItems.template.locations.dateX = 0;

        const bullet = series.bullets.push(new am4charts.Bullet());
        const dot = bullet.createChild(am4core.Circle);
        bullet.tooltipText = `[bold]${name}[/]: {valueY}`;
        dot.width = 4;
        dot.height = 4;
        dot.horizontalCenter = "middle";
        dot.verticalCenter = "middle";
        
        return series;
    }

    updateCursor(date) {
        const currentDate = addDays(this.props.epoch, date);
        const point = this.dateAxis.dateToPoint(currentDate);
        this.chart.cursor.triggerMove(point, 'soft');
    }

    updateShow(category) {
        for (const cat of categories) {
            if (cat === category) {
                this.series[cat].show();
            } else {
                this.series[cat].hide();
            }
        }
    }

    componentDidUpdate(prevProps) {
        const params = this.props.params 

        // Switch between 'total' and 'daily'
        if (!prevProps || params.daily !== prevProps.params.daily) {
            fetchLineChart(params).then(result => {
                for (const category of categories) {
                    const data = result[category].map(point => {
                        return {
                            date: new Date(point.date),
                            value: point.value
                        }
                    });
                    this.series[category].data = data;   
                }
                if (!prevProps) this.updateShow(params.category);
            });
        }

        // Date changed => Date cursor moves
        if (prevProps && params.date !== prevProps.params.date) {
            this.updateCursor(params.date);
        }

        // Show correct category when category is selected
        if (!prevProps || params.category !== prevProps.params.category) {
            this.updateShow(params.category);
        }
    }

    render() {
        return (
            <div id={this._id} style={{height: '500px', width: '59%', display: 'inline-block'}}/>         
        )
    }
}

function addDays(date, days) { 
    const copy = new Date(Number(date))
    copy.setDate(date.getDate() + days)
    return copy 
}