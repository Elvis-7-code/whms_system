import apiClient from '../api/client';

export const breedingService = {
  getAll: (params) => apiClient.get('/breeding-records', { params }),
  getById: (id) => apiClient.get(`/breeding-records/${id}`),
  create: (payload) => apiClient.post('/breeding-records', payload),
  update: (id, payload) => apiClient.put(`/breeding-records/${id}`, payload),
  remove: (id) => apiClient.delete(`/breeding-records/${id}`),
  getUpcomingBirths: () => apiClient.get('/breeding-records/upcoming-births'),
};

export default breedingService;