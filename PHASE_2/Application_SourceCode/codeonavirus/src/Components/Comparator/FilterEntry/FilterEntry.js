import React from 'react';
import { Card, 
    Typography, IconButton, CircularProgress } from '@material-ui/core';
import ClearIcon from '@material-ui/icons/Clear';
import { disease_conversion, country_conversion } from '../../../static';

export default class FilterEntry extends React.Component {

    handleClick = (event) => {
        this.props.onDel(this.props.country, this.props.disease, this.props.source);
    }

    render() {
        let button;
        if (this.props.loaded) {
            button = (
                <IconButton onClick={this.handleClick}>
                    <ClearIcon/>
                </IconButton>
            );
        } else {
            button = <CircularProgress size="30px"/>;
        }

        return (
            <div className='card0'>
                <Card style={{ height: '100%'}}>
                    <div className='cardL'>
                        <div className='cardIL'>
                            <Typography color='textSecondary'>
                                Country: 
                            </Typography>
                            <Typography variant='body1' componen='p'>
                                {country_conversion[this.props.country]}
                            </Typography>

                            <Typography color='textSecondary'>
                                Disease:
                            </Typography>
                            <Typography variant='body1' componen='p'>
                                {disease_conversion[this.props.disease]}
                            </Typography>

                            <Typography color='textSecondary'>
                                Source: 
                            </Typography>
                            <Typography variant='body1' componen='p'>
                                {this.props.source}
                            </Typography>
                        </div>
                    </div>
                    <div className='cardR'>
                        <div className='cardIR'>
                            {button}
                        </div>
                    </div>
                </Card>
            </div>
        );
    }
}