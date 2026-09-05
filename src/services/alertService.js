import apiClient from '../api/client';

export const alertService = {
  getAll: (params) => apiClient.get('/alerts', { params }),
  markRead: (id) => apiClient.patch(`/alerts/${id}/read`),
  markAllRead: () => apiClient.patch('/alerts/read-all'),
};

export default alertService;