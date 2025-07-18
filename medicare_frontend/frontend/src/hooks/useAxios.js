// frontend/src/hooks/useAxios.js
import axios from "axios";

export default function useAxios() {
  const instance = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
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
