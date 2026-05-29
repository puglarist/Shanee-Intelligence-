import { useState, useCallback } from 'react'

interface AuthState {
  token: string | null
  user: { username: string } | null
  loading: boolean
  error: string | null
}

export function useAuth() {
  const [auth, setAuth] = useState<AuthState>(() => ({
    token: localStorage.getItem('token'),
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
    loading: false,
    error: null
  }))

  const login = useCallback(async (username: string, password: string) => {
    setAuth(prev => ({ ...prev, loading: true, error: null }))
    try {
      const response = await fetch('/api/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data = await response.json()
      const user = { username }

      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(user))

      setAuth({
        token: data.access_token,
        user,
        loading: false,
        error: null
      })
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed'
      setAuth(prev => ({ ...prev, loading: false, error: message }))
    }
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setAuth({
      token: null,
      user: null,
      loading: false,
      error: null
    })
  }, [])

  return {
    ...auth,
    login,
    logout
  }
}
