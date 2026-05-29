import { useEffect, useState } from 'react'

interface SystemStatus {
  status: string
  timestamp: string
  version: string
  services: Record<string, string>
}

export default function Dashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/status')
        if (!response.ok) throw new Error('Failed to fetch status')
        const data = await response.json()
        setSystemStatus(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error fetching status')
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold text-white mb-4">System Dashboard</h1>
        <p className="text-gray-400">Real-time system monitoring and metrics</p>
      </section>

      {loading ? (
        <div className="text-center py-12 text-gray-400">
          <p>Loading system status...</p>
        </div>
      ) : error ? (
        <div className="p-4 bg-red-900/30 border border-red-500/50 rounded text-red-300">
          {error}
        </div>
      ) : systemStatus ? (
        <div className="space-y-6">
          <div className="grid md:grid-cols-4 gap-4">
            <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
              <div className="text-sm text-gray-400 mb-2">Status</div>
              <div className="text-2xl font-bold">
                <span className="text-green-400">●</span> {systemStatus.status}
              </div>
            </div>

            <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
              <div className="text-sm text-gray-400 mb-2">Version</div>
              <div className="text-2xl font-bold text-cyan-400">{systemStatus.version}</div>
            </div>

            <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
              <div className="text-sm text-gray-400 mb-2">Services</div>
              <div className="text-2xl font-bold text-cyan-400">
                {Object.keys(systemStatus.services).length}
              </div>
            </div>

            <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
              <div className="text-sm text-gray-400 mb-2">Last Updated</div>
              <div className="text-sm text-cyan-400">
                {new Date(systemStatus.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
            <h2 className="text-xl font-bold text-white mb-4">Services</h2>
            <div className="space-y-2">
              {Object.entries(systemStatus.services).map(([service, status]) => (
                <div key={service} className="flex justify-between items-center p-3 bg-gray-700/50 rounded">
                  <span className="text-gray-300 font-medium">{service}</span>
                  <span className={`text-sm ${status === 'running' ? 'text-green-400' : 'text-red-400'}`}>
                    {status === 'running' ? '✓' : '✗'} {status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
