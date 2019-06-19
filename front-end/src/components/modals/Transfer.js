import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import {API_URL} from "../../config";
import axios from 'axios';
import history from '../../utils/history';

class Transfer extends React.Component {
    constructor() {
        super();

        this.state = {
            toUser: null,
            toAccount: null,
            fromAccount: null,
            amount: null,
            accounts: [],
            users: []
        };

        this.handleToUserChosen = this.handleToUserChosen.bind(this);
        this.handleFromAccountChosen = this.handleFromAccountChosen.bind(this);
        this.handleToAccountChosen = this.handleToAccountChosen.bind(this);
        this.handleAmountChange = this.handleAmountChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.formFilled = this.formFilled.bind(this);
        this.getToUserAccounts = this.getToUserAccounts.bind(this);
        this.reset = this.reset.bind(this);
        this.loadAccounts = this.loadAccounts.bind(this);
        this.loadUsers = this.loadUsers.bind(this);
    }

    reset() {
        this.setState({
            toUser: null,
            toAccount: null,
            fromAccount: null,
            amount: null,
        });
    }

    loadAccounts() {
        axios.get(`${API_URL}/accounts`)
            .then(res => {
                if (res.status === 200) {
                    this.setState({
                        accounts: res.data.data
                    });
                }
            });
    }

    loadUsers() {
        axios.get(`${API_URL}/users`)
            .then(res => {
                if (res.status === 200) {
                    this.setState({
                        users: res.data.data
                    });
                }
            });
    }

    componentDidMount() {
        this.reset();
        this.loadAccounts();
        this.loadUsers();
    }

    handleToUserChosen(evt) {
        this.setState({
            toUser: evt.target.value
        });
    }

    handleFromAccountChosen(evt) {
        this.setState({
            fromAccount: evt.target.value
        });
    }

    handleToAccountChosen(evt) {
        this.setState({
            toAccount: evt.target.value
        });
    }

    handleAmountChange(evt) {
        this.setState({
            amount: parseFloat(evt.target.value)
        });
    }

    handleSubmit(evt) {
        evt.preventDefault();

        const fromAccount = this.state.accounts.find(account => account.id === parseInt(this.state.fromAccount));

        if (fromAccount.balance < this.state.amount) {
            alert('There\'s not enough funds.');
            return;
        }

        if (this.state.fromAccount === this.state.toAccount) {
            alert('From Account and To Account could not be the same.');
            return;
        }

        axios.post(
            `${API_URL}/accounts/transfer`,
            {
                'account_from_id': this.state.fromAccount,
                'account_to_id': this.state.toAccount,
                'amount': this.state.amount
            })
            .then(res => {
                console.log(res.data.message);

                if (res.status === 200) {
                    if (res.data.message) {
                        alert(res.data.message);
                    } else {
                        alert('Successfull transfer');
                        history.push('/accounts');
                    }
                }

                this.loadAccounts();
            })
            .catch(error => {
                alert('Transfer failed. We already know about the problem and working on it.')
            });
    }

    formFilled() {
        return this.state.fromAccount && this.state.toUser && this.state.toAccount && this.state.amount;
    }

    getToUserAccounts() {
        if (!this.state.toUser) {
            return [];
        }

        let toUser = this.state.users.find(user => user.id === parseInt(this.state.toUser));

        if (!toUser) {
            return [];
        }

        return toUser.accounts;
    }

    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="transfer.fromAccount">
                    <Form.Label>From</Form.Label>
                    <Form.Control as="select" onChange={this.handleFromAccountChosen}>
                        <option value="-1">Select Account...</option>
                        {this.state.accounts.map(account =>
                            <option key={account.id} value={account.id}>
                                {account.currency.ticker} ({account.balance})
                            </option>
                        )}
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="transfer.toUser">
                    <Form.Label>To</Form.Label>
                    <Form.Control as="select" onChange={this.handleToUserChosen}>
                        <option value="-1">Select User...</option>
                        {this.state.users.map(user =>
                            <option key={user.id} value={user.id}>
                                {user.login}
                            </option>
                        )}
                    </Form.Control>
                    <Form.Control as="select" disabled={!this.state.toUser}
                                  onChange={this.handleToAccountChosen}>
                        <option value="-1">Select Account...</option>
                        {this.getToUserAccounts().map(account =>
                            <option key={account.id}
                                    value={account.id}>
                                {account.currency.ticker}
                            </option>
                        )}
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="transfer.Amount">
                    <Form.Label>Amount</Form.Label>
                    <Form.Control type="text" onChange={this.handleAmountChange}/>
                </Form.Group>
                <Button variant="primary" type="submit" disabled={!this.formFilled()}>Transfer</Button>
            </Form>
        );
    }
}

export default Transfer;