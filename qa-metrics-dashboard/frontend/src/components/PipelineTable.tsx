import React from 'react'

type Pipeline = { id: number; name: string; description?: string }
export default function PipelineTable({ items }: { items: Pipeline[] }) {
  return (
    <div className="card overflow-x-auto">
      <table className="min-w-full">
        <thead>
          <tr><th className="text-left p-2">Name</th><th className="text-left p-2">Description</th></tr>
        </thead>
        <tbody>
          {items.map(p => (
            <tr key={p.id} className="border-t">
              <td className="p-2 font-medium">{p.name}</td>
              <td className="p-2">{p.description || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
