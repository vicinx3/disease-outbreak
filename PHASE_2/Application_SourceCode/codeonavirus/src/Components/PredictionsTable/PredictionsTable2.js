import React from 'react';
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableSortLabel from "@material-ui/core/TableSortLabel";
import Paper from "@material-ui/core/Paper";
import "./PredictionsTable.css";


export default class PredictionsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            params: null,
            // rows: [], 
            order: 'asc',
            orderBy: 'date'
        }

        this.headCells = [
            {id: 'date', align: 'left', label: 'Date', width: '20%'},
            {id: 'country', align: 'left', label: 'Country'},
            {id: 'disease', align: 'left', label: 'Disease'},
            {id: 'duration', align: 'right', label: 'Duration (days)'},
        ];
    }

    createSortHandler = property => event => {
        this.handleRequestSort(event, property)
    }

    handleRequestSort = (event, property) => { 
        const isAsc = this.state.orderBy === property && this.state.order === 'asc';
        this.setState({
            order: isAsc ? 'desc' : 'asc',
            orderBy: property 
        });
    }

    // componentDidUpdate() {
    //     if (this.props.params !== this.state.params) {
    //         fetchTable().then(result => {
    //             this.setState({
    //                 params: this.props.params, 
    //                 rows: result
    //             });
    //         });
    //     }
    // }

    render() {
        const rows = this.props.rows;
        const order = this.state.order;
        const orderBy = this.state.orderBy;
        
        return (
            <Paper id = "pMain">
                <TableContainer>
                    <Table
                        size="medium"
                    >
                        <TableHead>
                            <TableRow>
                                {this.headCells.map(headCell => (
                                    <TableCell
                                        key={headCell.id}
                                        align={headCell.align}
                                        width={headCell.width}
                                    >
                                        <TableSortLabel
                                            active={orderBy === headCell.id}
                                            direction={orderBy === headCell.id ? order : 'asc'}
                                            onClick={this.createSortHandler(headCell.id)}
                                        >
                                            {headCell.label}
                                        </TableSortLabel>
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {stableSort(rows, getComparator(order, orderBy)).map(
                                (row,index) => {
                                    return (
                                        <TableRow hover key={row.id}>
                                            <TableCell>{row.date}</TableCell>
                                            <TableCell>{row.country}</TableCell>
                                            <TableCell>{row.disease}</TableCell>
                                            <TableCell align='right'>{row.duration}</TableCell>
                                        </TableRow>
                                    );
                                }
                            )}
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
    return order === 'desc'
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
    return stabilizedThis.map(el => el[0]);
}