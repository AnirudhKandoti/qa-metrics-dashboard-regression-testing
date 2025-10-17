import axios from 'axios'
import { getToken } from './auth'

export const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE })
api.interceptors.request.use((cfg) => {
  const t = getToken()
  if (t) cfg.headers = { ...cfg.headers, Authorization: `Bearer ${t}` }
  return cfg
})
