// frontend/src/api.js
import axios from 'axios';

// Import the URL from the environment variable
const baseURL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: baseURL, 
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor: Automatically add the token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;