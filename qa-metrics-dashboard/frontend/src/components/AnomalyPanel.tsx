import React from 'react'

type Row = { ts: string; value: number; score: number }
export default function AnomalyPanel({ rows }: { rows: Row[] }) {
  if (!rows.length) return <div className="card">No anomalies detected.</div>
  return (
    <div className="card">
      <h3 className="text-lg mb-2">Detected Anomalies</h3>
      <ul className="list-disc pl-5 space-y-1">
        {rows.map((r, i) => (
          <li key={i}>{new Date(r.ts).toLocaleString()} — value {r.value} (score {r.score.toFixed(3)})</li>
        ))}
      </ul>
    </div>
  )
}
