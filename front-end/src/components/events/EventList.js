import React, {Component} from 'react';
import Table from 'react-bootstrap/Table';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import axios from "axios/index";
import {API_URL} from "../../config";

class EventList extends Component {
    static TYPE_TRANSFER = 100;
    static TYPE_FEE = 200;
    static TYPE_CONVERT = 300;

    static STATUS_PENDING = 200;
    static STATUS_SUCCESS = 300;
    static STATUS_FAILED = 300;

    constructor() {
        super();

        this.state = {
            filter: '',
            orderField: 'created_at',
            events: []
        };

        this.handleFilterChanged = this.handleFilterChanged.bind(this);
        this.handleOrderFieldClick = this.handleOrderFieldClick.bind(this);
        this.loadEvents = this.loadEvents.bind(this);
    }

    componentDidMount() {
        this.loadEvents();
    }

    loadEvents() {
        axios.get(`${API_URL}/events`)
            .then(res => {
                if (res.status === 200) {
                    this.setState({
                        events: res.data.data
                    });
                }
            });
    }

    parseEvent(event) {
        const transactions = event.transactions;

        if (!transactions || !transactions.length) {
            return 0;
        }

        const feeTransaction = transactions.find(tr => parseInt(tr.type) === EventList.TYPE_FEE);
        const convertTransaction = transactions.find(tr => parseInt(tr.type) === EventList.TYPE_CONVERT);
        const transferTransaction = transactions.find(tr => parseInt(tr.type) === EventList.TYPE_TRANSFER);
        const external = !!transferTransaction;
        const convert = !!convertTransaction;
        let accountFrom = null;
        let accountTo = null;
        let amount = 0;

        if (external) {
            accountTo = `${transferTransaction.account_to.user} (${transferTransaction.account_to.currency.ticker})`;
            amount = `${transferTransaction.value} (${transferTransaction.account_to.currency.ticker})`;

            if (convert) {
                accountFrom = `${convertTransaction.account_from.user} (${convertTransaction.account_from.currency.ticker})`;
            } else {
                accountFrom = `${transferTransaction.account_from.user} (${transferTransaction.account_from.currency.ticker})`;
            }
        } else {
            accountFrom = `${convertTransaction.account_from.user} (${convertTransaction.account_from.currency.ticker})`;
            accountTo = `${convertTransaction.account_to.user} (${convertTransaction.account_to.currency.ticker})`;
            amount = `${convertTransaction.value} (${convertTransaction.account_to.currency.ticker})`;
        }

        return {
            id: event.id,
            from: accountFrom,
            to: accountTo,
            amount: `${amount}`,
            fee: feeTransaction ? feeTransaction.value : 0,
            created_at: event.created_at
        }
    }

    getEvents() {
        console.log(this.state.orderField);

        let events = this.state.events.map(event => this.parseEvent(event));

        if (this.state.filter) {
            events = events.filter(event => {
                return Object.values(event).join(' ').toLowerCase().includes(this.state.filter.toLowerCase());
            });
        }

        const sorter = (a, b) => {
            if (a[this.state.orderField] > b[this.state.orderField]) {
                return 1;
            }

            if (a[this.state.orderField] < b[this.state.orderField]) {
                return -1
            }

            return 0;
        };

        if (this.state.orderField) {
            events.sort(sorter);
        }

        return events;
    }

    handleFilterChanged(evt) {
        this.setState({
            filter: evt.target.value
        });
    }

    handleOrderFieldClick(evt) {
        this.setState({
            orderField: evt.target.getAttribute('data-order-field')
        });
    }

    render() {
        return (
            <div>
                <InputGroup className="mb-3">
                    <InputGroup.Prepend>
                        <InputGroup.Text id="basic-addon1">Filter</InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl onChange={this.handleFilterChanged}/>
                </InputGroup>
                <Table bordered>
                    <thead>
                    <tr onClick={this.handleOrderFieldClick}>
                        <th data-order-field="from" style={{cursor: 'pointer'}} width="10">From</th>
                        <th data-order-field="to" style={{cursor: 'pointer'}} width="10">To</th>
                        <th data-order-field="amount" style={{cursor: 'pointer'}} width="10">Amount</th>
                        <th data-order-field="fee" style={{cursor: 'pointer'}} width="10">Fee</th>
                    </tr>
                    </thead>
                    <tbody>
                    {this.getEvents(this.state.filter, this.state.orderField).map(event =>
                        <tr key={event.id} onClick={() => {
                            alert(123)
                        }}>
                            <td onClick={() => alert(123)}>{event.from}</td>
                            <td>{event.to}</td>
                            <td>{event.amount}</td>
                            <td>{event.fee}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>
            </div>
        )
    }
}

export default EventList;