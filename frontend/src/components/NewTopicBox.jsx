import React, { useState } from 'react';
import FormTemplate from './Layout/FormTemplate/FormTemplate';
import BackLogo from "../static/images/BackLogo.png";
import InputField from './InputField';
import Button from './Button';
import './components.css';

const NewTopicBox = ({ onClose }) => {
    const [topicTitle, setTopicTitle] = useState('');
    const [topicExperience, setTopicExperience] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCreateTopic = () => {
        // Need to add API logic here
        setLoading(true);
        setLoading(false);
    }

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
                            <label className="text-area-label" htmlFor="experience">How much experience do you have with this topic?</label>
                            <textarea 
                                id="experience"
                                name="experience"
                                value={topicExperience}
                                placeholder="Describe how much experience you have had with this topic here"
                                onChange={e => setTopicExperience(e.target.value)}
                            />
                        </div>
                        <Button text={loading ? 'Creating topic...' : "Create Topic"} disabled={loading} />
                    </form>
                    }
                    className="popup"
                /> 
            </div>
        </div>
    );
};

export default NewTopicBox;