import React, { useState } from 'react'
import { api } from '../api'
import { saveToken } from '../auth'

export default function LoginForm({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('Admin@12345')
  const [err, setErr] = useState<string | null>(null)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErr(null)
    try {
      const r = await api.post('/auth/token', { email, password })
      saveToken(r.data.access_token)
      onLogin()
    } catch (e: any) {
      setErr(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <form onSubmit={submit} className="card max-w-md mx-auto space-y-3">
      <h2 className="text-xl font-semibold">Sign in</h2>
      {err && <div className="text-red-500">{err}</div>}
      <input className="w-full p-2 rounded border" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
      <input className="w-full p-2 rounded border" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" />
      <button className="px-3 py-2 rounded bg-blue-600 text-white">Login</button>
    </form>
  )
}
