import jwtDecode from 'jwt-decode'

export function saveToken(t: string) { localStorage.setItem('token', t) }
export function getToken(): string | null { return localStorage.getItem('token') }
export function clearToken() { localStorage.removeItem('token') }
export function roleFromToken(t: string | null): string | null {
  if (!t) return null
  try { return (jwtDecode as any)(t).role || null } catch { return null }
}
