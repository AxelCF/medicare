import React, { useEffect, useState } from "react";
import useAxios from "../hooks/useAxios";

export default function MesRendezVousMedecin() {
  const axiosInstance = useAxios();
  const [rendezvous, setRendezvous] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axiosInstance.get("/rendezvous/")
      .then((res) => {
        setRendezvous(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur récupération RDV médecin :", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center text-blue-600">Chargement...</p>;

  if (rendezvous.length === 0)
    return <p className="text-center text-gray-500">Aucun rendez-vous à venir.</p>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-blue-800 text-center mb-6">Mes rendez-vous avec des patients</h2>
      <ul className="space-y-4">
        {rendezvous.map((rdv) => (
          <li key={rdv.id} className="border p-4 rounded shadow bg-white">
            <p><strong>Patient :</strong> {rdv.patient}</p>
            <p><strong>Date :</strong> {new Date(rdv.date).toLocaleString("fr-FR")}</p>
            <p><strong>Motif :</strong> {rdv.motif}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
