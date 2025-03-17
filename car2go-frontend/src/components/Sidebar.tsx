import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Sidebar({ role }: { role: string }) {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <aside className="w-64 bg-[#001F3F] text-white min-h-screen p-6 flex flex-col justify-between">
      <div>
        <h2 className="text-xl font-bold mb-6">Tableau de bord</h2>
        <nav className="space-y-4">
          <Link href="/dashboard" className="block hover:underline">🏠 Accueil</Link>
          {role === "apprenti" && <Link href="/booking" className="block hover:underline">📅 Réserver une voiture</Link>}
          {role === "accompagnateur" && <Link href="/sessions" className="block hover:underline">🚗 Mes apprentis</Link>}
          {role === "admin" && <Link href="/admin/cars" className="block hover:underline">⚙️ Gestion des voitures</Link>}
        </nav>
      </div>

      {/* Bouton de Déconnexion */}
      <button
        onClick={handleLogout}
        className="mt-6 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
      >
          Déconnexion
      </button>
    </aside>
  );
}
