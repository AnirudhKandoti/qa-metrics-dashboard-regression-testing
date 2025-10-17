import React, { useEffect, useState } from 'react'
import { api } from '../api'
import PipelineTable from '../components/PipelineTable'

export default function Pipelines() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { (async ()=>{ const r = await api.get('/pipelines/'); setItems(r.data) })() }, [])
  return <PipelineTable items={items} />
}
