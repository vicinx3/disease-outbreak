import React from 'react';
import { Switch, Route } from 'react-router-dom';
import MainPage from '../MainPage';
import Covid19 from '../Covid19';
import Covid19Comparator from '../Covid19Comparator';
import Predictions from '../Predictions';
import Comparator from '../Comparator';

function App() { 
    return (
        <Switch>
            <Route 
                exact 
                path="/"
                component={MainPage}
            />
            <Route 
                exact 
                path="/covid_19"
                component={Covid19}
            />   
            <Route 
                exact 
                path="/prediction"
                component={Predictions}
            />
            <Route
                exact
                path="/covid_19/comparator"
                component={Covid19Comparator}
            />
            <Route
                exact
                path="/comparator"
                component={Comparator}
            />
        </Switch>
    );
}

export default App; 