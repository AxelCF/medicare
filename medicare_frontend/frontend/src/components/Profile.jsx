import React, { useEffect, useState } from "react";
import API from "../api";

export default function Profile() {
  const [profile, setProfile] = useState({ user: {}, phone: "" });

  useEffect(() => {
    API.get("profile/").then((res) => setProfile(res.data));
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, phone: e.target.value });
  };

  const handleSave = async () => {
    await API.patch("profile/", { phone: profile.phone, user: profile.user });
    alert("Profil mis à jour !");
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Mon Profil</h1>
      <p>Nom : {profile.user.first_name} {profile.user.last_name}</p>
      <p>Email : {profile.user.email}</p>
      <label className="block mt-4">Téléphone :</label>
      <input
        type="text"
        value={profile.phone}
        onChange={handleChange}
        className="border px-2 py-1"
      />
      <button
        onClick={handleSave}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Sauvegarder
      </button>
    </div>
  );
}
