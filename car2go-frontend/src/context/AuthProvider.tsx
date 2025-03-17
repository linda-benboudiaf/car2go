"use client";

import { createContext, useContext, useState, useEffect } from "react";

// Définition du type User
type User = {
  id?: number;
  name?: string;
  email: string;
  role?: "admin" | "user";
};

type AuthContextType = {
  user: User | null;
  setUser: (user: { email: string; token: string }) => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Exemple : Vérifier si l'utilisateur est déjà connecté (localStorage ou requête API)
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}