import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import './ContentPage.css';
import BackLogo from "../../static/images/BackLogo.png";

// templates and layouts
import MainLayout from '../../components/Layout/MainLayout/MainLayout';
import Button from "../../components/Button";

const ContentPage = () => {
    const { userId, title } = useParams();
    const [loading, setLoading] = useState(false);
    const [questions, setQuestions] = useState([]);
    const [chatMessages, setChatMessages] = useState([]);
    const [processingMessage, setProcessingMessage] = useState(false);
    const [diagnosticTestResponses, setDiagnosticTestResponses] = useState({});
    const [toggleChatbot, setToggleChatbot] = useState(false);
    const [evaluatingDiagnosticTest, setEvaluatingDiagnosticTest] = useState(false);
    const [message, setMessage] = useState("");
    const navigate = useNavigate();
    const chatWindowRef = useRef(null);
    // const chatMessagesRef = useRef([]);

    const fetchAITutorResponse = async () => {
        try {
            const response = await fetch(`/api/ai_tutor/${userId}/${encodeURIComponent(title)}`);
            if (response.ok) {
                const aiResponse = await response.json();

                setChatMessages(prevMessages => [
                    ...prevMessages,
                    {sender: "tutor", message: aiResponse}
                ]);

            } else {
                throw new Error("Failed to fetch AI tutor response")
            }
        } catch (error) {
            console.error("Error fetching AI tutor response:", error);
        }
    }

    useEffect(() => {
        const loadLearningPath = async() => {
            try {
                setLoading(true);
                const response = await fetch(`/api/learning_paths/load/learning_path/${userId}/${encodeURIComponent(title)}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/JSON'
                    }
                });

                if (!response.ok) {
                    throw new Error("Failed to load learning path content and diagnostic test");
                }

                const data = await response.json();
                
                setQuestions(data.diagnostic_test.questions || []);
                setChatMessages(data.learning_path_content.chat_history || []);
                setDiagnosticTestResponses(data.diagnostic_test.questions.reduce((acc, _, index) => {
                    acc[index] = "";
                    return acc;
                },{}));

                const resultResponse = await fetch(`/api/diagnostic_test_result/user/${userId}/learning_path/${encodeURIComponent(title)}`);
                console.log(resultResponse.status)
                console.log(resultResponse)
                if (resultResponse.ok) {
                    setToggleChatbot(true);
                } else if (resultResponse.status === 404) {
                    console.log("Diagnostic Test Result not found");
                } else {
                    throw new Error("Failed to fetch diagnostic test result");
                }
                if (data.learning_path_content.chat_history.length === 0 && resultResponse.ok) {
                    await fetchAITutorResponse();
                }

            } catch (error) {
                console.error("Error loading learning path:", error)
            } finally {
                setLoading(false);
            }
        };
        
        loadLearningPath();
    },[userId, title]);

    // useEffect(() => {
    //     const handleUnload = () => {
    //         saveChatHistory();
    //     }

    //     window.addEventListener("beforeunload",handleUnload);

    //     return () => {
    //         window.removeEventListener("beforeunload", handleUnload);
    //     };
    // }, [chatMessages]);

    const saveChatHistory = async (new_message) => {
        try {
            console.log("Saving...")
            const url = `/api/learning_paths/save_chat/${userId}/${encodeURIComponent(title)}`;
            const data = JSON.stringify(new_message);
            console.log(data);
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: data
            });

        } catch (error) {
            console.error("Error saving chat history:", error);
        }
    };

    const handleProceed = async () => {
        setLoading(true);
        setEvaluatingDiagnosticTest(true);
        console.log("Consolidated Responses:", diagnosticTestResponses);
        const url = `/api/diagnostic_test/evaluate/user/${userId}/learning_path/${encodeURIComponent(title)}`;
        const data = JSON.stringify(diagnosticTestResponses);
        console.log(data);
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: data
        });
        setEvaluatingDiagnosticTest(false);
        setLoading(false);
        setToggleChatbot(true);
        await fetchAITutorResponse();
    }

    const handleSendMessage = async () => {
        setProcessingMessage(true);
        if (message.trim()) {
            console.log("User Message:", message);
            const new_message = {
                sender: "user",
                message: message,
                timestamp: new Date().toISOString()
            }
            setChatMessages(prevMessages => [
                ...prevMessages,
                new_message
                ]);
            setMessage("");
            await saveChatHistory(new_message);
            await fetchAITutorResponse();
            setProcessingMessage(false);
        }
    }

    // useEffect(() => {
    //     console.log(chatMessages);
    //     chatMessagesRef.current = chatMessages;
    // }, [chatMessages]);

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [chatMessages]);


    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey && processingMessage === false) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <MainLayout>
            <div className="content-page-container"> 
                <div className="content-container">
                    <div onClick={() => navigate("/home")} className='back-button'>
                        <img className="back-logo" src={BackLogo} alt="Back logo" />
                        <span className="back-name">Back</span>
                    </div>
                    <h1 className="content-page-header">{title}</h1>
                    
                    {!toggleChatbot ? (
                        <>
                            <h2 className="content-page-header">Diagnostic Test</h2>

                            {loading ? (
                                <div className="loading-container">
                                    <div className="spinner"></div>
                                    {evaluatingDiagnosticTest ? (
                                        <p>Please wait while we evaluate your diagnostic test...</p>
                                    ) : (
                                        <p>Loading content...</p>  
                                    )}
                                </div>
                            ) : (
                                <>
                                    <div className="questions-container">
                                        {questions.map((question,index) => (
                                            <>
                                                <div key={index} className="question-item">
                                                    <p style={{ whiteSpace: 'pre-wrap' }} className="question-text">{index+1}. {question.question}</p>
                                                </div>
                                                {question.provided_data_schemas?.example_input && (
                                                    <div className="question-example">
                                                        <p style={{ whiteSpace: 'pre-wrap' }}><b>Sample Input:</b> {question.provided_data_schemas.example_input}</p>
                                                    </div>
                                                )}
                                                {question.provided_data_schemas?.example_output && (
                                                    <div className="question-example">
                                                        <p style={{ whiteSpace: 'pre-wrap' }}><b>Sample Output:</b> {question.provided_data_schemas.example_output}</p>
                                                    </div>
                                                )}
                                                <textarea
                                                    placeholder="Enter your answer here..."
                                                    className="answer-input"
                                                    // value={diagnosticTestResponses[index] || ''}
                                                    onChange={(e) => setDiagnosticTestResponses(prev => ({ ...prev, [index]: e.target.value}))}
                                                />
                                            </>
                                        ))}
                                    </div>
                                    <div className="content-page-button-section">
                                        <Button
                                            onClick={handleProceed}
                                            text="Proceed"
                                            className="proceed-button"
                                        />                                
                                    </div>
                                </>
                                )}
                        </>
                    ) : (
                        <>
                            <div className="chat-window" ref={chatWindowRef}>
                                {
                                    chatMessages.map((item, index) => (
                                        <div key={index} style={{ whiteSpace: 'pre-wrap' }} className={`chat-message ${item.sender === "user" ?
                                            "user-message" : "tutor-message"}`}>
                                                {item.message}
                                        </div>
                                    ))
                                }
                                <div className="chat-input-container">
                                    <textarea
                                        type="text"
                                        placeholder="Message Tutor"
                                        className="chat-input"
                                        rows="1"
                                        value={message}
                                        onChange={(e) => setMessage(e.target.value)}
                                        onKeyDown={handleKeyPress}
                                        onInput={(e) => {
                                            e.target.style.height = 'auto';
                                            e.target.style.height = `${e.target.scrollHeight}px`;
                                        }}
                                    />
                                    <button 
                                        className={`send-chat-button ${processingMessage ? "disabled" : ""}`} 
                                        onClick={handleSendMessage}
                                        disabled={processingMessage}
                                    >
                                        ⬆
                                    </button>
                                </div>
                            </div>                        
                        </>

                    )
                        
                    }
                </div>
            </div>
        </MainLayout>
    )
};


export default ContentPage;