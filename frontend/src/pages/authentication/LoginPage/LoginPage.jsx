import React from "react";
import { useState } from "react";
import '../authentication.css';
import { useAuth } from '../../../context/AuthContext';
import LoginLayout from '../../../components/Layout/LoginLayout';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { setAuthState } = useAuth();
 
    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    password
                })
            })

            if (!response.ok) {
                const errorData = await response.json()  
                throw new Error(errorData.detail || 'Login failed');
            }

            const data = await response.json()  

            setAuthState({
                token: data.token,
                userId: data.userId,
                username: data.username
            })
            
            console.log("Login successful!")
            //navigate('/home')

        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    }

    console.log(error)


    return (
        <LoginLayout>
            <div className="login-container">
                <div className="login-card">
                    <form onSubmit={ handleLogin }>
                        <div className="login-form-component">
                            <label>Username</label>
                            <input 
                                type="username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Type your username"
                                required
                            />
                            <label>Password</label>
                            <input 
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Type your password"
                                required
                            />
                        </div>

                        {error && <p className="login-error-message">{error}</p>}

                        <button type="submit" className="login-submit-button">
                            Login
                        </button>
                    </form>
                    <p className="create-account-login-redirect-line">
                        Don't have an account? <a href="/create-account">Sign Up</a>
                    </p>
                </div>
            </div>
        </LoginLayout>
    );
};

export default LoginPage;