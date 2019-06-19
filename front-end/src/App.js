import React, {Component} from 'react';
import './App.css';
import {Route, Switch} from 'react-router';
import LoginPage from './components/auth/Login';
import Register from './components/auth/Register';
import MainLayout from './components/common/MainLayout';
import EventList from './components/events/EventList';
import AccountList from "./components/accounts/AccountList";
import NotFound from "./components/errors/NotFound";
import AuthenticatedRoute from "./routes/AuthenticatedRoute";
import Logout from "./components/auth/Logout";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Transfer from "./components/modals/Transfer";


class App extends Component {
    constructor() {
        super();

        this.state = {
            transferModal: false,
        };

        this.transferModalToggle = this.transferModalToggle.bind(this);
    }

    transferModalToggle() {
        this.setState({
            transferModal: !this.state.transferModal
        });
    }

    render() {
        return (
            <div className="App">
                <Container>
                    <Row>
                        <Col md={{span: 8, offset: 2}}>
                            <Switch>
                                <Route exact path="/" component={LoginPage}/>
                                <Route path="/login" component={LoginPage}/>
                                <Route path="/register" component={Register}/>
                                <Route path="/logout" component={Logout}/>

                                <MainLayout>
                                    <Switch>
                                        <AuthenticatedRoute path="/history" component={EventList}/>
                                        <AuthenticatedRoute path="/accounts" component={AccountList} />
                                        <AuthenticatedRoute path="/transfer" component={Transfer}/>
                                    </Switch>
                                </MainLayout>

                                <Route component={NotFound}/>
                            </Switch>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export default App;
