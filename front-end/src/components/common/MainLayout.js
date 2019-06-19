import React, {Component} from 'react';
import history from "../../utils/history";
import TransferModal from '../modals/Transfer';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';

class MainLayout extends Component {
    render() {
        return (
            <div className="Dashboard">
                <div className="App-Frame">
                    <Navbar>
                        <Navbar.Collapse>
                            <Nav.Item>
                                <Nav.Link href="/accounts">Accounts</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link href="/history">History</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link href="/transfer">Transfer</Nav.Link>
                            </Nav.Item>
                        </Navbar.Collapse>
                        <Navbar.Collapse className="justify-content-end">
                            <Nav.Item>
                                <Button variant="secondary" onClick={() => history.push('/logout')}>Logout</Button>
                            </Nav.Item>
                        </Navbar.Collapse>
                    </Navbar>

                    <main className="Content">
                        {this.props.children}
                    </main>
                </div>
            </div>
        )
    }
}

export default MainLayout;