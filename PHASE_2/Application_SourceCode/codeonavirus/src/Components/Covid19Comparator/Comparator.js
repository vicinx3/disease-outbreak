import React from 'react'
import FilterAdd from './FilterAdd';
import FilterEntry from './FilterEntry';
import Selector from '../Selector';
import StandardLineChart from './StandardLineChart';
import TrajectoryLineChart from './TrajectoryLineChart';
import { fetchComparator } from '../../API/covid';
import Navbar from "../Navbar";
import "./Comparator.css";

const tabsCategory = [{label: 'Confirmed', value: 'confirmed'}, 
            {label: 'Recovered', value: 'recovered'}, 
            {label: 'Deaths', value: 'deaths'}];

export default class Comparator extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            filters: [], 
            category: 'confirmed'
        }
        this.max = 5;
        this.epoch = new Date(2020, 0, 22);
    }

    filterEqual = (a, b) => a.country === b.country;

    filterFind = (filter, filters=this.state.filters) => {
        for (let i = 0; i < filters.length; i++) {
            if (this.filterEqual(filters[i], filter)) {
                return i;
            }
        }
        return -1;
    }

    addDisabled = () => this.state.filters.length >= this.max;

    handleAddFilter = (country) => { 
        if (this.addDisabled()) return; 
        if (this.filterFind({country: country}) >= 0) return; 
        this.setState({
            filters: [...this.state.filters, {
                country: country,
                offset: 0, 
                loaded: false
            }]
        })

        // Fetch data 
        fetchComparator({country: country}).then(result => {
            const filtersCopy = JSON.parse(JSON.stringify(this.state.filters));
            const i = this.filterFind({country: country});
            if (i >= 0) {
                filtersCopy[i].loaded = true; 
                filtersCopy[i].data = result;
                this.setState({filters: filtersCopy});
            }
        })
    }

    handleChange = (state) => {
        return (value) => {
            this.setState({[state]: value});
        }
    }

    handleChangeOffset = (country, offset) => {
        const index = this.filterFind({country: country});
        if (index >= 0) {
            const filtersCopy = JSON.parse(JSON.stringify(this.state.filters));
            filtersCopy[index].offset = offset
            this.setState({filters: filtersCopy});
        }
    }

    handleDeleteFilter = (country) => {
        const index = this.filterFind({country: country});
        if (index >= 0) {
            this.setState({filter: this.state.filters.splice(index, 1)});
        }
    }

    componentDidMount = () => {
        this.handleAddFilter('all countries');
    }

    formatFilters = () => {
        const filters = this.state.filters;
        const standard = [];
        const trajectory = [];
        for (let i = 0; i < filters.length; i++) {
            if (!filters[i].loaded) continue;
            
            const country = filters[i].country
            const offset = filters[i].offset;
            standard.push({country: country, offset: offset});
            for (const category of ['confirmed', 'recovered', 'deaths']) {
                const dataSet = filters[i].data.standard[category]; 
                standard[standard.length - 1][category] = [];
                for (let j = 0; j < dataSet.length; j++) {
                    standard[standard.length - 1][category].push({
                        date: addDays(this.epoch, dataSet[j].date + offset),
                        value: dataSet[j].value
                    });
                }
            }

            trajectory.push({country: country, data: filters[i].data.trajectory});
        }
        return {standard: standard, trajectory: trajectory};
    }

    render() {
        const formattedFilters = this.formatFilters();
        return (
            <div>
                <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"></link>
                <Navbar ac = {4}/>
                <div>
                    <div id = "cardC">
                        <FilterAdd onAdd={this.handleAddFilter} disabled={this.addDisabled()}/>
                        {this.state.filters.map(filter => (
                            <div className = "kCard">
                            <FilterEntry
                                key={filter.country}
                                country={filter.country}
                                offset={filter.offset}
                                onDel={this.handleDeleteFilter}
                                onChangeOffset={this.handleChangeOffset}
                            />
                            </div>
                        ))}
                    </div>
                    <h1 id = "cvHeader">COVID-19 Comparator</h1>
                    <h3 className='cTitle'>COVID-19 Cases by Country</h3>
                    <Selector tabs={tabsCategory} default='confirmed' onChange={this.handleChange('category')}/>
                    <StandardLineChart
                        filters={formattedFilters.standard}
                        equal={this.filterEqual}
                        category={this.state.category}
                    />
                    <div style={{height: '50px'}}/>
                    <h3 className='cTitle'>Rate of Increase of COVID-19 Cases</h3>
                    <TrajectoryLineChart
                        filters={formattedFilters.trajectory}
                        equal={this.filterEqual}
                    />
                </div>
            </div>
        );
    }
}

function addDays(date, days) { 
    const copy = new Date(Number(date))
    copy.setDate(date.getDate() + days)
    return copy 
}