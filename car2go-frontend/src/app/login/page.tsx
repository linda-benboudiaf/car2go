"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthProvider";
import { ToastContainer, toast } from "react-toastify";
import { useRouter } from "next/navigation";
import Header from "@/components/Header";
import "react-toastify/dist/ReactToastify.css";

export default function LoginPage() {
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  interface LoginResponse {
    access_token: string;
    token_type: string;
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Email ou mot de passe incorrect.");
        } else if (response.status >= 500) {
          throw new Error("Erreur serveur, veuillez réessayer plus tard.");
        } else {
          throw new Error("Connexion échouée. Vérifiez vos identifiants.");
        }
      }

      const data: LoginResponse = await response.json();

      localStorage.setItem("token", data.access_token);
      setUser({ email, token: data.access_token });
      toast.success("Connexion réussie !");
      // Redirection vers le dashboard après connexion
      router.push("/dashboard");
    } catch (err: unknown) {
      if (err instanceof Error) {
        toast.error(err.message);
      } else {
        toast.error("Une erreur inconnue est survenue.");
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white relative">
      <ToastContainer />
      <Header/>
      <div className="bg-[#F8F8F8] p-8 rounded-lg shadow-md w-96">
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-[#001F3F]">Email :</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
            />
          </div>
          <div className="mb-4">
            <label className="block text-[#001F3F]">Mot de passe :</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-[#001F3F] rounded-lg focus:outline-none focus:ring focus:ring-[#FF0040] focus:border-[#FF0040] bg-white text-[#001F3F]"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-[#FF0040] text-white py-2 rounded-lg hover:bg-[#D90038] transition duration-300"
          >
            Se connecter
          </button>
        </form>
        <div className="text-center mt-4">
          <a href="#" className="text-[#FF0040] text-sm hover:underline">
            Mot de passe oublié ?
          </a>
        </div>
      </div>
    </div>
  );
}