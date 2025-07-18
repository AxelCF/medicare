import React, { useEffect, useState } from "react";
import useAxios from "../hooks/useAxios";
import { useParams, useNavigate } from "react-router-dom";

export default function AgendaMedecin() {
  const { id } = useParams(); // ID du médecin
  const axiosInstance = useAxios();
  const navigate = useNavigate();

  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [motif, setMotif] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    axiosInstance
      .get(`/agenda/?medecin=${id}`)
      .then((res) => {
        setSlots(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await axiosInstance.post("/rendezvous/", {
        motif: motif,
        disponibilite: selectedSlot.id, // ⚠️ ID de la disponibilité
      });

      setMessage("✅ Rendez-vous réservé avec succès !");
      setSelectedSlot(null);
      setMotif("");
    } catch (err) {
      console.error(err);
      setMessage("❌ Erreur lors de la réservation.");
    }
  };

  if (loading) {
    return <p className="text-center text-blue-600">Chargement de l’agenda...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold text-blue-800 mb-6 text-center">
        Agenda du Médecin
      </h2>

      {message && <p className="text-center mb-4 text-green-600">{message}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {slots.map((slot) => (
          <button
            key={slot.date}
            disabled={slot.is_booked}
            onClick={() => setSelectedSlot(slot)}
            className={`border rounded p-2 text-sm ${
              slot.is_booked
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-white hover:bg-blue-100"
            } ${selectedSlot?.date === slot.date ? "border-blue-600" : ""}`}
          >
            {new Date(slot.date).toLocaleString("fr-FR", {
              dateStyle: "short",
              timeStyle: "short",
            })}
          </button>
        ))}
      </div>

      {selectedSlot && (
        <form onSubmit={handleSubmit} className="mt-6 bg-white p-4 rounded shadow">
          <h3 className="text-lg font-bold mb-2">Réserver ce créneau :</h3>

          <p className="mb-2 text-sm text-gray-700">
            {new Date(selectedSlot.date).toLocaleString("fr-FR", {
              dateStyle: "full",
              timeStyle: "short",
            })}
          </p>

          <input
            type="text"
            placeholder="Motif du rendez-vous"
            className="w-full border px-3 py-2 rounded mb-3"
            value={motif}
            onChange={(e) => setMotif(e.target.value)}
            required
          />

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Confirmer le rendez-vous
          </button>
        </form>
      )}
    </div>
  );
}
