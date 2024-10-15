import React from 'react';
import PropTypes from 'prop-types';
import './components.css';

const Button = ({ text, type, onClick, disabled, className }) => {
    return (
        <button 
            type={type}
            onClick={onClick}
            className={`button ${className}`}
            disabled={disabled}
        >
            {text}
        </button>
    )
};

Button.propTypes = {
    text: PropTypes.string.isRequired,
    onClick: PropTypes.func,
    disabled: PropTypes.bool
};

Button.defaultProps = {
    onClick: () => {},
    disabled: false,
    type: "submit"
};

export default Button;