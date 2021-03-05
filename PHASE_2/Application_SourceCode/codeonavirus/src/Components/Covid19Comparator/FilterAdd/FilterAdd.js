import React from 'react';
import SearchBar from '../../SearchBar';
import { IconButton } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import { covid_country_list, country_conversion } from '../../../static';
import "./FilterAdd.css";

export default class FilterAdd extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            country: 'all countries'
        }
    }

    handleChange = (value) => {
        this.setState({country: value});
    }

    handleClick = (event) => {
        this.props.onAdd(this.state.country);
    }

    render() {
        const addDisabled = 'disabled' in this.props && this.props.disabled;
        const style = {
            width: '100%',
            marginLeft: '-20%'
        };
        return (
            <div id = "fs">
                <SearchBar
                    values={covid_country_list}
                    converter={country_conversion}
                    label='Country'
                    onChange={this.handleChange}
                    style={style}
                />
                <IconButton onClick={this.handleClick} disabled={addDisabled}>
                    <AddIcon/>
                </IconButton>
            </div>
        );
    }
 }