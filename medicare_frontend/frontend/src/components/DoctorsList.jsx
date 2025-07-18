import React, { useEffect, useState } from "react";
import useAxios from "../hooks/useAxios";
import { useNavigate } from "react-router-dom";

export default function DoctorsList() {
  const axiosInstance = useAxios();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    axiosInstance
      .get("medecins/")
      .then((res) => {
        setDoctors(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-blue-600 text-xl font-semibold">Chargement...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">
        Nos médecins disponibles
      </h2>
      {doctors.length === 0 ? (
        <p className="text-center text-gray-500">Aucun médecin disponible.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {doctors.map((doc) => (
            <div
              key={doc.id}
              className="border rounded-lg p-4 shadow hover:shadow-lg transition"
            >
              <h3 className="text-lg font-semibold text-gray-800">
                Dr. {doc.user.first_name} {doc.user.last_name}
              </h3>
              <p className="text-sm text-gray-600">
                Spécialité : {doc.specialty || "Non spécifiée"}
              </p>
              <button
                onClick={() => navigate(`/agenda/${doc.id}`)}
                className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Prendre RDV
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
