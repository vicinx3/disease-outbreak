import React from "react";
import Map from "../Map";
import Slider from "../Slider";
import Navbar from "../Navbar";
import Selector from "../Selector";
import Covid19Table from "../Covid19Table";
import LineChart from "../Covid19LineChart";
import { fetchLastDay, fetchMap } from "../../API/covid";
import "./Covid19.css";

export default class Covid19 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      date: 0,
      last: 0,
      marks: null,
      dailyChange: false,
      category: "confirmed",
    };
    this.epoch = new Date(2020, 0, 22);
  }

  componentDidMount() {
    fetchLastDay().then((r) => {
      this.setState({
        date: r.last_day,
        last: r.last_day,
        marks: r.marks,
      });
    });
  }

  handleChange = (state) => {
    return (value) => {
      console.log(`${state}: ${value}`);
      this.setState({ [state]: value });
    };
  };

  render() {
    const currentDate = addDays(this.epoch, this.state.date);
    const tabsDaily = [
      { label: "Total cases", value: "false" },
      { label: "Daily change", value: "true" },
    ];
    const tabsCategory = [
      { label: "Confirmed", value: "confirmed" },
      { label: "Recovered", value: "recovered" },
      { label: "Deaths", value: "deaths" },
    ];

    const params = {
      date: this.state.date,
      category: this.state.category,
      daily: this.state.dailyChange,
    };

    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
    };

    return (
      <div>
        <link
          href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap"
          rel="stylesheet"
        ></link>
        <Navbar ac={3} />
        <div id="sBar">
          <Covid19Table params={{ date: this.state.date }} />
        </div>
        <div id="mp">
          <Map
            title={"Number of COVID-19 Reports by Country"}
            getData={(setData) => {
              fetchMap(params).then((data) => setData(data, "#1481BA"));
            }}
          />
        </div>
        {/* Need to format this!!! */}
        <div id="pContent">
          <h1 id="cTime">{currentDate.toLocaleString("en-UK", options)}</h1>
          <Slider
            style={{ marginLeft: "3%", width: "102%" }}
            set={this.handleChange("date")}
            step={1}
            marks={this.state.marks}
            min={0}
            max={this.state.last}
            value={this.state.date}
          />
          <div style={{ display: "inline-block", width: "40%" }}>
            <Selector
              tabs={tabsDaily}
              default={"false"}
              onChange={this.handleChange("dailyChange")}
            />
          </div>
          <div style={{ display: "inline-block", width: "60%" }}>
            <Selector
              tabs={tabsCategory}
              default="confirmed"
              onChange={this.handleChange("category")}
            />
          </div>
        </div>
        <div id="chart">
          <LineChart params={params} epoch={this.epoch} />
        </div>
      </div>
    );
  }
}

function addDays(date, days) {
  const copy = new Date(Number(date));
  copy.setDate(date.getDate() + days);
  return copy;
}
