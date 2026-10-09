import { useState, useEffect } from "react"
import axios from "../api/client"

export default function RecommendedItems() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) { setLoading(false); return }

    axios.get("/api/recommendations", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => setItems(r.data))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-sm text-stone-400">Loading recommendations...</p>
  if (!items.length) return null

  return (
    <section className="my-8">
      <h2 className="text-xl font-bold text-red-900 mb-4">✨ Recommended for You</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-stone-200 rounded-xl p-4 shadow-sm">
            <p className="font-semibold text-stone-800 text-sm">{item.name}</p>
            <p className="text-xs text-stone-400 mb-1">{item.category}</p>
            <p className="text-amber-600 font-bold">₹{item.price}</p>
            <p className="text-xs text-stone-400 mt-1 italic">{item.reason}</p>
          </div>
        ))}
      </div>
    </section>
  )
}