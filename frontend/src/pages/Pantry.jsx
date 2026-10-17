import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import { useDebounce } from '../hooks/useDebounce'
import { getPantryItems, addPantryItem, deletePantryItem, searchIngredients } from '../api/pantry'

const UNITS = ['g', 'kg', 'ml', 'l', 'pcs', 'tbsp', 'tsp', 'cup']

export default function Pantry() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [selectedIngredient, setSelectedIngredient] = useState(null)
  const [quantity, setQuantity] = useState('')
  const [unit, setUnit] = useState('g')

  const debouncedQuery = useDebounce(query, 400)

  useEffect(() => {
    loadPantry()
  }, [])

  useEffect(() => {
    if (debouncedQuery.length < 2 || selectedIngredient) {
      setSuggestions([])
      return
    }
    searchIngredients(debouncedQuery).then(res => setSuggestions(res.data))
  }, [debouncedQuery])

  const loadPantry = async () => {
    setLoading(true)
    const res = await getPantryItems()
    setItems(res.data)
    setLoading(false)
  }

  const handleSelectSuggestion = (ingredient) => {
    setSelectedIngredient(ingredient)
    setQuery(ingredient.name)
    setSuggestions([])
  }

  const handleAdd = async (e) => {
    e.preventDefault()
    if (!selectedIngredient || !quantity) return

    await addPantryItem({
      ingredient_name: selectedIngredient.name,
      ingredient_id: selectedIngredient.id,
      quantity: parseFloat(quantity),
      unit,
    })

    setQuery('')
    setQuantity('')
    setSelectedIngredient(null)
    loadPantry()
  }

  const handleDelete = async (id) => {
    await deletePantryItem(id)
    loadPantry()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-2xl mx-auto p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Your Pantry</h1>

        <form onSubmit={handleAdd} className="bg-white p-6 rounded-xl shadow mb-8">
          <div className="flex gap-3 mb-3">
            <div className="flex-1 relative">
              <input
                type="text"
                placeholder="Search ingredient..."
                value={query}
                onChange={e => { setQuery(e.target.value); setSelectedIngredient(null) }}
                className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              {suggestions.length > 0 && (
                <ul className="absolute z-10 w-full bg-white border rounded-lg mt-1 shadow-lg max-h-48 overflow-y-auto">
                  {suggestions.map(s => (
                    <li
                      key={s.id}
                      onClick={() => handleSelectSuggestion(s)}
                      className="px-4 py-2 hover:bg-green-50 cursor-pointer text-sm"
                    >
                      {s.name}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <input
              type="number"
              placeholder="Qty"
              value={quantity}
              onChange={e => setQuantity(e.target.value)}
              className="w-24 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              step="0.1"
            />
            <select
              value={unit}
              onChange={e => setUnit(e.target.value)}
              className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {UNITS.map(u => <option key={u} value={u}>{u}</option>)}
            </select>
          </div>
          <button
            type="submit"
            disabled={!selectedIngredient || !quantity}
            className="bg-green-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Add to pantry
          </button>
        </form>

        {loading ? (
          <p className="text-gray-400">Loading pantry...</p>
        ) : items.length === 0 ? (
          <p className="text-gray-400">Your pantry is empty. Add your first ingredient above.</p>
        ) : (
          <ul className="bg-white rounded-xl shadow divide-y">
            {items.map(item => (
              <li key={item.id} className="flex items-center justify-between px-6 py-4">
                <div>
                  <p className="font-medium text-gray-900">{item.ingredient_name}</p>
                  <p className="text-sm text-gray-500">{item.quantity} {item.unit}</p>
                </div>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-sm text-gray-400 hover:text-red-500 transition-colors"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}