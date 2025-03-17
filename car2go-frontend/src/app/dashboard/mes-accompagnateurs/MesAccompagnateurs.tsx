"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthProvider";
import { useRouter } from "next/navigation";

interface Accompagnateur {
  id: number;
  accompagnateur_id: number;
  lien: string;
  accompagnateur: {
    id: number;
    nom: string;
    prenom: string;
    email: string;
  };
}

export default function MesAccompagnateurs() {
  const { user, token } = useAuth();
  const router = useRouter();
  const [accompagnateurs, setAccompagnateurs] = useState<Accompagnateur[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user) {
      router.push("/login");
      return;
    }

    const fetchAccompagnateurs = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/apprenti_accompagnateur/${user.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) throw new Error("Erreur lors de la récupération des accompagnateurs");

        const data = await response.json();
        setAccompagnateurs(data);
      } catch (err) {
        setError("Impossible de charger les accompagnateurs.");
      } finally {
        setLoading(false);
      }
    };

    fetchAccompagnateurs();
  }, [user, token, router]);

  const handleDelete = async (id: number) => {
    if (!window.confirm("Voulez-vous vraiment supprimer cet accompagnateur ?")) return;

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/apprenti_accompagnateur/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) throw new Error("Erreur lors de la suppression.");

      setAccompagnateurs(accompagnateurs.filter((acc) => acc.id !== id));
    } catch (err) {
      setError("Impossible de supprimer cet accompagnateur.");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Mes Accompagnateurs</h1>

      {loading && <p>Chargement...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && accompagnateurs.length === 0 && (
        <p className="text-gray-500">Aucun accompagnateur trouvé.</p>
      )}

      {!loading && accompagnateurs.length > 0 && (
        <table className="w-full border-collapse border border-gray-300 mt-4">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2">Nom</th>
              <th className="border border-gray-300 px-4 py-2">Prénom</th>
              <th className="border border-gray-300 px-4 py-2">Email</th>
              <th className="border border-gray-300 px-4 py-2">Lien</th>
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {accompagnateurs.map((acc) => (
              <tr key={acc.id} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2">{acc.accompagnateur.nom}</td>
                <td className="border border-gray-300 px-4 py-2">{acc.accompagnateur.prenom}</td>
                <td className="border border-gray-300 px-4 py-2">{acc.accompagnateur.email}</td>
                <td className="border border-gray-300 px-4 py-2">{acc.lien}</td>
                <td className="border border-gray-300 px-4 py-2 text-center">
                  <button
                    onClick={() => handleDelete(acc.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="mt-6">
        <button
          onClick={() => alert("Ajout d'un accompagnateur (fonctionnalité à venir)")}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Ajouter un accompagnateur
        </button>
      </div>
    </div>
  );
}