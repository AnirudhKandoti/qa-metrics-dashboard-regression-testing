import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceDot } from 'recharts'

type Pt = { ts: string; value: number; anomaly?: boolean }
export default function MetricChart({ data, title }: { data: Pt[]; title: string }) {
  return (
    <div className="card">
      <h3 className="text-lg mb-2">{title}</h3>
      <div style={{ width: '100%', height: 280 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <XAxis dataKey="ts" tick={false} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" dot={false} />
            {data.filter(d=>d.anomaly).map((d,i)=> (
              <ReferenceDot key={i} x={d.ts} y={d.value} r={5} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
