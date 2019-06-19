import React from 'react';

import {Redirect} from 'react-router';
import {clearToken} from "../../utils/storage";

export default () => {
    clearToken();
    return <Redirect to="/login"/>;
};