import React, { Component } from 'react';
import { Multiselect } from 'multiselect-react-dropdown';
import getDiseases from './getDiseases';

class DiseaseSearchBar extends Component {
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
        var diseases = this.multiselectRef.current.getSelectedItems();
        this.props.submit(diseases);
    }

    componentDidMount() {
        const diseases = getDiseases();
        this.setState({options: diseases});
    }

    render() {
        return (
            <div id = "sbar">
                <Multiselect
                    options={this.state.options} // Options to display in the dropdown
                    onSelect={this.handleSubmit} // Function will trigger on select event
                    onRemove={this.handleSubmit} // Function will trigger on remove event
                    isObject={false}
                    id="disease"
                    selectionLimit="1"
                    ref={this.multiselectRef}
                    placeholder="Disease Search (Max 1)"
                />
            </div>
        );
    }
}

export default DiseaseSearchBar;