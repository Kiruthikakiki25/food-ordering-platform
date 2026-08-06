// src/pages/Register.jsx
import { useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await client.post('/auth/register', form);
      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed');
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center px-4">
        <div className="max-w-sm text-center bg-white p-8 rounded-xl border border-amber-100 shadow-sm">
          <h1 className="text-xl font-bold text-stone-900">Check your email</h1>
          <p className="text-stone-500 mt-2">
            We sent a verification link to {form.email}. Verify your account before logging in.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-white p-8 rounded-xl border border-amber-100 shadow-sm space-y-4">
        <h1 className="text-2xl font-bold text-stone-900">Create account</h1>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <input
          type="text" placeholder="Name"
          className="w-full border border-stone-200 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
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
          Create account
        </button>
        <p className="text-sm text-center text-stone-500">
          Already have an account? <Link to="/login" className="text-amber-700 font-semibold">Log in</Link>
        </p>
      </form>
    </div>
  );
}