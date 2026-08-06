// src/pages/Login.jsx
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await client.post('/auth/login', form);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-white p-8 rounded-xl border border-amber-100 shadow-sm space-y-4">
        <h1 className="text-2xl font-bold text-stone-900">Welcome back</h1>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <input
          type="email" placeholder="Email"
          className="w-full border border-stone-200 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password" placeholder="Password"
          className="w-full border border-stone-200 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <button className="w-full bg-red-900 text-white font-bold p-3 rounded-lg hover:bg-red-800 transition-colors">
          Log in
        </button>
        <p className="text-sm text-center text-stone-500">
          No account? <Link to="/register" className="text-amber-700 font-semibold">Register</Link>
        </p>
      </form>
    </div>
  );
}