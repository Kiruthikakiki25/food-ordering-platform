// src/pages/OrderTracking.jsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import client from '../api/client';

const STEPS = ['placed', 'preparing', 'out_for_delivery', 'delivered'];

export default function OrderTracking() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    const fetchOrder = () => {
      client.get(`/orders/${id}`).then((res) => setOrder(res.data));
    };

    fetchOrder(); // initial load

    const interval = setInterval(() => {
      fetchOrder();
    }, 5000); // poll every 5 seconds

    return () => clearInterval(interval); // cleanup on unmount
  }, [id]);

  if (!order) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-stone-400">Loading order...</p>
      </div>
    );
  }

  const currentStep = STEPS.indexOf(order.status);

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto bg-white rounded-xl border border-amber-100 shadow-sm p-6">
        <h1 className="text-xl font-bold text-stone-900 mb-1">Order #{order.id}</h1>
        <p className="text-stone-500 mb-6">Total: ₹{order.total}</p>

        <div className="flex justify-between relative">
          {STEPS.map((step, i) => (
            <div key={step} className="flex flex-col items-center flex-1 relative z-10">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                  i <= currentStep ? 'bg-amber-600 text-white' : 'bg-stone-200 text-stone-400'
                }`}
              >
                {i + 1}
              </div>
              <p className="text-xs mt-2 text-center text-stone-600 capitalize">
                {step.replace(/_/g, ' ')}
              </p>
            </div>
          ))}
          <div className="absolute top-4 left-0 right-0 h-0.5 bg-stone-200 -z-0" />
        </div>
      </div>
    </div>
  );
}