import apiClient from '../api/client';

export const reportService = {
  getSalesSummary: (params) => apiClient.get('/reports/sales-summary', { params }),
  getHerdOverview: (params) => apiClient.get('/reports/herd-overview', { params }),
  exportReport: (type, params) =>
    apiClient.get(`/reports/${type}/export`, { params, responseType: 'blob' }),
};

export default reportService;