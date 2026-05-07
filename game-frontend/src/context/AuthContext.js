import React, { createContext, useState, useEffect } from 'react';
import { getMe, login, register, logout } from '../api/authApi';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      getMe(token)
        .then((userData) => setUser(userData))
        .catch(() => {
          setUser(null);
          setToken(null);
          localStorage.removeItem('token');
        });
    }
  }, [token]);

  const handleLogin = async (credentials) => {
    const data = await login(credentials);
    setToken(data.token);
    localStorage.setItem('token', data.token);
    const userData = await getMe(data.token);
    setUser(userData);
  };

  const handleRegister = async (userData) => {
    await register(userData);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider
      value={{ user, token, handleLogin, handleRegister, handleLogout }}
    >
      {children}
    </AuthContext.Provider>
  );
};