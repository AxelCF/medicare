// frontend/src/hooks/useAxios.js
import axios from "axios";

export default function useAxios() {
  const API = import.meta.env.VITE_API_URL;
  const instance = axios.create({
    baseURL: API,
  });

  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem("access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  return instance;
}
