// src/components/MenuItemCard.jsx
export default function MenuItemCard({ item, onAddToCart }) {
  return (
    <div className="bg-white border border-amber-100 rounded-lg p-4 flex justify-between items-center shadow-sm hover:shadow-md transition-shadow">
      <div>
        <h3 className="font-semibold text-stone-900">{item.name}</h3>
        <p className="text-sm text-stone-500">{item.category}</p>
        <p className="text-sm font-bold text-red-900 mt-1">₹{item.price}</p>
      </div>
      <button
        onClick={() => onAddToCart(item)}
        className="bg-amber-600 text-white font-semibold text-sm px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors"
      >
        Add
      </button>
    </div>
  );
}