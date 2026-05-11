import apiClient from './apiClient';

const API_BASE_URL = 'http://localhost:8008/api';

export const fetchScenarios = async () => {
    try {
        const response = await apiClient.get(`${API_BASE_URL}/scenarios`);
        return response.data;
    } catch (error) {
        console.error('Error fetching scenarios:', error);
        throw error;
    }
};

export const submitDecision = async (decision) => {
    try {
        const response = await apiClient.post(`${API_BASE_URL}/decisions`, decision);
        return response.data;
    } catch (error) {
        console.error('Error submitting decision:', error);
        throw error;
    }
};