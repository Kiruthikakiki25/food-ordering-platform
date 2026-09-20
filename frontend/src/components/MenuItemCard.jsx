// src/components/MenuItemCard.jsx
export default function MenuItemCard({ item, onAddToCart }) {
  return (
    <div className="bg-white border border-amber-100 rounded-lg p-4 flex justify-between items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
      <div>
        <div className="flex items-center gap-2">
          <span
            title={item.veg_flag ? 'Vegetarian' : 'Non-vegetarian'}
            className={`inline-block w-3 h-3 rounded-full ${
              item.veg_flag ? 'bg-green-600' : 'bg-red-600'
            }`}
          />
          <h3 className="font-semibold text-stone-900">{item.name}</h3>
        </div>
        <p className="text-sm text-stone-500">{item.category}</p>
        {item.description && (
          <p className="text-sm text-stone-600 mt-1">{item.description}</p>
        )}
        <p className="text-sm font-bold text-red-900 mt-1">₹{item.price}</p>
      </div>
      <button
        onClick={() => onAddToCart(item)}
        className="bg-amber-600 text-white font-semibold text-sm px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors shrink-0"
      >
        Add
      </button>
    </div>
  );
}