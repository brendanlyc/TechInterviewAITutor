import React from "react";
import './LoginLayout.css';
import tetorLogo from "../../../static/images/tetor-logo.png";

const LoginLayout = ({children}) => {
    return (
        <div className="layout">
            <div className="tetor-logo">
                <img className="tetor-logo-pic" src={tetorLogo} alt="Tetor logo" />
                <span className="tetor-name">TETOR</span>
            </div>

            <div className="content-container">
                {children}
            </div>
        </div>
    );
};

export default LoginLayout;