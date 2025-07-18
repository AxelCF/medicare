import React, { useEffect, useState } from "react";
import useAxios from "../hooks/useAxios";

export default function DoctorsList({ onSelectMedecin }) {
  const axiosInstance = useAxios();
  const [doctors, setDoctors] = useState([]);
  const [dispos, setDispos] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoctorsAndDispos = async () => {
      try {
        const doctorsRes = await axiosInstance.get("medecins/");
        const disposPromises = doctorsRes.data.map((doc) =>
          axiosInstance.get(`disponibilites/?medecin=${doc.id}`)
        );
        const disposRes = await Promise.all(disposPromises);
        const disposData = {};
        disposRes.forEach((res, idx) => {
          disposData[doctorsRes.data[idx].id] = res.data;
        });

        setDoctors(doctorsRes.data);
        setDispos(disposData);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    };

    fetchDoctorsAndDispos();
  }, []);

  if (loading) {
    return <p className="text-center text-blue-600">Chargement des médecins...</p>;
  }

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">
        Nos médecins
      </h2>

      <ul className="space-y-4">
        {doctors.map((doctor) => {
          const hasDispo = dispos[doctor.id]?.length > 0;

          return (
            <li
              key={doctor.id}
              className="border p-4 rounded shadow flex justify-between items-center hover:shadow-lg transition"
            >
              <div>
                <p className="font-semibold text-lg text-gray-800">
                  Dr. {doctor.user.first_name} {doctor.user.last_name}
                </p>
                <p className="text-gray-500 mb-2">{doctor.specialty}</p>
                {hasDispo ? (
                  <p className="text-green-600 font-semibold">Créneaux disponibles</p>
                ) : (
                  <p className="text-red-600 font-semibold">Indisponible</p>
                )}
              </div>

              {hasDispo && (
                <button
                  onClick={() => onSelectMedecin(doctor.id)}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Prendre RDV
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
