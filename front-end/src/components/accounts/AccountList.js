import React, {Component} from 'react';
import Table from 'react-bootstrap/Table';
import axios from "axios/index";
import {API_URL} from "../../config";

class AccountList extends Component {
    constructor() {
        super();

        this.state = {
            accounts: []
        };

        this.loadAccounts = this.loadAccounts.bind(this);
    }

    componentDidMount() {
        this.loadAccounts();
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

    render() {
        return (
            <Table bordered>
                <thead>
                <tr>
                    <th width="90">Currency</th>
                    <th width="10">Balance</th>
                </tr>
                </thead>
                <tbody>
                {this.state.accounts.map(account =>
                    <tr key={account.id}>
                        <td>{account.currency.ticker}</td>
                        <td>{account.balance}</td>
                    </tr>
                )}
                </tbody>
            </Table>
        )
    }
}

export default AccountList;