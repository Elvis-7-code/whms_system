import apiClient from "../api/client";

export const getAll = (params) =>
  apiClient.get("/animals", { params });

export const getById = (id) =>
  apiClient.get(`/animals/${id}`);

export const create = (payload) =>
  apiClient.post("/animals", payload);

export const update = (id, payload) =>
  apiClient.put(`/animals/${id}`, payload);

export const remove = (id) =>
  apiClient.delete(`/animals/${id}`);