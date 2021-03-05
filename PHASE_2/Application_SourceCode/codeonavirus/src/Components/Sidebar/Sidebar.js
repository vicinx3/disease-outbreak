import React, { Component } from 'react';
import { fetchSidebar } from '../../API/main';
import "./Sidebar.css";
import { withStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TablePagination from '@material-ui/core/TablePagination';
import Paper from '@material-ui/core/Paper';
import lightBlue from '@material-ui/core/colors/lightBlue';

const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: lightBlue[500],
      color: theme.palette.common.black,
      zIndex: 0
    },
    body: {
      fontSize: 14,
      color: theme.palette.common.black,
    },
  }))(TableCell);
  
const StyledTableRow = withStyles((theme) => ({
    root: {
        '&:nth-of-type(odd)': {
            backgroundColor: theme.palette.common.white,
        },
        '&:nth-of-type(even)': {
            backgroundColor: lightBlue[100],
        }    
    },
}))(TableRow);

export default class Sidebar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            articles: [],
            params: null,
            page: 0,
            rowsPerPage: 10,
        }
    }

    onOpenModal = url => {
        this.props.setSel(url);
    };

    show = () => {
        this.props.showModal();
    }

    setPage = (num) => {
      this.setState({
          page: num
      })
    }

    setRowsPerPage = (num) => {
      this.setState({
          rowsPerPage: num
      })
    }

    handleChangePage = (event, newPage) => {
      this.setPage(newPage);
    };
    
    handleChangeRowsPerPage = (event) => {
      this.setRowsPerPage(+event.target.value);
      this.setPage(0);
    };

    componentDidMount() {
        this.componentDidUpdate();
    }

    componentDidUpdate() {
        if (this.props.params !== this.state.params) {
            fetchSidebar(this.props.params).then(result => {
                this.setState({
                    articles: result,
                    params: this.props.params
                });
            });
      }
    }

    render() {
        const articles = this.state.articles;
        return (
          <div>
          <h1 id = "aHeading">Articles</h1>
            <div id = "table">
            <TableContainer component={Paper}>
              <Table stickyHeader aria-label="sticky table">
                <TableHead className = "th">
                  <StyledTableRow>
                    <StyledTableCell width="10%">Date</StyledTableCell>
                    <StyledTableCell align="left">Headline</StyledTableCell>
                    <StyledTableCell align="left" width="18%">URL</StyledTableCell>
                    <StyledTableCell align="left" width="15%">Main Text</StyledTableCell>
                  </StyledTableRow>
                </TableHead>
                <TableBody>
                  {articles.slice(this.state.page * this.state.rowsPerPage, this.state.page * this.state.rowsPerPage + this.state.rowsPerPage).map((article, i) => (
                    <StyledTableRow key={article.date_of_publication + article.headline}>
                      <StyledTableCell component="th" scope="article">
                        {article.date}
                      </StyledTableCell>
                      <StyledTableCell align="left">{article.headline}</StyledTableCell>
                      <StyledTableCell align="left" component="a" href={article.url}>{article.source} Link</StyledTableCell>
                      <StyledTableCell component = "a" className = "sm" onClick = {() => {this.onOpenModal(article.url); this.show()}}>View</StyledTableCell>
                    </StyledTableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            </div>
            <div id = "pagination">
            <TablePagination
              rowsPerPageOptions={[10, 25, 100]}
              component="div"
              count={articles.length}
              rowsPerPage={this.state.rowsPerPage}
              page={this.state.page}
              onChangePage={this.handleChangePage}
              onChangeRowsPerPage={this.handleChangeRowsPerPage}
            />
            </div>
          </div>
        );
    }
}
  