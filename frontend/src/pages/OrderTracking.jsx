// src/pages/OrderTracking.jsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import client from '../api/client';

const STEPS = ['placed', 'preparing', 'out_for_delivery', 'delivered'];

export default function OrderTracking() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    let timer;
    const fetchOrder = () => {
      client.get(`/orders/${id}`).then((res) => {
        setOrder(res.data);
        if (res.data.status === 'delivered') clearInterval(timer);
      });
    };

    fetchOrder();
    timer = setInterval(fetchOrder, 5000);
    return () => clearInterval(timer);
  }, [id]);

  if (!order) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-stone-400">Loading order...</p>
      </div>
    );
  }

  const currentStep = STEPS.indexOf(order.status);
  const branchName = order.branch_name || order.branch?.name;
  const items = order.items || [];
  const paymentStatus = order.payment_status || order.payment?.status;

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto space-y-4">
        <div className="bg-white rounded-xl border border-amber-100 shadow-sm p-6">
          <h1 className="text-xl font-bold text-stone-900">Order #{order.id}</h1>
          {branchName && (
            <p className="text-sm text-stone-500 mt-1">Branch: {branchName}</p>
          )}
          {paymentStatus && (
            <p className="text-sm text-stone-500">Payment: {paymentStatus}</p>
          )}
          <p className="text-stone-700 font-semibold mt-2">Total: ₹{order.total}</p>

          <div className="flex justify-between relative mt-6">
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

          <p className="text-center text-sm mt-6 font-medium text-red-900 capitalize">
            {order.status === 'delivered'
              ? 'Delivered. Enjoy your meal!'
              : `Status: ${order.status.replace(/_/g, ' ')}`}
          </p>
        </div>

        {items.length > 0 && (
          <div className="bg-white rounded-xl border border-amber-100 shadow-sm divide-y divide-amber-100">
            <h2 className="p-4 font-semibold text-stone-900">Items</h2>
            {items.map((it, i) => (
              <div key={i} className="flex justify-between p-4 text-sm">
                <span className="text-stone-700">
                  {it.name || it.menu_item_name || `Item ${it.menu_item_id}`} × {it.quantity}
                </span>
                <span className="text-stone-500">
                  ₹{(it.price_at_order ?? it.price ?? 0) * it.quantity}
                </span>
              </div>
            ))}
          </div>
        )}

        <Link to="/" className="block text-center text-sm text-red-800 underline">
          Order again
        </Link>
      </div>
    </div>
  );
}