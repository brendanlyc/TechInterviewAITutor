// src/components/ErrorMessage.js
import React from 'react';
import PropTypes from 'prop-types';
import './components.css';


const ErrorMessage = ({ message }) => {
  return message ? <p className="form-template-error">{message}</p> : null;
};

ErrorMessage.propTypes = {
  message: PropTypes.string,
};

export default ErrorMessage;
