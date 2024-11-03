import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../../components/Layout/MainLayout/MainLayout';
import './HomePage.css';
import NewTopicBox from "../../components/NewTopicBox";

//components //
import Button from "../../components/Button";

const HomePage = () => {
    const [learningPaths, setLearningPaths] = useState([]);
    const [showNewTopicBox, setShowNewTopicBox] = useState(false);
    const { userId, username } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (userId) {
            fetch(`api/learning_paths/user_id/${Number(userId)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error fetching learning paths - Please try again');
                }
                return response.json();
            })
            .then(data => {
                setLearningPaths(data);
            })
            .catch(error => {
                console.error(error.message);
            });
        }
    }, [userId]);

    const handleOpenCreateTopicBox = () => {
        setShowNewTopicBox(true);
    }

    const handleCloseCreateTopicBox = () => {
        setShowNewTopicBox(false);
    }

    const handleClick = (title) => {
        navigate(`/content/${userId}/${encodeURIComponent(title)}`)
    }
    
    return (
        <MainLayout className = "parent-container" fullWidth>
            <div className="home-page-container">
                <div className={`home-page-content-container ${showNewTopicBox ? 'blurred' : ''}`}>
                    <p className="learning-paths-welcome-statement">Welcome Back, {username}</p>
                    <h1 className="learning-paths-pick-topic-statement">Pick a learning path to continue</h1>
                    <div className="learning-paths-container">
                        {learningPaths.length == 0 ? (
                            <p className="no-learning-path-statement">No learning paths found. Click on 'Create New Topic'
                                to get started!
                            </p>) : (
                                <div className="learning-paths-list">
                                    {learningPaths.map(path => (
                                        <div key={path.id} className='learning-path-box'>
                                                <div className="learning-path-columns">
                                                    <div className="learning-path-column-left">
                                                        <h2 className="learning-path-title">{path.title}</h2>
                                                    </div>
                                                    <div className="learning-path-column-right">
                                                        <Button 
                                                            className="white-variant learning-path-variant"
                                                            text={path.completed ? "CONTINUE" : "REVISE"}
                                                            onClick={() => handleClick(path.title)}
                                                        />
                                                    </div>
                                                </div>

                                        </div>
                                    ))}
                                </div>)}

                        <button className="create-new-topic-button" onClick={handleOpenCreateTopicBox}>Create New Topic</button>
                        
                    </div>
                </div>
                {showNewTopicBox && 
                <NewTopicBox 
                    onClose={handleCloseCreateTopicBox} 
                    userId={userId} 
                />}
            </div>
        </MainLayout>
    );
};

export default HomePage;