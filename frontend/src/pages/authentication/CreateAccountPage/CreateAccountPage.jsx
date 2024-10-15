import React, { useState } from "react";
import '../authentication.css';
import { handleFormSubmit } from "../../../utils/formHandlers";

// templates and layouts
import LoginLayout from '../../../components/Layout/LoginLayout/LoginLayout';
import FormTemplate from "../../../components/Layout/FormTemplate/FormTemplate";

// components
import InputField from "../../../components/InputField";
import Button from "../../../components/Button";
import ErrorMessage from "../../../components/ErrorMessage";


const CreateAccountPage = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false)

    const handleSignup = async(e) => {
        setLoading(true);
        await handleFormSubmit({
            e,
            apiUrl: 'api/users/',
            body: { email, username, password },
            onSuccess: () => {
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
                    paragraphContent='Account successfully created. Head back to the login page to login'
                    formContent={
                        <>
                            <hr className="form-divider" />
                            <Button text="Back to Login" onClick={() => window.location.href = '/'} />
                        </>
                    }
                />
            </LoginLayout>
        )
    }

    else {
        return (
            <LoginLayout>
                <FormTemplate 
                    formContent={
                        <form onSubmit= { handleSignup }>
                            <div className="form-input-components">
                                <InputField 
                                    label="Email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="Type your email"
                                    required
                                />
                                <InputField 
                                    label="Username"
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="Type your username"
                                    required
                                />
                                <InputField 
                                    label="Password"
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Type your password"
                                    required
                                />
                            </div>
                            <hr className="form-divider" />
                            <Button text={loading ? "Creating Account..." :  "Sign Up Now"} disabled={loading} />
                            <ErrorMessage message={error} />
                        </form>
                    }
                    footerContent={
                        <p>Have an account? <a href="/">Login</a></p>
                    }
                />
            </LoginLayout>
        )
    };
};

export default CreateAccountPage;