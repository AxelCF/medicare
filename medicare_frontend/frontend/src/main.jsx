import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.jsx";
import Login from "./components/Login";
import Profile from "./components/Profile";
import RendezVousList from "./components/RendezVousList";
import DisponibilitesList from "./components/DisponibilitesList";
import DoctorsList from "./components/DoctorsList";
import AgendaPatient from "./components/Agenda";
import AgendaMedecin from "./components/AgendaMedecin";
import Register from "./components/Register";
import PrivateRoute from "./components/PrivateRoute";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route index element={<DoctorsList />} />
        <Route path="doctors" element={<DoctorsList />} />
        <Route path="register" element={<Register />} /> {/* <- accès libre */}
        {/* ✅ Pages protégées */}
        <Route
          path="profile"
          element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          }
        />
        <Route
          path="rendezvous"
          element={
            <PrivateRoute>
              <RendezVousList />
            </PrivateRoute>
          }
        />
        <Route
          path="disponibilites/:id"
          element={
            <PrivateRoute>
              <DisponibilitesList />
            </PrivateRoute>
          }
        />
        <Route
          path="agenda/:id"
          element={
            <PrivateRoute>
              <AgendaPatient />
            </PrivateRoute>
          }
        />
        <Route
          path="mon-agenda"
          element={
            <PrivateRoute>
              <AgendaMedecin />
            </PrivateRoute>
          }
        />
      </Route>

      {/* Page de connexion */}
      <Route path="/login" element={<Login />} />
    </Routes>
  </BrowserRouter>
);
