import axios from 'axios';

// This is THE seam between frontend and backend.
// Once a backend is chosen, only VITE_API_BASE_URL (in .env) needs to change.
// Every service file (src/services/*) should import `apiClient` from here
// rather than calling axios directly, so auth/error handling stays centralized.

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach the auth token (if present) to every outgoing request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Centralized error handling — e.g. auto-logout on 401.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      // TODO: redirect to login once router-level logout hook exists
    }
    return Promise.reject(error);
  },
);

export default apiClient;