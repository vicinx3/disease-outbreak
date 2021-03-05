import React, { Component } from 'react';
import { Multiselect } from 'multiselect-react-dropdown';
import getCountries from './getCountries';
import "./SearchBar.css";

class SearchBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: "",
            options: []
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.multiselectRef = React.createRef();
    }

    handleSubmit(event) {
        var countries = this.multiselectRef.current.getSelectedItems();
        console.log(countries)
        this.props.submit(countries);
    }

    componentDidMount() {
        const countries = getCountries();
        this.setState({options: countries});
    }

    render() {
        return (
            <div id = "countsbar">
                <Multiselect
                    options={this.state.options} // Options to display in the dropdown
                    onSelect={this.handleSubmit} // Function will trigger on select event
                    onRemove={this.handleSubmit} // Function will trigger on remove event
                    id="country"
                    displayValue="name"
                    selectionLimit="1"
                    ref={this.multiselectRef}
                    placeholder="Country Search (Max 1)"
                />
            </div>
        );
    }
}

export default SearchBar;