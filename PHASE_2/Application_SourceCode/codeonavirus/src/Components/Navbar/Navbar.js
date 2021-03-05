import React, { Component } from 'react';
import { NavLink } from "react-router-dom";
import "./Navbar.css";

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            init: true
        }
    }

    componentDidMount() {
        var divs = document.getElementsByClassName("navItem");
        divs[this.props.ac].style.backgroundColor = "#1481BA";
    }

    render() {
        return (
            <nav id = "navContainer">
                <div className="navItem">
                    <NavLink to="/" activeClassName="selected">
                        Global Diseases
                    </NavLink>
                </div>
                <div className="navItem">
                    <NavLink to="/comparator" activeClassName="selected">
                        Global Comparator
                    </NavLink>
                </div>
                <div className="navItem">
                    <NavLink to="/prediction" activeClassName="selected">
                        Prediction
                    </NavLink>
                </div>
                <div className="navItem">
                    <NavLink to="/covid_19" activeClassName="selected">
                        JHU COVID-19
                    </NavLink>
                </div>
                <div className="navItem">
                    <NavLink to="/covid_19/comparator" activeClassName="selected">
                        JHU COVID-19 Comparator
                    </NavLink>
                </div>
            </nav>
        );
    }
}

export default Navbar;