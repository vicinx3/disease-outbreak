import { fetcher, extractCountry } from "./utils";

export async function fetchLastDay() {
  const url = new URL("http://127.0.0.1:5001/covid/last_day");
  return await fetcher(url, "Failed to fetch last day");
}

export async function fetchMap(filter) {
  const url = new URL("http://127.0.0.1:5001/covid/map");
  const params = [
    ["date", filter.date],
    ["category", filter.category],
    ["daily", filter.daily],
  ];
  url.search = new URLSearchParams(params).toString();
  return await fetcher(url, "Failed to fetcch map data");
}

export async function fetchTable(filter) {
  const url = new URL("http://127.0.0.1:5001/covid/table");
  const params = [["date", filter.date]];
  url.search = new URLSearchParams(params).toString();
  return await fetcher(url, "Failed to fetch table data");
}

export async function fetchLineChart(filter) {
  const url = new URL("http://127.0.0.1:5001/covid/line_chart");
  const params = [["daily", filter.daily]];
  url.search = new URLSearchParams(params).toString();
  return await fetcher(url, "Failed to fetch line chart data");
}

export async function fetchComparator(filter) {
  const url = new URL("http://127.0.0.1:5001/covid/comparator");
  const params = [];
  extractCountry(params, filter);
  url.search = new URLSearchParams(params).toString();
  return await fetcher(url, "Failed to fetch comparator data");
}
