import apiClient from '../api/client';

export const animalService = {
  getAll: (params) => apiClient.get('/animals', { params }),
  getById: (id) => apiClient.get(`/animals/${id}`),
  create: (payload) => apiClient.post('/animals', payload),
  update: (id, payload) => apiClient.put(`/animals/${id}`, payload),
  remove: (id) => apiClient.delete(`/animals/${id}`),
};

export default animalService;