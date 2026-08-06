// src/pages/RestaurantMenu.jsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import client from '../api/client';
import MenuItemCard from '../components/MenuItemCard';

export default function RestaurantMenu() {
  const { id } = useParams();
  const [menu, setMenu] = useState([]);

  useEffect(() => {
    client.get(`/restaurants/${id}/menu`).then((res) => setMenu(res.data));
  }, [id]);

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

  return (
    <div className="min-h-screen bg-orange-50 p-6">
      <div className="max-w-lg mx-auto space-y-3">
        <h1 className="text-2xl font-bold text-stone-900 mb-4">Menu</h1>
        {menu.map((item) => (
          <MenuItemCard key={item.id} item={item} onAddToCart={handleAddToCart} />
        ))}
        {menu.length === 0 && (
          <p className="text-stone-400 text-center mt-10">No items found for this restaurant.</p>
        )}
      </div>
    </div>
  );
}