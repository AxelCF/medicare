// frontend/src/api.js
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL;

const API = axios.create({
  baseURL: `${API_BASE_URL}/api/`, // on garde /api/ si l’API Django est sous ce chemin
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;
