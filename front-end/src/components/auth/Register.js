import React, {Component} from 'react';
import '../../App.css';
import {Button, FormControl, FormGroup, FormLabel,} from 'react-bootstrap';
import history from '../../utils/history';
import {API_URL} from "../../config";
import axios from 'axios';
import {setToken} from "../../utils/storage";

class Register extends Component {
    constructor() {
        super();
        this.state = {
            login: '',
            password: '',
            confirmation: '',
        };

        this.handlePassChange = this.handlePassChange.bind(this);
        this.handleConfirmChange = this.handleConfirmChange.bind(this);
        this.handleLoginChange = this.handleLoginChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.formFilled = this.formFilled.bind(this);
    }

    handleSubmit(evt) {
        evt.preventDefault();

        if (this.state.password !== this.state.confirmation) {
            alert('Password and confirmation should be equal.');
        }

        axios.post(
            `${API_URL}/register`, {
                'login': this.state.login,
                'password': this.state.password,
                'confirmation': this.state.confirmation
            })
            .then(res => {
                if (res.status === 201) {
                    if (res.data.message) {
                        alert(res.data.message);
                    }

                    if (res.data.token) {
                        setToken(res.data.token);
                        history.push('/accounts');
                    }
                }
            })
            .catch(err => {
                if (err.response.data && err.response.data.message) {
                    alert(err.response.data.message);
                } else {
                    alert('Something bad happened. We\'ve already started working on it.')
                }
            });

        return this.setState({error: ''});
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

    handleConfirmChange(evt) {
        this.setState({
            confirmation: evt.target.value,
        });
    }

    formFilled() {
        return this.state.login && this.state.password && this.state.confirmation;
    }

    render() {
        return (
            <section className="h-100">
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
                    <FormGroup controlId="confirmation">
                        <FormLabel>Confirmation</FormLabel>
                        <FormControl
                            value={this.state.confirmation}
                            onChange={this.handleConfirmChange}
                            type="password"
                        />
                    </FormGroup>
                    <Button
                        block
                        bsSize="large"
                        type="submit"
                        disabled={!this.formFilled()}
                    >
                        Register
                    </Button>
                    <br/>
                    Already Have An Account?
                    <Button
                        block
                        bsSize="large"
                        type="submit"
                        onClick={() => history.push('/login')}
                    >
                        Login
                    </Button>
                </form>
            </section>
        );
    }
}

export default Register;