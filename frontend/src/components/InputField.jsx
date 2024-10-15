import React from 'react';
import PropTypes from 'prop-types';
import './components.css';

const InputField = ({ label, type, value, onChange, placeholder, required}) => {
    return (
        <div className="input-field-container">
            {label && <label className="input-field-label">{label}</label>}
            <input 
                className="input-field"
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                required={required}
            />
        </div>
    );
};

InputField.propTypes = {
    label: PropTypes.string,
    type: PropTypes.string,
    value: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    placeholder: PropTypes.string,
    required: PropTypes.bool
}

InputField.defaultProps = {
    type: 'text',
    placeholder: '',
    required: false
}

export default InputField;