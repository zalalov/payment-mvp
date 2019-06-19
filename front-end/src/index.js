import 'bootstrap/dist/css/bootstrap.css';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {Router} from "react-router-dom";
import history from './utils/history';
import axios from 'axios';
import {getToken} from "./utils/storage";

axios.interceptors.request.use(function (config) {
    const token = getToken();

    if (token) {
        config.headers.Authorization =  `Bearer: ${token}`;
    }

    return config;
});

ReactDOM.render(
    <Router history={history}>
        <App/>
    </Router>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
