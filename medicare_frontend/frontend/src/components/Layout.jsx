import React from "react";
import { Outlet, Link, useNavigate } from "react-router-dom";

export default function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* NAVBAR */}
      <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
        <div className="text-xl font-bold text-blue-700">
          <Link to="/">Medicare</Link>
        </div>
        <div className="space-x-4">
          <Link to="/doctors" className="text-gray-700 hover:text-blue-600">
            Médecins
          </Link>
          <Link to="/rendezvous" className="text-gray-700 hover:text-blue-600">
            Mes rendez-vous
          </Link>
          <Link to="/profile" className="text-gray-700 hover:text-blue-600">
            Profil
          </Link>
          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-700 font-medium"
          >
            Déconnexion
          </button>
        </div>
      </nav>

      {/* CONTENU */}
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
