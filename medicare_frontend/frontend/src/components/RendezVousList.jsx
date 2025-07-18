import React, { useEffect, useState } from "react";
import useAxios from "../hooks/useAxios";

export default function RendezVousList() {
  const axiosInstance = useAxios();
  const [rendezvous, setRendezvous] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axiosInstance
      .get("rendezvous/")
      .then((res) => {
        setRendezvous(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur chargement rendez-vous", err);
        setLoading(false);
      });
  }, []);

  if (loading)
    return <p className="text-center text-blue-600">Chargement...</p>;

  if (rendezvous.length === 0) {
    return (
      <p className="text-center text-gray-500">Aucun rendez-vous trouvé.</p>
    );
  }

  const now = new Date();
  const rdvAVenir = rendezvous.filter((r) => new Date(r.date) > now);
  const rdvPasses = rendezvous.filter((r) => new Date(r.date) <= now);

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">
        Mes rendez-vous
      </h2>

      <h3 className="text-xl font-semibold mb-2 text-green-700">📅 À venir</h3>
      <ul className="mb-6 space-y-4">
        {rdvAVenir.map((rdv) => (
          <li key={rdv.id} className="border p-4 rounded shadow bg-green-50">
            <p><strong>Date :</strong> {new Date(rdv.date).toLocaleString()}</p>
            <p><strong>Motif :</strong> {rdv.motif}</p>
            <p><strong>Médecin :</strong> Dr. {rdv.medecin_name}</p>
          </li>
        ))}
      </ul>

      <h3 className="text-xl font-semibold mb-2 text-gray-600">🕓 Passés</h3>
      <ul className="space-y-4">
        {rdvPasses.map((rdv) => (
          <li key={rdv.id} className="border p-4 rounded shadow bg-gray-100">
            <p><strong>Date :</strong> {new Date(rdv.date).toLocaleString()}</p>
            <p><strong>Motif :</strong> {rdv.motif}</p>
            <p><strong>Médecin :</strong> Dr. {rdv.medecin_name}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
