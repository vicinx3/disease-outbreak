import React from 'react';
import { Card, Typography, IconButton, TextField } from '@material-ui/core';
import ClearIcon from '@material-ui/icons/Clear';
import { country_conversion } from '../../../static';
import './FilterEntry.css';

export default class FilterEntry extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: false
        }
    }

    handleChange = (event) => {
        let value = Number(event.target.value);
        if (Number.isInteger(value)) {
            this.setState({error: false});
            this.props.onChangeOffset(this.props.country, value);
        } else {
            this.setState({error: true});
        }   
    }

    handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        } 
    }

    handleClick = (event) => {
        this.props.onDel(this.props.country);
    }

    render() {
        const error = this.state.error
        return (
            <div className='cardO'>
                <Card>
                    <div className='cardL'>
                        <div className='cardIL'>
                            <Typography color='textSecondary'>
                                Country: 
                            </Typography>
                            <Typography variant='body1' component='p'>
                                {country_conversion[this.props.country]}
                            </Typography>
                            <form noValidate autoComplete='off'>
                                <TextField error={error} label='Offset (days)' type='number' onChange={this.handleChange} onKeyDown={this.handleKeyDown}/>
                            </form>
                        </div>
                    </div>
                    <div className='cardR'>
                        <div className='cardIR'>
                            <IconButton onClick={this.handleClick}>
                                <ClearIcon/>
                            </IconButton>
                        </div>
                    </div>
                </Card>
            </div>
        );
    }
}