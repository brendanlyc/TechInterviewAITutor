import React, { useState } from "react";
import '../authentication.css';
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom'
import LoginLayout from '../../../components/Layout/LoginLayout';


const CreateAccountPage = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
 
    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            setError('');

            const response = await fetch('/api/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    username,
                    password
                })
            })

            if (!response.ok) {
                const errorData = await response.json()  
                throw new Error(errorData.detail || 'Failed to create an account');
            }

            const data = await response.json()  
            
            //navigate('/signup-success')

        } catch (err) {
            setError(err.message);
            console.error(err);
        }
    }

    console.log(error)


    return (
        <LoginLayout>
            <div className="create-account-container">
                <div className="create-account-card">
                    <form onSubmit={ handleSignup }>
                        <div className="create-account-form-component">
                            <label>Email</label>
                            <input 
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Type your email"
                                required
                            />
                            <label>Username</label>
                            <input 
                                type="text"
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

                        {error && <p className="create-account-error-message">{error}</p>}

                        <button type="submit" className="create-account-submit-button">
                            Sign Up Now
                        </button>
                    </form>
                    <p className="create-account-login-redirect-line">
                        Have an account? <a href="/">Login</a>
                    </p>
                </div>
            </div>
        </LoginLayout>
    );
};

export default CreateAccountPage;