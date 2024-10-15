import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../../components/Layout/MainLayout/MainLayout';
import './HomePage.css';
import InputField from '../../components/InputField';
import FormTemplate from '../../components/Layout/FormTemplate/FormTemplate';
import NewTopicBox from "../../components/NewTopicBox";

const HomePage = () => {
    const [learningPaths, setLearningPaths] = useState([]);
    const [showNewTopicBox, setShowNewTopicBox] = useState(false);
    const { userId, username } = useAuth();

    useEffect(() => {
        fetch(`/api/learning_paths/${userId}`)
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
    }, []);

    const handleOpenCreateTopicBox = () => {
        setShowNewTopicBox(true);
    }

    const handleCloseCreateTopicBox = () => {
        setShowNewTopicBox(false);
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
                                        <div key={path.id} className={`learning-path-box 
                                            ${path.current_level > path.total_levels 
                                            ? 'learning-path-completed' : ''}`
                                            }>
                                                <div className="learning-path-columns">
                                                    <div className="learning-path-column-left">
                                                        <h2 className="learning-path-title">{path.title}</h2>
                                                        {path.current_level_title && <p className="learning-path-next-level">Next: {path.current_level_title}</p>}
                                                    </div>
                                                </div>
                                                <p className="learning-path-progress">
                                                    {path.current_level - 1 === path.total_levels 
                                                    ? 'Completed (100%)'
                                                    : `${path.current_level - 1}/${path.total_levels} Done (${(((path.current_level - 1) / path.total_levels) * 100).toFixed(1)}%)`}
                                                </p>
                                        </div>
                                    ))}
                                </div>)}

                        {/* // <div className="learning-paths-list">
                        //     <div className="learning-path-box">
                        //             <div className="learning-path-columns">
                        //                 <div className="learning-path-column-left">
                        //                     <h2 className="learning-path-title">Two Pointer</h2>
                        //                     <p className="learning-path-next-level">Next: Two Pointers with Multiple Arrays</p>
                        //                 </div>
                        //             </div>
                        //         <p className="learning-path-progress">{'3/6 Done (50%)'}</p>
                        //     </div>

                        //     <div className="learning-path-box learning-path-completed">
                        //         <div className="learning-path-columns">
                        //             <div className="learning-path-column-left">
                        //                 <h2 className="learning-path-title">Topological Sort</h2>
                        //             </div>
                        //         </div>
                        //         <p className="learning-path-progress">{'Completed (100%)'}</p>
                        //     </div>

                        //     <div className="learning-path-box learning-path-completed">
                        //         <div className="learning-path-columns">
                        //             <div className="learning-path-column-left">
                        //                 <h2 className="learning-path-title">Topological Sort</h2>
                        //             </div>
                        //         </div>
                        //         <p className="learning-path-progress">{'Completed (100%)'}</p>
                        //     </div>
                        // </div> */}

                        <button className="create-new-topic-button" onClick={handleOpenCreateTopicBox}>Create New Topic</button>
                        
                                                    {/* )
                        } */}
                    </div>
                </div>
                {showNewTopicBox && <NewTopicBox onClose={handleCloseCreateTopicBox} />}
            </div>
        </MainLayout>
    );
};

export default HomePage;