'use client';
import { useState } from "react";
import Image from "next/image";
import Header from "@/components/Header";
import Link from "next/link";

export default function Home() {
  const images = ["/car1.jpg", "/car2.jpg", "/car3.jpg"];
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
  };

  return (
    <div className="bg-white text-[#001F3F]">
      <Header />
      <main className="container mx-auto px-6 pt-24">
        {/* Hero Section */}
        <section className="text-center py-10">
          <h1 className="text-4xl font-bold text-[#FF0040] mb-4">
            Apprenez à conduire en toute simplicité !
          </h1>
          <p className="text-lg mb-6">
            Louez nos véhicules à double commande et préparez votre permis en toute sécurité.
          </p>
          <Link href="/register">
            <button className="bg-[#FF0040] text-white px-6 py-3 rounded-lg hover:bg-[#D90038] transition duration-300">
              Réserver maintenant
            </button>
          </Link>
        </section>

        {/* Image Slider */}
        <section className="my-10 overflow-hidden relative h-[500px] sm:h-[400px] z-10">
          <div className="relative w-full h-full">
            <Image
              src={images[currentIndex]}
              alt="Voiture"
              layout="fill"
              objectFit="cover"
              className="transition-transform duration-500"
            />
            {/* Boutons de navigation */}
            <button
              onClick={prevImage}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-transparent text-white px-4 py-2 rounded-full"
            >
              ◀
            </button>
            <button
              onClick={nextImage}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-transparent text-white px-4 py-2 rounded-full"
            >
              ▶
            </button>
          </div>
        </section>

        {/* Tarifs Section */}
        <section className="py-10">
          <h2 className="text-3xl font-bold text-center mb-6">Nos Tarifs</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
            <div className="p-6 border border-[#001F3F] rounded-lg shadow-md">
              <h3 className="text-2xl font-semibold mb-3">1 heure</h3>
              <p className="text-lg">25€</p>
              <button className="mt-4 bg-[#FF0040] text-white px-4 py-2 rounded-lg hover:bg-[#D90038] transition duration-300">
                Réserver
              </button>
            </div>
            <div className="p-6 border border-[#001F3F] rounded-lg shadow-md">
              <h3 className="text-2xl font-semibold mb-3">2 heures</h3>
              <p className="text-lg">45€</p>
              <button className="mt-4 bg-[#FF0040] text-white px-4 py-2 rounded-lg hover:bg-[#D90038] transition duration-300">
                Réserver
              </button>
            </div>
            <div className="p-6 border border-[#001F3F] rounded-lg shadow-md">
              <h3 className="text-2xl font-semibold mb-3">5 heures</h3>
              <p className="text-lg">100€</p>
              <button className="mt-4 bg-[#FF0040] text-white px-4 py-2 rounded-lg hover:bg-[#D90038] transition duration-300">
                Réserver
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-[#001F3F] text-white py-6 mt-10 text-center">
        <p>&copy; 2025 Car2Go. Tous droits réservés.</p>
        <div className="mt-2 flex justify-center space-x-4">
          <Link href="/mentions-legales" className="hover:underline">Mentions Légales</Link>
          <Link href="/contact" className="hover:underline">Contact</Link>
        </div>
      </footer>
    </div>
  );
}
