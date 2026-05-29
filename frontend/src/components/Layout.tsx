import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-900">
      <nav className="bg-gray-800 border-b border-cyan-500/20 px-6 py-4">
        <div className="flex justify-between items-center max-w-7xl mx-auto">
          <div className="flex items-center gap-8">
            <Link to="/" className="text-2xl font-bold text-cyan-500">
              Shanee Intelligence
            </Link>
            <div className="hidden md:flex gap-6">
              <Link to="/" className="text-gray-300 hover:text-cyan-400 transition">Home</Link>
              <Link to="/dashboard" className="text-gray-300 hover:text-cyan-400 transition">Dashboard</Link>
              {user && (
                <Link to="/secure" className="text-gray-300 hover:text-cyan-400 transition">Secure Area</Link>
              )}
            </div>
          </div>
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <span className="text-sm text-gray-400">Welcome, {user.username}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link to="/login" className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded transition">
                Login
              </Link>
            )}
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
        <Outlet />
      </main>

      <footer className="bg-gray-800 border-t border-cyan-500/20 px-6 py-4 text-center text-gray-500 text-sm">
        <p>&copy; 2024 Shanee Intelligence. Privacy-focused GPU-accelerated platform.</p>
      </footer>
    </div>
  )
}
