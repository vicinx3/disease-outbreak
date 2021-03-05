import React, { Component } from 'react';
import Slider from '@material-ui/core/Slider';
import { withStyles } from '@material-ui/core/styles';
import "./Slider.css"

const Styledslider= withStyles({
    root: {
      width: '80%',
      left: '100px',
      color: '#00487C',
    },
    thumb: {
        height: 24,
        width: 24,
        backgroundColor: '#fff',
        border: '2px solid currentColor',
        marginTop: -8,
        marginLeft: -12,
    },
    track: {
        height: 8,
        borderRadius: 4,
    },
    rail: {
        height: 8,
        borderRadius: 4,
        opacity: 1,

    },
    markLabel: {
        color: "#000"
    },
    mark: {
        opacity: 1,
        backgroundColor: '#fff'
    }
  })(Slider);

class Slide extends Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.state = {
            value: this.props.default
        }
    }    

    handleChange = (e, newValue) => {
        this.props.set(newValue)
        if (!('value' in this.props)) {
            this.setState({value: newValue})
        }
    }

    render() {
        const step = 'step' in this.props ? this.props.step : null;
        const value = 'value' in this.props ? this.props.value: this.state.value;

        const style = 'style' in this.props ? this.props.style : {};
        return (
            <div id = "slider" style={style}>
                <Styledslider
                    value = {value}
                    step = {step}
                    marks = {this.props.marks}
                    min = {this.props.min}
                    max = {this.props.max}
                    onChange = {this.handleChange}
                />
            </div>
        );
    }
}

export default Slide