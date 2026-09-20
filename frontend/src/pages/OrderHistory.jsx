// src/pages/OrderHistory.jsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';

export default function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    client
      .get('/orders/my-orders')
      .then((res) => setOrders(res.data))
      .catch((err) =>
        setError(
          err.response?.status === 401
            ? 'Please log in to see your orders.'
            : 'Could not load your orders. Please try again.'
        )
      )
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto space-y-3">
        <h1 className="text-2xl font-bold text-stone-900">My Orders</h1>

        {loading && <p className="text-stone-500 text-center">Loading orders...</p>}
        {error && (
          <p className="text-red-700 text-center">
            {error} <Link to="/login" className="underline">Log in</Link>
          </p>
        )}
        {!loading && !error && orders.length === 0 && (
          <p className="text-stone-400 text-center mt-10">You have no orders yet.</p>
        )}

        {orders.map((o) => (
          <Link
            to={`/orders/${o.id}`}
            key={o.id}
            className="block bg-white border border-amber-100 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-center">
              <h2 className="font-semibold text-stone-900">Order #{o.id}</h2>
              <span className="text-xs font-bold px-2 py-1 rounded-full bg-amber-600 text-white capitalize">
                {(o.status || '').replace(/_/g, ' ')}
              </span>
            </div>
            {(o.branch_name || o.branch?.name) && (
              <p className="text-sm text-stone-500 mt-1">
                Branch: {o.branch_name || o.branch?.name}
              </p>
            )}
            {o.created_at && (
              <p className="text-sm text-stone-500">
                {new Date(o.created_at).toLocaleString()}
              </p>
            )}
            <p className="text-sm font-bold text-red-900 mt-1">₹{o.total}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}