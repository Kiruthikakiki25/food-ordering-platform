import { useState } from "react"
import axios from "../api/client"

export default function SmartSearch() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const search = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      // restaurant_id=1 works for single-brand; adjust if needed
      const res = await axios.post("/api/restaurants/1/smart-search", { query })
      setResults(res.data)
    } catch {
      setResults({ explanation: "Couldn't process your query.", recommendations: [] })
    }
    setLoading(false)
  }

  return (
    <div className="my-6">
      <h2 className="text-lg font-bold text-red-900 mb-2">🔍 Smart Menu Search</h2>
      <div className="flex gap-2">
        <input
          className="flex-1 border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
          placeholder={`Try: "What's safe for peanut allergy under Rs.200?"`}
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
        />
        <button
          onClick={search}
          disabled={loading}
          className="bg-amber-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-amber-500 disabled:opacity-50"
        >
          {loading ? "..." : "Search"}
        </button>
      </div>

      {results && (
        <div className="mt-4 bg-white border border-stone-200 rounded-xl p-4">
          <p className="text-sm text-stone-500 italic mb-3">{results.explanation}</p>
          <div className="flex flex-col gap-3">
            {results.recommendations.map((r, i) => (
              <div key={i} className="flex justify-between items-start border-b border-stone-100 pb-2 last:border-0">
                <div>
                  <p className="font-semibold text-stone-800">{r.name}</p>
                  <p className="text-xs text-stone-400 italic">{r.reason}</p>
                </div>
                <span className="text-amber-600 font-bold text-sm">₹{r.price}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}