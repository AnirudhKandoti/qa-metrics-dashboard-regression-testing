import React, { useState } from 'react'
import LoginForm from './components/LoginForm'
import { getToken, clearToken, roleFromToken } from './auth'
import Dashboard from './pages/Dashboard'
import Pipelines from './pages/Pipelines'
import Settings from './pages/Settings'

export default function App() {
  const [_, setTick] = useState(0)
  const token = getToken()
  const role = roleFromToken(token)
  if (!token) return <LoginForm onLogin={() => setTick(x=>x+1)} />

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-4">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">QA Metrics Dashboard</h1>
        <div className="space-x-2 text-sm">
          <span className="opacity-80">{role}</span>
          <button className="px-2 py-1 rounded bg-neutral-700 text-white" onClick={()=>{clearToken(); location.reload()}}>Logout</button>
        </div>
      </header>
      <nav className="flex gap-2">
        <a href="#/" className="px-2 py-1 rounded bg-neutral-200 dark:bg-neutral-700">Dashboard</a>
        <a href="#/pipelines" className="px-2 py-1 rounded bg-neutral-200 dark:bg-neutral-700">Pipelines</a>
        <a href="#/settings" className="px-2 py-1 rounded bg-neutral-200 dark:bg-neutral-700">Settings</a>
      </nav>
      <main>
        {location.hash === '#/pipelines' ? <Pipelines/> : location.hash === '#/settings' ? <Settings/> : <Dashboard/>}
      </main>
    </div>
  )
}
