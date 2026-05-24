import { useState, useEffect } from 'react'

interface SystemStatus {
  api_online: boolean
  gpu_available: boolean
  message: string
}

export default function Dashboard() {
  const [status, setStatus] = useState<SystemStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/status')
        const data = await response.json()
        setStatus(data)
      } catch (err) {
        setError('Failed to fetch system status')
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
  }, [])

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          {loading && <p className="text-slate-400">Loading...</p>}
          {error && <p className="text-red-400">{error}</p>}
          {status && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-slate-300">API Status</span>
                <span className={status.api_online ? 'text-green-400' : 'text-red-400'}>
                  {status.api_online ? '✓ Online' : '✗ Offline'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-300">GPU Available</span>
                <span className={status.gpu_available ? 'text-green-400' : 'text-yellow-400'}>
                  {status.gpu_available ? '✓ Yes' : '⚠ No'}
                </span>
              </div>
              <p className="text-slate-400 text-sm mt-4">{status.message}</p>
            </div>
          )}
        </div>

        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-300">Active Sessions</span>
              <span className="text-cyan-400">0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">Compute Jobs</span>
              <span className="text-cyan-400">0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">Storage Used</span>
              <span className="text-cyan-400">0 MB</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <p className="text-slate-400">No recent activity</p>
      </div>
    </div>
  )
}
