// src/pages/Menu.jsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import MenuItemCard from '../components/MenuItemCard';

export default function Menu() {
  const branch = JSON.parse(localStorage.getItem('branch') || 'null');
  const [menu, setMenu] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    client
      .get('/menu')
      .then((res) => setMenu(res.data))
      .catch(() => setError('Could not load the menu. Please try again.'))
      .finally(() => setLoading(false));
  }, []);

  const handleAddToCart = (item) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existing = cart.find((c) => c.menu_item_id === item.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({ menu_item_id: item.id, name: item.name, price: item.price, quantity: 1 });
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${item.name} added to cart`);
  };

  if (!branch) {
    return (
      <div className="min-h-screen bg-orange-50 flex flex-col items-center justify-center gap-3">
        <p className="text-stone-500">Please choose a branch first.</p>
        <Link to="/" className="bg-red-800 text-white px-4 py-2 rounded-lg">
          Choose branch
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto space-y-3">
        <div className="flex justify-between items-center mb-2">
          <div>
            <h1 className="text-2xl font-bold text-stone-900">Menu</h1>
            <p className="text-sm text-stone-500">Ordering from {branch.name} branch</p>
          </div>
          <Link to="/" className="text-sm text-red-800 underline">
            Change branch
          </Link>
        </div>

        {loading && <p className="text-stone-500 text-center">Loading menu...</p>}
        {error && <p className="text-red-700 text-center">{error}</p>}

        {menu.map((item) => (
          <MenuItemCard key={item.id} item={item} onAddToCart={handleAddToCart} />
        ))}
      </div>
    </div>
  );
}