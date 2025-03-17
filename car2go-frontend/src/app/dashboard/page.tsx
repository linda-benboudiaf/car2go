"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import SidebarBookingDetails from "@/components/SidebarBookingDetails";

interface User {
  id: number;
  nom: string;
  prenom: string;
  role: "apprenti" | "accompagnateur" | "admin";
}

interface Booking {
  id: number;
  user_id: number;
  car_id: number;
  start_time: string;
  end_time: string;
  purpose: string;  // Ajout du motif de réservation
  status: string;
  car: {
    id: number;
    nom: string;
    modele: string;
    annee_fab: number;
    type: string;
    plaque: string;
    controle_technique: string;
    prix_par_heure: number;
    disponible: boolean;
    image_url: string;
  };
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchUserAndBookings = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const userResponse = await fetch("http://127.0.0.1:8000/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!userResponse.ok) throw new Error("Échec de la récupération des données utilisateur.");
        const userData = await userResponse.json();
        setUser(userData);

        const bookingsResponse = await fetch("http://127.0.0.1:8000/bookings/user", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!bookingsResponse.ok) throw new Error("Impossible de récupérer les réservations.");
        const bookingsData = await bookingsResponse.json();
        setBookings(bookingsData);

      } catch (error) {
        console.error(error);
        router.push("/login");
      } finally {
        setLoading(false);
      }
    };

    fetchUserAndBookings();
  }, [router]);

  const onSelectBooking = (booking: Booking) => {
    setSelectedBooking(booking);
  };

  if (loading) {
    return <p className="text-center text-[#001F3F]">Chargement...</p>;
  }

  if (!user) {
    return <p className="text-center text-red-500">Erreur de récupération des données utilisateur.</p>;
  }

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar role={user.role} />
      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold text-[#001F3F]">Bienvenue, {user.prenom} !</h1>
        <DashboardContent role={user.role} bookings={bookings} onSelectBooking={onSelectBooking} />
        {selectedBooking && (
          <SidebarBookingDetails booking={selectedBooking} onClose={() => setSelectedBooking(null)} />
        )}
      </main>
    </div>
  );
}

function DashboardContent({ role, bookings, onSelectBooking }: { role: string; bookings: Booking[]; onSelectBooking: (booking: Booking) => void }) {
  return (
    <div className="mt-6">
      {role === "apprenti" && <ApprentiDashboard bookings={bookings} onSelectBooking={onSelectBooking} />}
      {role === "accompagnateur" && <AccompagnateurDashboard bookings={bookings} onSelectBooking={onSelectBooking} />}
      {role === "admin" && <AdminDashboard onSelectBooking={onSelectBooking} />}
    </div>
  );
}

function ApprentiDashboard({ bookings, onSelectBooking }: { bookings: Booking[]; onSelectBooking: (booking: Booking) => void }) {
  return (
    <div id="reservations" className="mt-4 p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-4">📅 Mes Réservations</h2>
      {bookings.length === 0 ? (
        <p className="text-gray-500 text-center">Aucune réservation pour le moment.</p>
      ) : (
        <div className="overflow-x-auto w-full">
          <table className="w-full border-collapse border border-gray-200 min-w-[900px]">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="border border-gray-300 px-6 py-3 whitespace-nowrap">Nom Voiture</th>
                <th className="border border-gray-300 px-6 py-3 whitespace-nowrap">Début</th>
                <th className="border border-gray-300 px-6 py-3 whitespace-nowrap">Fin</th>
                <th className="border border-gray-300 px-6 py-3 whitespace-nowrap">Durée (h)</th>
                <th className="border border-gray-300 px-6 py-3 whitespace-nowrap">Motif</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map((booking) => {
                const startTime = new Date(booking.start_time);
                const endTime = new Date(booking.end_time);
                const duration = Math.abs((endTime.getTime() - startTime.getTime()) / (1000 * 60 * 60)); // Durée en heures
                const motif = booking.purpose === "self" ? "Perfectionnement" : `Accompagnement de l'apprenti XX`;

                return (
                  <tr
                    key={booking.id}
                    className="border border-gray-300 cursor-pointer hover:bg-gray-100"
                    onClick={() => onSelectBooking(booking)}
                  >
                    <td className="border border-gray-300 px-6 py-3">{booking.car?.nom ?? "Non disponible"}</td>
                    <td className="border border-gray-300 px-6 py-3">{startTime.toLocaleString()}</td>
                    <td className="border border-gray-300 px-6 py-3">{endTime.toLocaleString()}</td>
                    <td className="border border-gray-300 px-6 py-3">{duration} h</td>
                    <td className="border border-gray-300 px-6 py-3">{motif}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function AccompagnateurDashboard({ bookings, onSelectBooking }: { bookings: Booking[]; onSelectBooking: (booking: Booking) => void }) {
  return (
    <div className="mt-4 p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-4">🚗 Sessions Accompagnées</h2>
      {bookings.length === 0 ? (
        <p className="text-gray-500">Aucune session prévue.</p>
      ) : (
        <ul className="mt-2">
          {bookings.map((booking) => (
            <li
              key={booking.id}
              className="p-3 bg-white shadow-md rounded-lg mb-2 cursor-pointer hover:bg-gray-100"
              onClick={() => onSelectBooking(booking)}
            >
              🚗 {booking.car.nom} - {new Date(booking.start_time).toLocaleString()} → {new Date(booking.end_time).toLocaleString()} ({booking.status})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function AdminDashboard({ onSelectBooking }: { onSelectBooking: (booking: Booking) => void }) {
  return (
    <div className="mt-4 p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-4">⚙️ Gestion des Réservations</h2>
      <p className="text-gray-500">Sélectionnez une réservation pour afficher ses détails.</p>
      <li>
        <button
          onClick={() => onSelectBooking({ id: 1, user_id: 1, car_id: 1, start_time: "2025-01-01T00:00:00Z", end_time: "2025-01-01T01:00:00Z", purpose: "Test", status: "En attente", car: { id: 1, nom: "Test", modele: "Test", annee_fab: 2025, type: "Test", plaque: "Test", controle_technique: "2025-01-01", prix_par_heure: 0, disponible: true, image_url: "https://via.placeholder.com/150" } })}
          className="p-3 bg-white shadow-md rounded-lg mb-2 cursor-pointer hover:bg-gray-100"
        >
          🚗 Test - 01/01/2025 00:00 → 01:00 (En attente)
        </button>
      </li>
    </div>
  );
}
