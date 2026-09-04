import apiClient from '../api/client.js';

// TODO: point this at the real backend once it exists, e.g. a
// POST /api/public/contact route that emails/notifies the farm owner.
// This endpoint should NOT require auth — it's a public inquiry form.

export async function sendContactMessage(payload) {
  const { data } = await apiClient.post('/public/contact', payload);
  return data;
}