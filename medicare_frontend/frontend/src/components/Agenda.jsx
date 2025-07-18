import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useAxios from "../hooks/useAxios";

export default function Agenda() {
  const { id } = useParams(); // ID du médecin
  const axiosInstance = useAxios();
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axiosInstance
      .get(`/agenda/?medecin=${id}`)
      .then((res) => {
        console.log("✅ Slots reçus:", res.data);
        setSlots(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  const handleBooking = async (slot) => {
    console.log("🟡 Créneau cliqué :", slot);

    const payload = {
      date: slot.date,
      motif: "Consultation",
      disponibilite: slot.disponibilite_id,
      medecin: parseInt(id),
    };

    try {
      await axiosInstance.post("/rendezvous/", payload);
      alert("✅ Rendez-vous pris avec succès !");
      // Refresh slots
      const res = await axiosInstance.get(`/agenda/?medecin=${id}`);
      setSlots(res.data);
    } catch (err) {
      console.error("🚫 Erreur détaillée :", err.response?.data || err.message);
      alert("❌ Impossible de prendre ce créneau.");
    }
  };

  const groupedSlots = slots.reduce((acc, slot) => {
    const dateKey = new Date(slot.date).toISOString().split("T")[0];
    acc[dateKey] = acc[dateKey] || [];
    acc[dateKey].push(slot);
    return acc;
  }, {});

  if (loading) return <p className="text-center text-blue-500">Chargement de l’agenda...</p>;

  if (!slots.length)
    return <p className="text-center text-gray-500">Aucun créneau disponible.</p>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-center text-blue-800 mb-6">
        Agenda du médecin {id}
      </h2>

      <div className="space-y-8">
        {Object.entries(groupedSlots).map(([date, daySlots]) => (
          <div key={date}>
            <h3 className="text-lg font-semibold text-blue-700 mb-3">
              {new Date(date).toLocaleDateString("fr-FR", {
                weekday: "long",
                day: "2-digit",
                month: "long",
              })}
            </h3>
            <div className="flex flex-wrap gap-4">
              {daySlots.map((slot, idx) => (
                <div
                  key={idx}
                  className={`p-4 w-[130px] rounded-lg border text-center transition shadow-sm ${
                    slot.is_booked
                      ? "bg-gray-200 text-gray-500 cursor-not-allowed"
                      : "bg-white hover:bg-blue-50"
                  }`}
                >
                  <p className="text-sm font-medium">
                    {new Date(slot.date).toLocaleTimeString("fr-FR", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                  {slot.is_booked ? (
                    <p className="text-xs text-red-500 mt-2 font-semibold">Réservé</p>
                  ) : (
                    <button
                      onClick={() => handleBooking(slot)}
                      className="mt-2 text-sm text-blue-600 hover:underline"
                    >
                      Réserver
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
