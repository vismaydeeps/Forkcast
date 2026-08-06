import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.name}
          </h1>
          <button
            onClick={logout}
            className="text-sm text-gray-500 hover:text-red-500 transition-colors"
          >
            Sign out
          </button>
        </div>
        <p className="text-gray-500">Pantry and meal plan coming in Week 2.</p>
      </div>
    </div>
  )
}