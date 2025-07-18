import React, { useState } from "react";
import useAxios from "../hooks/useAxios";

export default function CompteRenduForm({ rendezvous }) {
  const axiosInstance = useAxios();
  const [notes, setNotes] = useState(rendezvous.notes_medicales || "");
  const [saved, setSaved] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axiosInstance.patch(`/rendezvous/${rendezvous.id}/`, {
        notes_medicales: notes,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error("Erreur lors de l'enregistrement du compte-rendu", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-2">
      <textarea
        className="w-full border rounded p-2 text-sm"
        rows={3}
        placeholder="Compte-rendu médical"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
      <button
        type="submit"
        className="mt-1 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
      >
        Enregistrer
      </button>
      {saved && (
        <span className="text-green-600 text-sm ml-2">✅ Enregistré</span>
      )}
    </form>
  );
}
