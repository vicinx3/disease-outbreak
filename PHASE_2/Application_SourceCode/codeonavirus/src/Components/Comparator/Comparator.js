import React from 'react';
import './Comparator.css';
import FilterSearch from './FilterSearch';
import FilterEntry from './FilterEntry';
import LineChart from './LineChart';
import { fetchComparatorActual, fetchComparatorPercentage } from '../../API/main';
import { disease_conversion, country_conversion } from '../../static';
import NavBar from "../Navbar";

export default class Comparator extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            filters: [{
                country: "all countries",
                disease: "all diseases",
                source: 'WHO',
                loaded: false,
            }],
            max: 5
        };
    }

    filterEqual = (a, b) => a.country === b.country && a.disease === b.disease && a.source === b.source;

    findFilter = (country, disease, source, filters=this.state.filters) => {
        for (let i = 0; i < filters.length; i++) {
            if (this.filterEqual(filters[i], {country: country, disease: disease, source: source})) {
                return i; 
            }
        }
        return -1;
    }

    addDisabled = () => this.state.max && this.state.filters.length >= this.state.max;

    handleAddFilter = (country, disease, source) => {
        if (this.addDisabled()) return;
        if (this.findFilter(country, disease, source) >= 0) return;
        this.setState({
            filters: [...this.state.filters, {
                country: country, 
                disease: disease,
                source: source,
                loaded: false
            }]
        });
    }

    handleDeleteFilter = (country, disease, source) => {
        const index = this.findFilter(country, disease, source);
        if (index >= 0) {
            this.setState({
                filter: this.state.filters.splice(index, 1)
            });
        }
    }

    process = (fetcher) => {
        return (filters, createSeries) => {
            for (const filter of filters) {
                const country = filter.country; 
                const disease = filter.disease;
                const source = filter.source;

                const name = `${country_conversion[country]}\n${disease_conversion[disease]}\n${source}`;
                const bulletTooltipText = "{dateX.formatDate('yyyy')}: [bold]{valueY}[/]";
    
                fetcher(country, disease, source)
                    .then(r => {
                        createSeries(filter, r, name, bulletTooltipText);
                        
                        let filtersCopy = JSON.parse(JSON.stringify(this.state.filters));
                        const i = this.findFilter(country, disease, source, filtersCopy);
                        if (i >= 0) filtersCopy[i].loaded = true; 
                        this.setState({filters: filtersCopy});
                    });
            }
        }
    }

    render() {
        return (
            <div>
                <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"></link>
                <NavBar ac = {1}/>
                <h1 id = "comparator">Global Disease Comparator</h1>
                <div id = "comparison">
                    <div id = "cCont">
                        <FilterSearch onAdd={this.handleAddFilter} disabled={this.addDisabled()}/>
                        <div>
                            {this.state.filters.map((filter) => {
                                return (
                                <div style={{width: '97%', marginBottom: '15px'}}>
                                    <FilterEntry 
                                        key={filter.country + filter.disease}
                                        country={filter.country} 
                                        disease={filter.disease} 
                                        source={filter.source}
                                        onDel={this.handleDeleteFilter}
                                        loaded={filter.loaded}
                                        />
                                </div>);
                            })}
                        </div>
                    </div>
                </div>
                    <div id = "charts"> 
                        <h3 className = "cTitle">Number of Reports over Years</h3>           
                        <LineChart className = "chart"
                            data={this.state.filters}
                            equal={this.filterEqual}
                            process={this.process(fetchComparatorActual)}
                            xAxisTitle='Year'
                            yAxisTitle='Number of Reports'
                        />
                        <h3 className = "cTitle">Percentage of Total Reports from All Sources</h3>
                        <LineChart className = "chart"
                            data={this.state.filters}
                            equal={this.filterEqual}
                            process={this.process(fetchComparatorPercentage)}
                            maxValue={100}
                            xAxisTitle='Year'
                            yAxisTitle='Percentage (%)'
                        />
                </div>  
            </div>
        );
    }
}