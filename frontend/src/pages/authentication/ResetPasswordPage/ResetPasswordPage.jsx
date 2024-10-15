import React, { useState } from "react";
import { useParams } from "react-router-dom";
import '../authentication.css';
import { handleFormSubmit } from "../../../utils/formHandlers";

// templates and layouts
import MainLayout from '../../../components/Layout/MainLayout/MainLayout';
import FormTemplate from "../../../components/Layout/FormTemplate/FormTemplate";

// components
import InputField from "../../../components/InputField";
import Button from "../../../components/Button";
import ErrorMessage from "../../../components/ErrorMessage";

const ResetPasswordPage = () => {
    const { userId, token } = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleResetPassword = async(e) => {
        if (password != confirmPassword) {
            setError("Passwords do not match");
        }

        setLoading(true);

        await handleFormSubmit({
            e,
            apiUrl: `/api/users/${userId}/password?token=${token}`,
            method: 'PUT',
            body: {password},
            onSuccess: () => {
                setSuccess(true);
            },
            onError: setError,
        });

        setLoading(false);
    };

    if (success) {
        return (
            <MainLayout>
                <FormTemplate 
                    title="Reset Password"
                    paragraphContent='Successfully reset password. Head back
                    to the login page to login'
                    formContent={
                        <>
                            <hr className="form-divider" />
                            <Button className="full-width" text="Back to login" onClick={() => window.location.href = '/'} />
                        </>
                    }
                />
            </MainLayout>
        );
    };

    return (
        <MainLayout>
            <FormTemplate 
                title="Reset Password"
                formContent={
                    <form onSubmit={handleResetPassword}>
                        <div className="form-input-components">
                            <InputField 
                                label="New Password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter new password"
                                required
                            />
                            <InputField 
                                label="Confirm Password"
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm new password"
                                required
                            />
                        </div>
                        <hr className="form-divider" />
                        <Button className="full-width" text={loading ? "Resetting..." : "Reset Password"} disabled={loading} />
                        <ErrorMessage message={error} />
                    </form>
                }
            />
        </MainLayout>
    );
};

export default ResetPasswordPage;