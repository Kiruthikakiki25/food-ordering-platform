import { useState, useEffect } from "react"
import axios from "../api/client"

export default function IngredientPanel({ itemId, itemName }) {
  const [data, setData] = useState(null)
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!itemId) return
    setData(null)
    setAnswer("")
    axios.get(`/api/menu/${itemId}/ingredients`)
      .then(r => setData(r.data))
      .catch(() => setData(null))
  }, [itemId])

  const askQuestion = async () => {
    if (!question.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`/api/menu/${itemId}/ask`, { question })
      setAnswer(res.data.answer)
    } catch {
      setAnswer("Sorry, couldn't get an answer right now.")
    }
    setLoading(false)
  }

  if (!data) return <p className="text-sm text-stone-400">Loading ingredients...</p>

  return (
    <div className="mt-4 bg-orange-50 rounded-xl p-4 border border-stone-200">
      {/* Nutrition bar */}
      {data.calories && (
        <div className="flex gap-4 text-xs text-stone-600 mb-3 flex-wrap">
          <span className="font-semibold text-red-900">{data.calories} kcal</span>
          {data.nutrition?.protein && <span>Protein: {data.nutrition.protein}g</span>}
          {data.nutrition?.carbs   && <span>Carbs: {data.nutrition.carbs}g</span>}
          {data.nutrition?.fat     && <span>Fat: {data.nutrition.fat}g</span>}
          {data.nutrition?.fiber   && <span>Fiber: {data.nutrition.fiber}g</span>}
        </div>
      )}

      {/* Ingredient tags */}
      <div className="flex flex-wrap gap-2 mb-3">
        {data.ingredients.map((ing, i) => (
          <span
            key={i}
            className={`text-xs px-2 py-1 rounded-full border ${
              ing.flagged_for_user
                ? "bg-red-100 border-red-400 text-red-700 font-semibold"
                : "bg-white border-stone-300 text-stone-600"
            }`}
          >
            {ing.name}
            {ing.allergen_flags?.length > 0 && (
              <span className="ml-1 text-amber-600">⚠ {ing.allergen_flags.join(", ")}</span>
            )}
          </span>
        ))}
      </div>

      {/* Ask anything */}
      <div className="flex gap-2 mt-2">
        <input
          className="flex-1 border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
          placeholder='e.g. "Is this safe for a diabetic?"'
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === "Enter" && askQuestion()}
        />
        <button
          onClick={askQuestion}
          disabled={loading}
          className="bg-red-900 text-white text-sm px-4 py-2 rounded-lg hover:bg-red-800 disabled:opacity-50"
        >
          {loading ? "..." : "Ask AI"}
        </button>
      </div>
      {answer && (
        <p className="mt-3 text-sm text-stone-700 bg-white border border-stone-200 rounded-lg p-3">
          {answer}
        </p>
      )}
    </div>
  )
}