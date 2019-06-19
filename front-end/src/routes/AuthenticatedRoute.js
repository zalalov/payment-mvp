import React from 'react';
import {Redirect, Route} from 'react-router';

import {getToken} from '../utils/storage';

const isAuthenticated = () => {
    return !!getToken();
};

const AuthenticatedRoute = (props) => {
    let {component: Component, ...rest} = props;

    return (
        <Route {...rest} render={props => (
            isAuthenticated() ? (
                <Component {...props}/>
            ) : (
                <Redirect to={{
                    pathname: '/login',
                    state: {from: props.location}
                }}/>
            )
        )}/>
    );
};

export default AuthenticatedRoute;