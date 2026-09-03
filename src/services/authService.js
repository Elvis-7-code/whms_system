import apiClient from '../api/client';

export const authService = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  signup: (payload) => apiClient.post('/auth/signup', payload),
  getCurrentUser: () => apiClient.get('/auth/me'),
  logout: () => apiClient.post('/auth/logout'),
};

export default authService;