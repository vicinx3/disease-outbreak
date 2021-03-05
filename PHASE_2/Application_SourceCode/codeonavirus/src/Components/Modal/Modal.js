import React, {Component} from 'react';
import { fetchModal } from '../../API/main';
import "./Modal.css";

class Modal extends Component {
    // eslint-disable-next-line
    constructor(props) {
        super(props);
        this.state = {
            url: null, 
            post: null,
        }
    }

    hideModal = () => {
        this.props.hideModal()
    }

    componentDidUpdate() {
        if (this.props.show === true) {
            var modals = document.getElementsByClassName('modal');
            var modal = modals[0];
            var mod = this;
            window.onclick = function (event) {
            if (event.target === modal) {
                mod.props.hideModal();
            }
        }
        }
    }

    render() {
        if (this.props.url !== this.state.url) {
            fetchModal(this.props.url).then(result => {
                this.setState({
                    url: this.props.url,
                    post: result
                });
            });
        }
        const showHideClassName = this.props.show ? 'modal-display-block' : 'modal-display-none';
        const post = this.state.post;
        if (post !== null) {
            return(
                <div className = {showHideClassName}>
                    <div className = "modal">
                        <div className = "modal-main">
                            <button className = "cButton" onClick = {() => this.hideModal()}>
                                    Close
                            </button>
                            <h1 className = "mHeader">{post.headline}</h1>
                            <p className = "maintext">{post.main_text}</p>
                        </div>
                    </div>
                </div>
            );
        } else {
            return (<div></div>);
        }
    }
}

export default Modal;