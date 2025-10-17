import React from 'react'
import RoleGate from '../components/RoleGate'

export default function Settings() {
  return (
    <RoleGate allow={["admin"]}>
      <div className="card space-y-2">
        <h3 className="text-lg">Settings</h3>
        <p>Admin‑only area. Extend me with user management, API keys, etc.</p>
      </div>
    </RoleGate>
  )
}
