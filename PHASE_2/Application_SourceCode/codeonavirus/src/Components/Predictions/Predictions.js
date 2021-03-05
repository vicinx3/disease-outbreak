import React from 'react';
import Map from '../Map';
import { fetchMap, fetchTable } from '../../API/prediction';
import NavBar from '../Navbar'
import Slide from '../Slider';
import SearchBar from '../SearchBar';
import { disease_list, disease_conversion, country_list, country_conversion } from '../../static';
import PredictionsTable from '../PredictionsTable';
import "./Predictions.css";

let marksYear = [];
let months = ["January", "February", "March",  "April", "May", "June",  "July", "August", "September", "October", "November", "December"];

for (let i = 0; i < 31; i++) {
    if (i < 9) {
        if ((i % 4) === 0) {
            marksYear.push({value: i, label: months[(i + 4) % 12].slice(0,3) + " 2020"})
        } else {
            marksYear.push({value: i, label: ""})
        }
    } else if (i >= 9 && i < 20) {
        if ((i % 4) === 0) {
            marksYear.push({value: i, label: months[(i + 4) % 12].slice(0,3) + " 2021"})
        } else {
            marksYear.push({value: i, label: ""})
        }
    } else {
        if ((i % 4) === 0) {
            marksYear.push({value: i, label: months[(i + 4) % 12].slice(0,3) + " 2022"})
        } else {
            marksYear.push({value: i, label: ""})
        }        
    }
}

class Predictions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            slider: 0,
            disease: 'all diseases',
            country: 'all countries', 
            outbreaks: []
        };
    }

    handleChange = (state) => {
        return (value) => {
            this.setState({[state]: value});
        }
    }

    componentDidMount() {
        fetchTable().then(result => this.setState({outbreaks: result}));
    }

    format = (outbreaks) => {
        let result = outbreaks;
        if (this.state.country !== 'all countries') {
            result = result.filter(x => x.country === this.state.country);
        }

        if (this.state.disease !== 'all diseases') {
            result = result.filter(x => x.disease === this.state.disease);
        }

        result = result.map(x => ({
            date: x.date,
            country: country_conversion[x.country],
            disease: disease_conversion[x.disease],
            duration: x.duration,
            id: x.country + ' ' + x.disease
        }));
        return result;
    }

    render() {
        const params = {
            offset: this.state.slider,
            country: this.state.country, 
            disease: this.state.disease
        };

        return (
            <div id = "predictions">
                <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"></link>
                <NavBar ac = {2}/>
                <h3 className = "tHeader">Predicted Disease Outbreaks</h3>
                <PredictionsTable rows={this.format(this.state.outbreaks)}/>
                <div id = "pDiv">
                    <Map title={"Number of Predicted Disease Outbreaks by Country"} getData={(setData) => {
                        fetchMap(params).then(data => setData(data, "#1481BA"))
                    }}/>
                </div>
                <div id = "cDiv">
                    <h3 className = "pHeader">Filter Predicted Outbreaks by Month</h3>
                    <Slide style = {{marginLeft: "-3%"}} set={this.handleChange('slider')} marks={marksYear} min={0} max={30} default={0}/>
                    <h3 className = "pHeader">Filter Predicted Outbreaks by Country and Disease</h3>
                    <div>
                        <div style={{width: '50%', display: 'inline-block'}}>
                            <div style={{marginLeft: '10%', width: '80%'}}>
                                <SearchBar style={{width: '100%'}}
                                    values={country_list}
                                    converter={country_conversion}
                                    label='Country'
                                    onChange={this.handleChange('country')}
                                />
                            </div>
                        </div>
                        <div style={{width: '50%', display: 'inline-block'}}>
                            <div style={{width: '80%'}}>
                                <SearchBar style={{width: '100%', marginLeft: '-10%'}}
                                    values={disease_list}
                                    converter={disease_conversion}
                                    label='Disease'
                                    onChange={this.handleChange('disease')}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Predictions;
  