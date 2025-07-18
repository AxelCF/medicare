import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useAxios from "../hooks/useAxios";

export default function AgendaPatient() {
  const { id } = useParams(); // id du médecin
  const axiosInstance = useAxios();
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axiosInstance.get(`/agenda/?medecin=${id}`).then((res) => {
      setSlots(res.data);
      setLoading(false);
    });
  }, [id]);

  const handleBooking = async (date) => {
    try {
      await axiosInstance.post("/rendezvous/", {
        medecin: id,
        motif: "Consultation", // ou un champ à demander
        disponibilite: null, // à adapter si nécessaire
        date,
      });
      alert("Rendez-vous pris !");
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la réservation.");
    }
  };

  if (loading) return <p className="text-center">Chargement de l’agenda...</p>;

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h2 className="text-2xl font-bold mb-4 text-center text-blue-800">Agenda du médecin</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {slots.map((slot) => (
          <button
            key={slot.date}
            onClick={() => handleBooking(slot.date)}
            disabled={slot.is_booked}
            className={`p-2 border rounded ${
              slot.is_booked ? "bg-gray-300 text-gray-600 cursor-not-allowed" : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
          >
            {new Date(slot.date).toLocaleString("fr-FR", {
              weekday: "short",
              hour: "2-digit",
              minute: "2-digit",
              day: "numeric",
              month: "short",
            })}
          </button>
        ))}
      </div>
    </div>
  );
}
