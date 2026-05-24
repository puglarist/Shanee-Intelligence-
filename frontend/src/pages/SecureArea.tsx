import { useState } from 'react'

export default function SecureArea() {
  const [token, setToken] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (token.trim()) {
      setIsAuthenticated(true)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="max-w-md mx-auto bg-slate-800 p-8 rounded-lg border border-slate-700">
          <h1 className="text-3xl font-bold mb-6 text-center">Secure Area</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-slate-300 mb-2">Authentication Token</label>
              <input
                type="password"
                placeholder="Enter your token"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-cyan-500 hover:bg-cyan-600 rounded font-semibold transition"
            >
              Authenticate
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">Secure Area</h1>
        <button
          onClick={() => {
            setIsAuthenticated(false)
            setToken('')
          }}
          className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded transition"
        >
          Logout
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-slate-800 p-6 rounded-lg border border-cyan-500">
          <h2 className="text-xl font-semibold mb-4 text-cyan-400">🔒 File Management</h2>
          <p className="text-slate-300 mb-4">Upload and manage encrypted files</p>
          <button className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 rounded transition">
            Upload File
          </button>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg border border-cyan-500">
          <h2 className="text-xl font-semibold mb-4 text-cyan-400">⚙️ Compute Jobs</h2>
          <p className="text-slate-300 mb-4">Submit and monitor GPU compute jobs</p>
          <button className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 rounded transition">
            New Job
          </button>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg border border-cyan-500">
          <h2 className="text-xl font-semibold mb-4 text-cyan-400">🔗 Integrations</h2>
          <p className="text-slate-300 mb-4">Connect to GitHub, cloud storage, and services</p>
          <button className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 rounded transition">
            Connect Service
          </button>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg border border-cyan-500">
          <h2 className="text-xl font-semibold mb-4 text-cyan-400">📊 Analytics</h2>
          <p className="text-slate-300 mb-4">View security logs and activity reports</p>
          <button className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 rounded transition">
            View Reports
          </button>
        </div>
      </div>
    </div>
  )
}
