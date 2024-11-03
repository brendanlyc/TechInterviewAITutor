import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import './MainLayout.css';
import { useAuth } from '../../../context/AuthContext';
import SettingsIcon from "../../../static/images/SettingsIcon.png";
import tetorLogo from "../../../static/images/tetor-logo.png";

const MainLayout = ({children, contentFullWidth = false}) => {
    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    const handleNavigateToSettings = () => {
        console.log("Navigating to settings")
        //navigate("/settings");
    };

    return (
        <div className="layout">
            <div className="header">
                <div className="tetor-logo">
                    <img className="tetor-logo-pic" src={tetorLogo} alt="Tetor logo" />
                    <span className="tetor-name">TETOR</span>

                </div>
                {isAuthenticated && <img className="settings-icon" src={SettingsIcon} alt="Settings Button" onClick={handleNavigateToSettings} />}
            </div>

            <div className={`content-container ${contentFullWidth ? 'full-width' : ''}`}>
                {children}
            </div>
        </div>
    );
};

export default MainLayout;