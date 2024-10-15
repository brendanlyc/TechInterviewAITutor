import React, { useState } from "react";
import { Link } from "react-router-dom";
import '../authentication.css';
import { handleFormSubmit } from "../../../utils/formHandlers";

// templates and layouts
import LoginLayout from '../../../components/Layout/LoginLayout/LoginLayout';
import FormTemplate from "../../../components/Layout/FormTemplate/FormTemplate";

// components
import InputField from "../../../components/InputField";
import Button from "../../../components/Button";
import ErrorMessage from "../../../components/ErrorMessage";
import { Form } from "react-router-dom";

const ResetPasswordRequestPage = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleSendResetLink = async(e) => {
        setLoading(true);
        await handleFormSubmit({
            e,
            apiUrl: 'api/auth/request-reset-password',
            body: { email },
            onSuccess: (data) => {
                setSuccess(true);
            },
            onError: setError,
        });
        setLoading(false);
    };

    if (success) {
        return (
            <LoginLayout>
                <FormTemplate 
                    title='Reset Password'
                    paragraphContent='We have emailed you a link to reset your password. Please check your inbox.'
                    formContent= {
                        <>
                            <hr className="form-divider" />
                            <Button text="Back to Login" onClick={() => window.location.href = '/'} />
                        </>
                    }
                />
            </LoginLayout>
        )
    }

    return (
        <LoginLayout>
            <FormTemplate 
                title="Reset Password"
                paragraphContent="Enter the email you signed up with. We will email you a link to log in and reset your password."
                formContent={
                    <form onSubmit={handleSendResetLink}>
                        <div className="form-input-components">
                            <InputField 
                                    label="Email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="Type your email"
                                    required
                                />
                        </div>
                        <hr className="form-divider" />
                        <Button text={loading ? "Sending..." : "Send Link"} disabled={loading} />
                        <ErrorMessage message={error} />
                    </form>
                }
                footerContent={
                    <p>Don't have an account? <Link to="/create-account">Sign Up</Link></p>
                }
            />
        </LoginLayout>
    );
};

export default ResetPasswordRequestPage;