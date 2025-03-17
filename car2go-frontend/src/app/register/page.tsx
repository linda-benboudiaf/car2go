"use client";

import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Header from "@/components/Header";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    nom: "",
    prenom: "",
    email: "",
    telephone: "",
    adresse: "",
    date_naissance: "",
    role: "",
    license_date: null as string | null,
    numero_permis: "",
    numero_livret: null as string | null,
    password: "",
  });

  const [, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const role = e.target.value;
    setFormData({
      ...formData,
      role,
      license_date: role === "accompagnateur" ? formData.license_date : null,
      numero_permis: role === "accompagnateur" ? formData.numero_permis : "",
      numero_livret: role === "apprenti" ? formData.numero_livret : null,
    });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    const cleanedFormData = {
      nom: formData.nom.trim(),
      prenom: formData.prenom.trim() || null,
      email: formData.email.trim(),
      telephone: formData.telephone.trim() || null,
      adresse: formData.adresse.trim(),
      date_naissance: formData.date_naissance || null,
      role: formData.role,
      license_date: formData.license_date || null,
      numero_permis: formData.numero_permis || null,
      numero_livret: formData.numero_livret || null,
      password: formData.password.trim() || null,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cleanedFormData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Échec de l'inscription.");
      }

      toast.success("Inscription réussie !");
    } catch (err: unknown) {
      if (err instanceof Error) {
        toast.error(err.message);
      } else {
        toast.error("Une erreur inconnue est survenue.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white relative">
      <ToastContainer />
      <Header />
      <div className="bg-[#F8F8F8] p-8 rounded-lg shadow-md w-[800px] mt-8 pt-20">

        <form onSubmit={handleRegister}>
          <div className="grid grid-cols-2 gap-6">
            {/* Première colonne */}
            <div>
              {[
                { label: "Nom", name: "nom", type: "text", maxLength: 100 },
                { label: "Prénom", name: "prenom", type: "text", maxLength: 100 },
                { label: "Email", name: "email", type: "email" },
                { label: "Mot de passe", name: "password", type: "password" },
                { label: "Date de naissance", name: "date_naissance", type: "date" },
                { label: "Téléphone", name: "telephone", type: "text", maxLength: 15 },
              ].map(({ label, name, type, maxLength }, index) => (
                <div key={index} className="mb-4 relative">
                  <label className="block text-[#001F3F]">{label} :</label>
                  <input
                    type={type}
                    name={name}
                    value={formData[name as keyof typeof formData] || ""}
                    onChange={handleChange}
                    {...(maxLength ? { maxLength } : {})}
                    required
                    className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
                  />
                </div>
              ))}

              <hr className="my-4 border-[#FF0040]" />
            </div>

            {/* Deuxième colonne */}
            <div>
              <div className="mb-4">
                <label className="block text-[#001F3F] mb-2">Vous êtes :</label>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    className={`w-1/2 px-4 py-2 text-center rounded-lg transition-all ${
                      formData.role === "apprenti"
                        ? "bg-[#FF0040] text-white"
                        : "bg-gray-200 text-[#001F3F] hover:bg-gray-300"
                    }`}
                    onClick={() =>
                      handleRoleChange({ target: { value: "apprenti" } } as React.ChangeEvent<HTMLInputElement>)
                    }
                  >
                    Apprenti
                  </button>
                  <button
                    type="button"
                    className={`w-1/2 px-4 py-2 text-center rounded-lg transition-all ${
                      formData.role === "accompagnateur"
                        ? "bg-[#FF0040] text-white"
                        : "bg-gray-200 text-[#001F3F] hover:bg-gray-300"
                    }`}
                    onClick={() =>
                      handleRoleChange({ target: { value: "accompagnateur" } } as React.ChangeEvent<HTMLInputElement>)
                    }
                  >
                    Accompagnateur
                  </button>
                </div>
              </div>

              <div className="mb-4">
                <label className="block text-[#001F3F]">Adresse :</label>
                <input
                  type="text"
                  name="adresse"
                  value={formData.adresse}
                  onChange={handleChange}
                  maxLength={255}
                  required
                  className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
                />
              </div>

              {formData.role === "accompagnateur" && (
                <>
                  <div className="mb-4">
                    <label className="block text-[#001F3F]">Date d&#39;obtention du permis :</label>
                    <input
                      type="date"
                      name="license_date"
                      value={formData.license_date || ""}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-[#001F3F]">Numéro de permis :</label>
                    <input
                      type="text"
                      name="numero_permis"
                      value={formData.numero_permis}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
                    />
                  </div>
                </>
              )}

              {formData.role === "apprenti" && (
                <div className="mb-4">
                  <label className="block text-[#001F3F]">Numéro de livret :</label>
                  <input
                    type="text"
                    name="numero_livret"
                    value={formData.numero_livret || ""}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
                  />
                </div>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-[#FF0040] text-white py-2 rounded-lg hover:bg-[#D90038] transition duration-300 mt-4"
          >
            {isLoading ? "Chargement..." : "S'inscrire"}
          </button>
        </form>
      </div>
    </div>
  );
}
