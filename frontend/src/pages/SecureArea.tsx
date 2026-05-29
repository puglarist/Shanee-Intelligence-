import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'

interface UserInfo {
  username: string
  role: string
  createdAt: string
}

export default function SecureArea() {
  const { token } = useAuth()
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        if (!token) throw new Error('No authentication token')

        const response = await fetch('/api/user/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) throw new Error('Failed to fetch user info')
        const data = await response.json()
        setUserInfo(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error fetching user info')
      } finally {
        setLoading(false)
      }
    }

    fetchUserInfo()
  }, [token])

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold text-white mb-2">Secure Area</h1>
        <p className="text-gray-400">This area is only accessible to authenticated users</p>
      </section>

      {loading ? (
        <div className="text-center py-12 text-gray-400">
          <p>Loading user information...</p>
        </div>
      ) : error ? (
        <div className="p-4 bg-red-900/30 border border-red-500/50 rounded text-red-300">
          {error}
        </div>
      ) : userInfo ? (
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-lg p-8 border border-cyan-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">User Profile</h2>

            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400">Username</label>
                <p className="text-xl font-semibold text-cyan-400">{userInfo.username}</p>
              </div>

              <div>
                <label className="text-sm text-gray-400">Role</label>
                <p className="text-lg text-gray-300">{userInfo.role}</p>
              </div>

              <div>
                <label className="text-sm text-gray-400">Account Created</label>
                <p className="text-lg text-gray-300">
                  {new Date(userInfo.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20">
            <h3 className="text-lg font-bold text-white mb-4">Secure Features</h3>
            <ul className="space-y-2 text-gray-300">
              <li>✓ Access to authenticated API endpoints</li>
              <li>✓ User profile and account management</li>
              <li>✓ Advanced monitoring and analytics</li>
              <li>✓ Secure data operations</li>
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  )
}
