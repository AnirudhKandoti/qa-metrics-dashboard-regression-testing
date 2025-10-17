import React from 'react'
import { roleFromToken, getToken } from '../auth'

export default function RoleGate({ allow, children }: { allow: string[]; children: React.ReactNode }) {
  const role = roleFromToken(getToken())
  if (!role || !allow.includes(role)) return <div className="card">You do not have access.</div>
  return <>{children}</>
}
