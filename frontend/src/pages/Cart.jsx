// src/pages/Cart.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function Cart() {
  const [cart, setCart] = useState(() => JSON.parse(localStorage.getItem('cart') || '[]'));
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const updateQuantity = (menu_item_id, delta) => {
    const updated = cart
      .map((item) =>
        item.menu_item_id === menu_item_id
          ? { ...item, quantity: item.quantity + delta }
          : item
      )
      .filter((item) => item.quantity > 0);
    setCart(updated);
    localStorage.setItem('cart', JSON.stringify(updated));
  };

  const handlePlaceOrder = async () => {
    try {
      const { data } = await client.post('/orders', {
        items: cart.map((item) => ({
          menu_item_id: item.menu_item_id,
          quantity: item.quantity,
        })),
      });
      localStorage.removeItem('cart');
      navigate(`/orders/${data.order_id}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to place order');
    }
  };

  if (cart.length === 0) {
    return (
      <div className="min-h-screen bg-orange-50 flex items-center justify-center">
        <p className="text-stone-400 text-lg">Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto space-y-4">
        <h1 className="text-2xl font-bold text-stone-900">Your Cart</h1>
        {error && <p className="text-red-600 text-sm">{error}</p>}

        <div className="bg-white rounded-xl border border-amber-100 divide-y divide-amber-100 shadow-sm">
          {cart.map((item) => (
            <div key={item.menu_item_id} className="flex justify-between items-center p-4">
              <div>
                <p className="font-medium text-stone-900">{item.name}</p>
                <p className="text-sm text-stone-500">₹{item.price} each</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => updateQuantity(item.menu_item_id, -1)}
                  className="w-7 h-7 rounded-full bg-stone-100 text-stone-700 font-bold hover:bg-stone-200"
                >
                  −
                </button>
                <span className="font-semibold w-4 text-center">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.menu_item_id, 1)}
                  className="w-7 h-7 rounded-full bg-amber-600 text-white font-bold hover:bg-amber-700"
                >
                  +
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between items-center font-bold text-lg bg-white rounded-xl p-4 border border-amber-100">
          <span className="text-stone-900">Total</span>
          <span className="text-red-900">₹{total}</span>
        </div>

        <button
          onClick={handlePlaceOrder}
          className="w-full bg-red-900 text-white font-bold py-3 rounded-lg hover:bg-red-800 transition-colors shadow-md"
        >
          Place Order
        </button>
      </div>
    </div>
  );
}