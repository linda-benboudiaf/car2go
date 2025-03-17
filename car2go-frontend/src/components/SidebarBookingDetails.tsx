import React from "react";

interface Booking {
  id: number;
  user_id: number;
  car_id: number;
  start_time: string;
  end_time: string;
  purpose: string;
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

interface SidebarBookingDetailsProps {
  booking: Booking | null;
  onClose: () => void;
}

const SidebarBookingDetails: React.FC<SidebarBookingDetailsProps> = ({ booking, onClose }) => {
  if (!booking) return null; // Vérifie que booking est défini avant d'afficher la sidebar
  const motif = booking.purpose === "self" ? "Perfectionnement" : `Accompagnement de l'apprenti XX`;

  return (
    <div className="fixed top-0 right-0 h-full w-1/3 bg-white shadow-lg p-6 overflow-y-auto z-50 transition-transform duration-300 translate-x-0">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Détails de la Réservation</h2>
          <button onClick={onClose} className="text-gray-600 hover:text-red-500 text-lg">✖</button>
        </div>

        <img src='./car3.jpg' alt={booking.car.nom} className="w-full h-70 object-cover rounded-md mb-4" />

        <p><strong>Voiture :</strong> {booking.car.nom} - {booking.car.modele}</p>
        <p><strong>Plaque :</strong> {booking.car.plaque}</p>
        <p><strong>Année :</strong> {booking.car.annee_fab}</p>
        <p><strong>Type :</strong> {booking.car.type}</p>
        <p><strong>Contrôle Technique :</strong> {booking.car.controle_technique}</p>
        <p><strong>Début :</strong> {new Date(booking.start_time).toLocaleString()}</p>
        <p><strong>Fin :</strong> {new Date(booking.end_time).toLocaleString()}</p>
        <p><strong>Motif :</strong> {motif}</p>
        <p><strong>Statut :</strong> {booking.status}</p>
        <p><strong>Prix :</strong> {booking.car.prix_par_heure} €/h</p>
        <p><strong>Disponible :</strong> {booking.car.disponible ? "Oui" : "Non"}</p>

        <button
          onClick={onClose}
          className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
        >
          Fermer
        </button>
    </div>
  );
};

export default SidebarBookingDetails;
