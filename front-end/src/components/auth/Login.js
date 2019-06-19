import React, {Component} from 'react';
import '../../App.css';
import axios from "axios/index";
import {API_URL} from '../../config';
import {setToken} from "../../utils/storage";
import history from '../../utils/history';
import Button from 'react-bootstrap/Button';
import FormLabel from 'react-bootstrap/FormLabel';
import FormControl from 'react-bootstrap/FormControl';
import FormGroup from 'react-bootstrap/FormGroup';

class Login extends Component {
    constructor() {
        super();
        this.state = {
            login: '',
            password: '',
            error: '',
        };

        this.handlePassChange = this.handlePassChange.bind(this);
        this.handleLoginChange = this.handleLoginChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    formFilled() {
        return this.state.login && this.state.password;
    }

    handleSubmit(evt) {
        evt.preventDefault();

        axios.post(`${API_URL}/login`, {
            login: this.state.login,
            password: this.state.password
        }).then(res => {
            if (res.status === 200) {
                setToken(res.data.token);

                history.push('/accounts');
            }
        }).catch(err => {
            if (err.response.data && err.response.data.message) {
                alert(err.response.data.message);
            } else {
                alert('Something bad happened. We\'ve already started working on it.')
            }
        });
    }

    handleLoginChange(evt) {
        this.setState({
            login: evt.target.value,
        });
    };

    handlePassChange(evt) {
        this.setState({
            password: evt.target.value,
        });
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <FormGroup controlId="email">
                    <FormLabel>Login</FormLabel>
                    <FormControl
                        autoFocus
                        type="text"
                        value={this.state.login}
                        onChange={this.handleLoginChange}
                    />
                </FormGroup>
                <FormGroup controlId="password">
                    <FormLabel>Password</FormLabel>
                    <FormControl
                        value={this.state.password}
                        onChange={this.handlePassChange}
                        type="password"
                    />
                </FormGroup>
                <Button
                    block
                    bsSize="large"
                    type="submit"
                    disabled={!this.formFilled()}
                >
                    Login
                </Button>
                <Button
                    block
                    bsSize="large"
                    onClick={() => history.push('/register')}
                >
                    Register
                </Button>
            </form>
        );
    }
}

export default Login;