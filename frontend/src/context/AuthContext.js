// src/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const storedUserId = localStorage.getItem('userId')
    const storedUsername = localStorage.getItem('username')
    if (token && storedUserId && storedUsername) {
      setIsAuthenticated(true);
      setUserId(storedUserId);
      setUsername(storedUsername);
    }
  }, []);

  const setAuthState = ({ token, userId, username }) => {
    localStorage.setItem('authToken', token);
    localStorage.setItem('userId', userId);
    localStorage.setItem('username', username);
    setIsAuthenticated(true);
    setUserId(userId);
    setUsername(username);
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setUserId(null);
    setUsername('');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, userId, username, setAuthState, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
