import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  const isLoggedIn = !!localStorage.getItem("access_token");

  return (
    <nav className="bg-blue-600 text-white px-8 py-4 flex justify-between items-center">
      <div className="font-bold text-lg">
        <Link to="/">MediCare</Link>
      </div>

      <div className="space-x-4">
        {isLoggedIn ? (
          <>
            <Link to="/profile" className="hover:underline">
              Mon profil
            </Link>
            <Link to="/rendezvous" className="hover:underline">
              Mes RDV
            </Link>
            <Link to="/doctors" className="hover:underline">
              Médecins
            </Link>
            <button
              onClick={handleLogout}
              className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-100"
            >
              Déconnexion
            </button>
          </>
        ) : (
          <Link
            to="/login"
            className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-100"
          >
            Connexion
          </Link>
        )}
      </div>
    </nav>
  );
}
