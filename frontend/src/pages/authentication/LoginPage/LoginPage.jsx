import React, { useState} from "react";
import { Link, useNavigate } from "react-router-dom";
import '../authentication.css';
import { useAuth } from '../../../context/AuthContext';
import { handleFormSubmit } from "../../../utils/formHandlers";

// templates and layouts
import LoginLayout from '../../../components/Layout/LoginLayout/LoginLayout';
import FormTemplate from "../../../components/Layout/FormTemplate/FormTemplate";

// components
import InputField from "../../../components/InputField";
import Button from "../../../components/Button";
import ErrorMessage from "../../../components/ErrorMessage";

// styling


const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { setAuthState } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async(e) => {
        setLoading(true);
        await handleFormSubmit({
            e,
            apiUrl: 'api/auth/login',
            body: {username, password},
            onSuccess: (data) => {
                setAuthState({
                    token: data.token,
                    userId: data.userId,
                    username: data.username
                });
                navigate('/home');
            },
            onError: setError,
        });
        setLoading(false);
    };

    return (
        <LoginLayout>
            <FormTemplate 
                title="Login"
                formContent={
                    <form onSubmit={handleLogin}>
                        <div className="form-input-components">
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
                        <Button text={loading ? "Logging in..." : "Login"} disabled={loading} />
                        <ErrorMessage message={error} />
                    </form>
                }
                footerContent={
                    <>
                        <p><Link to="/reset-password">Forget password?</Link></p>
                        <p>Don't have an account? <Link to="/create-account">Sign Up</Link></p>
                    </>
                }
            />
        </LoginLayout>
    );
};

export default LoginPage;