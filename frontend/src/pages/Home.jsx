// src/pages/Home.jsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';

export default function Home() {
  const [restaurants, setRestaurants] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    client.get('/restaurants').then((res) => setRestaurants(res.data));
  }, []);

  const filtered = restaurants.filter(
    (r) =>
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      r.cuisine.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-orange-50">
      {/* Hero / search bar */}
      <div className="bg-red-900 py-12 px-6 text-white">
        <h1 className="text-3xl font-bold mb-1">
          What are you <span className="text-amber-400">craving</span> today?
        </h1>
        <p className="text-red-100 mb-5">Order from the best restaurants near you</p>
        <input
  type="text"
  placeholder="Search restaurants or cuisines..."
  value={search}
  onChange={(e) => setSearch(e.target.value)}
  className="w-full max-w-md px-4 py-3 rounded-lg bg-white text-stone-800 placeholder-stone-400 shadow-md focus:outline-none focus:ring-2 focus:ring-amber-500"
/>
      </div>

      {/* Restaurant grid */}
      <div className="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 max-w-6xl mx-auto">
        {filtered.map((r) => (
          <Link
            to={`/restaurants/${r.id}`}
            key={r.id}
            className="group bg-white rounded-xl border border-amber-100 overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200"
          >
            <div className="h-32 bg-amber-50 flex items-center justify-center">
              <span className="text-4xl">🍽️</span>
            </div>
            <div className="p-4">
              <div className="flex justify-between items-start">
                <h2 className="font-semibold text-stone-900 group-hover:text-red-800 transition-colors">
                  {r.name}
                </h2>
                <span className="flex items-center gap-1 bg-amber-600 text-white text-xs font-bold px-2 py-1 rounded-full">
                  ★ {r.rating}
                </span>
              </div>
              <p className="text-sm text-stone-500 mt-1">{r.cuisine}</p>
            </div>
          </Link>
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="text-center text-stone-400 mt-10">No restaurants match your search.</p>
      )}
    </div>
  );
}