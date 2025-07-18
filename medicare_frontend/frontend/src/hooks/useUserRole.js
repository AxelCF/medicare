// src/hooks/useUserRole.js
import { jwtDecode } from "jwt-decode";

export default function useUserRole() {
  const token = localStorage.getItem("access_token");

  if (!token) return null;

  try {
    const decoded = jwtDecode(token);
    return decoded.role || null;
  } catch (error) {
    console.error("Erreur décodage token:", error);
    return null;
  }
}
