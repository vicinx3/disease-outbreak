import React, { Component } from 'react';
import NavBar from "../Navbar";
import Map from '../Map';
import Slide from '../Slider';
import Sidebar from '../Sidebar';
import SearchBar from '../SearchBar';
import Modal from '../Modal/Modal';
import PieChart from '../PieChart';
import { fetchPieChartDisease, fetchMap } from '../../API/main';
import { disease_list, disease_conversion, country_list, country_conversion } from '../../static';
import "./MainPage.css";

let marksYear = []
for (let i = 0; i < 25; i++) {
    marksYear.push({value: 1996 + i, label: (1996 + i).toString()})
}

let marksMonth = []
let months = ["January", "February", "March",  "April", "May", "June",  "July", "August", "September", "October", "November", "December"];
for (let i = 1; i < 13; i++) {
    marksMonth.push({value: i, label: months[i - 1]})
}
marksMonth.unshift({value:0, label:'Show All'})

class MainPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            month: "0",
            year: "2020",
            country: 'all countries',
            disease: 'all diseases',
            articles: [],
            selectedPost: 'https://www.who.int/csr/don/2001_08_15/en/', // Random
            show: false
        }
    }

    setYear = (year) => {
        if (year !== this.state.year) {
            this.setState({
                year: year
            })
        }
    }
    
    setMonth = (month) => {
        if (month !== this.state.month) {
            this.setState({
                month: month
            })
        }
    }

    setDisease = (disease) => {
        if (disease !== this.state.disease) {
            this.setState({disease: disease});
        }
    }

    setCountry = (country) => {
        if (country !== this.state.country) {
            this.setState({country: country});
        }
    }

    setSel = (url) => {
        if (url !== this.state.selectedPost) {
            this.setState({
                selectedPost: url
            })
        }
    }

    showModal = () => {
        this.setState({
            show: true
        })
    }

    hideModal = () => {
        this.setState({
            show: false
        })
    }

    render() {
        const params = {
            year: this.state.year,
            month: this.state.month,
            country: this.state.country, 
            disease: this.state.disease
        };

        return (
            <div id = "root">
                <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"></link>
                <NavBar ac = {0}/>
                <Map title={"Number of Disease Reports by Country"} getData={(setData) => {
                    fetchMap(params).then(data => setData(data, "#1481BA"))
                }}/>
                <h3 className = "header">Filter Disease Reports By Year</h3>
                <Slide set={this.setYear} marks={marksYear} min={1996} max={2020} default={2020}/>
                <h3 className = "header">Filter Disease Reports By Month</h3>
                <Slide set={this.setMonth} marks={marksMonth} min={0} max={12} default={0}/>
                <h3 className = "header">Filter Disease Reports By Disease And Country</h3>
                <div style={{display: 'inline-block', width: '50%'}}>
                    <div style={{marginLeft: '20%'}}>
                        <SearchBar 
                            values={country_list}
                            converter={country_conversion}
                            label='Country Filter'
                            onChange={this.setCountry}
                            style={{width: '120%', marginLeft: '-20%'}}
                        />
                    </div>
                </div>
                <div style={{display: 'inline-block', width: '50%', marginBottom: '3.5%'}}>
                    <div style={{marginRight: '20%'}}>
                        <SearchBar 
                            values={disease_list}
                            converter={disease_conversion}
                            label='Disease Filter'
                            onChange={this.setDisease}
                            style={{width: '120%', marginLeft: '-20%'}}
                        />
                    </div>
                </div>
                <PieChart getData={(setData) => {
                    fetchPieChartDisease(params).then(data => setData(data))
                }}/>
                <Sidebar params={params} setSel={this.setSel} showModal={this.showModal}/>
                <Modal show = {this.state.show} url={this.state.selectedPost} hideModal = {this.hideModal}></Modal>
            </div>
        )
    }
}

export default MainPage