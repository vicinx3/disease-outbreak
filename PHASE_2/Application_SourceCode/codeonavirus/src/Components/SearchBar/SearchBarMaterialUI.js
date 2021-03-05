import React from 'react';
import { FormControl, InputLabel, Select} from '@material-ui/core';
import "./SearchBar.css";

export default class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: this.props.values[0]
        }
    }

    handleChange = (event) => {
        const newValue = event.target.value;
        this.props.onChange(newValue);
        this.setState({value: newValue});
    }

    render() {
        const valuesSelect = this.props.values.map(value => (
            <option key={value} value={value}>{this.props.converter[value]}</option>
        ));
        
        const style = 'style' in this.props ? this.props.style : {}
        return (
            <FormControl className = "searchBar" style={style}>
                <InputLabel className = "iLabel">
                    {this.props.label}
                </InputLabel>
                <Select className = "select"
                    native
                    value={this.state.value}
                    onChange={this.handleChange}
                >
                    {valuesSelect}
                </Select>
            </FormControl>
        );
    }
}