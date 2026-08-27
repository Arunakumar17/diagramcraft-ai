import axios from 'axios';

const API_BASE_URL = '/api';

export const api = {
    // Generate diagram from prompt
    generateDiagram: async (diagramType, prompt) => {
        const response = await axios.post(`${API_BASE_URL}/generate`, {
            diagram_type: diagramType,
            prompt: prompt
        });
        return response.data;
    },

    // Get diagram by ID
    getDiagram: async (diagramId) => {
        const response = await axios.get(`${API_BASE_URL}/diagram/${diagramId}`);
        return response.data;
    },

    // Get diagram history
    getHistory: async (limit = 20) => {
        const response = await axios.get(`${API_BASE_URL}/history?limit=${limit}`);
        return response.data;
    },

    // Delete diagram
    deleteDiagram: async (diagramId) => {
        const response = await axios.delete(`${API_BASE_URL}/diagram/${diagramId}`);
        return response.data;
    },

    // Health check
    healthCheck: async () => {
        const response = await axios.get(`${API_BASE_URL}/health`);
        return response.data;
    }
};
