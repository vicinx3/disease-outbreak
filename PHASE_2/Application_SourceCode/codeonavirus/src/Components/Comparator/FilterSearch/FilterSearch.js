import React from 'react';
import SearchBar from '../../SearchBar';
import { IconButton } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import { disease_list, disease_conversion, country_list, country_conversion } from '../../../static';
import "./FilterSearch.css";

class FilterSearch extends React.Component {  
    constructor(props) {
        super(props);
        this.state = {
            country: "all countries", 
            disease: "all diseases",
            source: "All sources"
        }
    }

    handleChange = (name) => (value) => {
        if (value !== this.state[name]) 
            this.setState({[name]: value});
    }

    handleClick = (event) => {
        this.props.onAdd(this.state.country, this.state.disease, this.state.source);
    }

    render() {        
        const isDisabled = 'disabled' in this.props && this.props.disabled; 
        const style = {
            width: '100%',
            marginLeft: '-20%',
            marginBottom: '12px'
        };
        return (
            <div id='fs'>
                <SearchBar
                    values={country_list}
                    converter={country_conversion}
                    label='Country'
                    onChange={this.handleChange('country')}
                    style={style}
                />
                <SearchBar
                    values={disease_list}
                    converter={disease_conversion}
                    label='Disease'
                    onChange={this.handleChange('disease')}
                    style={style}
                />
                <SearchBar
                    values={['All sources', 'WHO', 'ProMED']}
                    converter={{'All sources': 'All sources', 'WHO': 'WHO', 'ProMED': 'ProMED'}}
                    label='Source'
                    onChange={this.handleChange('source')}
                    style={style}
                />
                {/* <div className = "sButton"> */}
                <IconButton onClick={this.handleClick} disabled={isDisabled}>
                    <AddIcon/>
                </IconButton>
                {/* </div> */}
            </div>
        );
    }
}

export default FilterSearch;