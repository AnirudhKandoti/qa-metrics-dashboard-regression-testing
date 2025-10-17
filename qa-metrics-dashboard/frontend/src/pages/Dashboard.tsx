import React, { useEffect, useState } from 'react'
import { api } from '../api'
import MetricChart from '../components/MetricChart'
import AnomalyPanel from '../components/AnomalyPanel'

export default function Dashboard() {
  const [series, setSeries] = useState<{ ts: string; value: number }[]>([])
  const [anoms, setAnoms] = useState<{ ts: string; value: number; score: number }[]>([])

  const pipeline = 'webapp'
  const name = 'tests.pass_rate'

  useEffect(() => {
    (async () => {
      const s = await api.post('/metrics/series', { pipeline, name })
      setSeries(s.data.points)
      const a = await api.post('/anomalies/detect', { pipeline, name })
      setAnoms(a.data)
    })()
  }, [])

  const merged = series.map(pt => ({ ...pt, ts: new Date(pt.ts).toISOString(), anomaly: anoms.some(a => a.ts === pt.ts) }))

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div className="md:col-span-2"><MetricChart data={merged} title={`${pipeline} · ${name}`} /></div>
      <AnomalyPanel rows={anoms} />
    </div>
  )
}
