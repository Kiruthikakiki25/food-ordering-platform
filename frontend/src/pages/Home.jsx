// src/pages/Home.jsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function Home() {
  const [branches, setBranches] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    client
      .get('/branches')
      .then((res) => setBranches(res.data))
      .catch(() =>
        setError('Could not load branches. The server may be waking up, please retry in a minute.')
      )
      .finally(() => setLoading(false));
  }, []);

  const chooseBranch = (branch) => {
    localStorage.setItem('branch', JSON.stringify(branch));
    navigate('/menu');
  };

  const filtered = branches.filter(
    (b) =>
      b.name.toLowerCase().includes(search.toLowerCase()) ||
      b.city.toLowerCase().includes(search.toLowerCase()) ||
      b.pincode.includes(search)
  );

  return (
    <div className="min-h-screen bg-orange-50">
      <div className="bg-red-900 py-12 px-6 text-white">
        <h1 className="text-3xl font-bold mb-1">
          What are you <span className="text-amber-400">craving</span> today?
        </h1>
        <p className="text-red-100 mb-5">Choose your nearest branch to start ordering</p>
        <input
          type="text"
          placeholder="Search by branch, city or pincode..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md px-4 py-3 rounded-lg bg-white text-stone-800 placeholder-stone-400 shadow-md focus:outline-none focus:ring-2 focus:ring-amber-500"
        />
      </div>

      {loading && <p className="text-center text-stone-500 mt-10">Loading branches...</p>}
      {error && <p className="text-center text-red-700 mt-10">{error}</p>}

      <div className="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 max-w-6xl mx-auto">
        {filtered.map((b) => (
          <div
            key={b.id}
            className="bg-white rounded-xl border border-amber-100 overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200"
          >
            <div className="h-32 bg-amber-50 flex items-center justify-center">
              <span className="text-4xl">📍</span>
            </div>
            <div className="p-4">
              <h2 className="font-semibold text-stone-900">{b.name}</h2>
              <p className="text-sm text-stone-500 mt-1">
                {b.address}, {b.city} - {b.pincode}
              </p>
              <p className="text-sm text-stone-500">Phone: {b.phone}</p>
              <button
                onClick={() => chooseBranch(b)}
                className="mt-3 w-full bg-red-800 text-white py-2 rounded-lg hover:bg-red-900 transition-colors"
              >
                Order from here
              </button>
            </div>
          </div>
        ))}
      </div>

      {!loading && !error && filtered.length === 0 && (
        <p className="text-center text-stone-400 mt-10">No branches match your search.</p>
      )}
    </div>
  );
}