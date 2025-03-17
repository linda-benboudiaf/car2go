import Image from "next/image";
import Link from "next/link";

interface HeaderProps {
  className?: string;
}

export default function Header({ className }: HeaderProps) {
  return (
    <header className={`fixed top-0 left-0 w-full bg-white shadow-md z-50 ${className || ""}`}>
      <div className="container mx-auto flex items-center justify-between p-4">
        <Link href="/">
          <Image src="/logo.png" alt="Car2Go Logo" width={120} height={40} />
        </Link>
        <div className="flex space-x-4">
          <Link href="/login">
            <button className="px-4 py-2 text-white bg-[#001F3F] rounded-lg hover:bg-[#003366] transition">
              Connexion
            </button>
          </Link>
          <Link href="/register">
            <button className="px-4 py-2 text-white bg-[#FF0040] rounded-lg hover:bg-[#D90038] transition">
              Inscription
            </button>
          </Link>
        </div>
      </div>
    </header>
  );
}