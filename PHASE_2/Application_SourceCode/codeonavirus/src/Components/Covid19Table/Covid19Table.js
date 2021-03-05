import React from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableSortLabel from "@material-ui/core/TableSortLabel";
import Paper from "@material-ui/core/Paper";
import { fetchTable } from "../../API/covid";
import "./Covid19Table.css";

export default class Covid19Table extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rows: [],
      order: "desc",
      orderBy: "confirmed",
    };

    this.headCells = [
      { id: "country", align: "left", label: "Country", width: "20%" },
      { id: "confirmed", align: "right", label: "Confirmed" },
      { id: "recovered", align: "right", label: "Recovered" },
      { id: "deaths", align: "right", label: "Deaths" },
      { id: "mortality", align: "right", label: "Mortality Rate (%)" },
    ];
  }

  createSortHandler = (property) => (event) => {
    this.handleRequestSort(event, property);
  };

  handleRequestSort = (event, property) => {
    const isAsc = this.state.orderBy === property && this.state.order === "asc";
    this.setState({
      order: isAsc ? "desc" : "asc",
      orderBy: property,
    });
  };

  componentDidUpdate(prevProps) {
    if (this.props.params.date !== prevProps.params.date) {
      fetchTable(this.props.params).then((result) => {
        this.setState({
          params: this.props.params,
          rows: result,
        });
      });
    }
  }

  render() {
    const rows = this.state.rows;
    const order = this.state.order;
    const orderBy = this.state.orderBy;

    return (
      <Paper id="main">
        <TableContainer>
          <Table size="medium">
            <TableHead>
              <TableRow>
                {this.headCells.map((headCell) => (
                  <TableCell
                    key={headCell.id}
                    align={headCell.align}
                    width={headCell.width}
                  >
                    <TableSortLabel
                      active={orderBy === headCell.id}
                      direction={orderBy === headCell.id ? order : "asc"}
                      onClick={this.createSortHandler(headCell.id)}
                    >
                      {headCell.label}
                    </TableSortLabel>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {stableSort(rows, getComparator(order, orderBy)).map((row, index) => {
                return (
                  <TableRow hover key={row.country}>
                    <TableCell>{row.country}</TableCell>
                    <TableCell align="right">{row.confirmed}</TableCell>
                    <TableCell align="right">{row.recovered}</TableCell>
                    <TableCell align="right">{row.deaths}</TableCell>
                    <TableCell align="right">{row.mortality}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    );
  }
}

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}
