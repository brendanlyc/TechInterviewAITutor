import React from 'react';
import PropTypes from 'prop-types';
import "./FormTemplate.css"

const FormTemplate= ({
    title,
    headerContent,
    paragraphContent,
    formContent,
    footerContent,
    className
}) => {
    return (
        <div className={`form-template-container ${className || ''}`}>
            {headerContent && <div className="form-header-content">{headerContent}</div>}
            {title && <h1>{title}</h1>}
            {paragraphContent && <div className="form-template-paragraph">{paragraphContent}</div>}
            {formContent && <div className="form-template-form">{formContent}</div>}
            {footerContent && <div className="form-template-footer-content">{footerContent}</div>}
        </div>
    )
}

FormTemplate.propTypes = {
    headerContent: PropTypes.node,
    title: PropTypes.string,
    paragraphContent: PropTypes.node,
    formContent: PropTypes.node,
    bottomContent: PropTypes.node,
  };

export default FormTemplate;

