import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const fetchScenarios = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/scenarios`);
        return response.data;
    } catch (error) {
        console.error('Error fetching scenarios:', error);
        throw error;
    }
};

export const submitDecision = async (decision) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/decisions`, decision);
        return response.data;
    } catch (error) {
        console.error('Error submitting decision:', error);
        throw error;
    }
};