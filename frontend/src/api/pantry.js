import api from './client'

export const getPantryItems = () => api.get('/pantry')
export const addPantryItem = (item) => api.post('/pantry', item)
export const deletePantryItem = (id) => api.delete(`/pantry/${id}`)
export const searchIngredients = (query) =>
  api.get('/pantry/ingredients/search', { params: { query } })