import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import SecureArea from './pages/SecureArea'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
        <nav className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <Link to="/" className="text-2xl font-bold text-cyan-400">
              Shanee Intelligence
            </Link>
            <div className="flex gap-6">
              <Link to="/" className="hover:text-cyan-300 transition">Home</Link>
              <Link to="/dashboard" className="hover:text-cyan-300 transition">Dashboard</Link>
              <Link to="/secure" className="hover:text-cyan-300 transition">Secure Area</Link>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/secure" element={<SecureArea />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
