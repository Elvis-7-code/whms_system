import apiClient from '../api/client';

export const vaccinationService = {
  getAll: (params) => apiClient.get('/vaccinations', { params }),
  getDue: () => apiClient.get('/vaccinations/due'),
  markDone: (id) => apiClient.patch(`/vaccinations/${id}/mark-done`),
  create: (payload) => apiClient.post('/vaccinations', payload),
};

export default vaccinationService;