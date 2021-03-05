import React from 'react';
import { Tabs, Tab } from '@material-ui/core'

export default class Selector extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: this.props.default
        }
    }

    handleChange = (event, newValue) => {
        this.setState({value: newValue});
        this.props.onChange(newValue);
    } 

    render() {
        const tabs = this.props.tabs.map(tab => {
            return <Tab label={tab.label} value={tab.value} key={tab.value}/>
        });

        return (
            <Tabs 
                value={this.state.value}
                indicatorColor='primary'
                textColor='primary'
                onChange={this.handleChange}
                centered
            >
                {tabs}
            </Tabs>
        );
    }
}
