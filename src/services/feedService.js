import apiClient from '../api/client';

export const feedService = {
  getLevels: () => apiClient.get('/feed/levels'),
  addStock: (payload) => apiClient.post('/feed/stock', payload),
  logFeeding: (payload) => apiClient.post('/feed/log', payload),
  getFeedingTasksToday: () => apiClient.get('/feed/tasks/today'),
};

export default feedService;