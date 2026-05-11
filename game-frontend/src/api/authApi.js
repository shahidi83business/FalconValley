import apiClient from './apiClient';

const API_URL = 'http://127.0.0.1:8008/api/auth';

export const register = async (userData) => {
  const response = await apiClient.post(`${API_URL}/register`, userData);
  return response.data;
};

export const login = async (credentials) => {
  const response = await apiClient.post(`${API_URL}/login`, credentials);
  return response.data;
};

export const getMe = async (token) => {
  const response = await apiClient.get(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const logout = async () => {
  // If logout requires an API call, implement it here
  return { message: 'Logged out successfully!' };
};

export const forgotPassword = async (email) => {
  const response = await apiClient.post(`${API_URL}/forgot-password`, { email });
  return response.data;
};

export const resetPassword = async (token, newPassword) => {
  const response = await apiClient.post(`${API_URL}/reset-password`, {
    token,
    new_password: newPassword,
  });
  return response.data;
};