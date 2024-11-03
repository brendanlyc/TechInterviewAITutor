import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import FormTemplate from './Layout/FormTemplate/FormTemplate';
import BackLogo from "../static/images/BackLogo.png";
import InputField from './InputField';
import Button from './Button';
import './components.css';
import { handleFormSubmit } from "../utils/formHandlers"
import ErrorMessage from "./ErrorMessage";

const NewTopicBox = ({ onClose, userId }) => {
    const [topicTitle, setTopicTitle] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleCreateTopic = async(e) => {
        e.preventDefault();
        setLoading(true);

        await handleFormSubmit({
            e,
            apiUrl: 'api/learning_paths/',
            body: { user_id: Number(userId),
                    title: topicTitle,
                    },
            onSuccess: async () => {
                const fetchLearningPathId = await fetch(`/api/learning_paths/user_id/${userId}/learning_path_title/${topicTitle}`)
                if (!fetchLearningPathId.ok) {
                    setError("Failed to fetch learning path Id");
                    setLoading(false);
                    return;
                }

                const learningPathData = await fetchLearningPathId.json();
                const learningPathId = learningPathData.id;

                navigate(`/content/${userId}/${topicTitle}`);
            },
            onError: (errorMessage) => {
                setError(errorMessage);
                setLoading(false);
            },
        });
        setLoading(false);
    };

    return (
        <div className="new-topic-box">
            <div className="new-topic-box-container">
                <div onClick={onClose} className='back-button'>
                    <img className="back-logo" src={BackLogo} alt="Back logo" />
                    <span className="back-name">Back</span>
                </div>
                <FormTemplate
                    title="New Topic"
                    formContent={
                    <form onSubmit={handleCreateTopic}>
                        <div className="form-input-components">
                            <InputField
                                label="Topic Name"
                                type="text"
                                placeholder="Type your topic"
                                value={topicTitle}
                                onChange={e => setTopicTitle(e.target.value)}
                            />
                        </div>
                        <Button 
                            className="full-width"
                            text={loading ? 'Creating topic...' : "Create Topic"} 
                            disabled={loading} 
                        />
                        <ErrorMessage message={error} />
                    </form>
                    }
                    className="popup"
                /> 
            </div>
        </div>
    );
};

export default NewTopicBox;