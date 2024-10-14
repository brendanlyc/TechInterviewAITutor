import React from "react";
import './LoginLayout.css';

const LoginLayout = ({children}) => {
    return (
        <div className="layout">
            <div className="tetor-logo">
                <img src="../../static/images/tetor-logo.png" alt="Tetor logo" />
                <span className="tetor-name">TETOR</span>
            </div>

            <div className="content-container">
                {children}
            </div>
        </div>
    );
};

export default LoginLayout;