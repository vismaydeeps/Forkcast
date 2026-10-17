import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const location = useLocation()

  const linkClass = (path) =>
    `text-sm font-medium transition-colors ${
      location.pathname === path ? 'text-green-600' : 'text-gray-500 hover:text-gray-900'
    }`

  return (
    <nav className="bg-white border-b px-8 py-4">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-6">
          <span className="font-bold text-gray-900">Forkcast</span>
          <Link to="/" className={linkClass('/')}>Dashboard</Link>
          <Link to="/pantry" className={linkClass('/pantry')}>Pantry</Link>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-500">{user?.name}</span>
          <button onClick={logout} className="text-sm text-gray-400 hover:text-red-500 transition-colors">
            Sign out
          </button>
        </div>
      </div>
    </nav>
  )
}