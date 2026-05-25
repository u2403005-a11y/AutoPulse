import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    axios.get('/api/stats').then(r => setStats(r.data)).catch(() => {})
  }, [])

  const data = stats ? stats.popular_brands.map(b => ({ name: b.brand, count: b.count })) : []

  return (
    <div className="container mx-auto px-6 py-24">
      <h1 className="text-4xl font-extrabold mb-6">Analytics Dashboard</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="p-6 bg-white/3 rounded-2xl backdrop-blur-md">
          <h3 className="text-xl font-semibold mb-4">Popular Brands</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={data}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="p-6 bg-white/3 rounded-2xl backdrop-blur-md">
          <h3 className="text-xl font-semibold mb-4">Overview</h3>
          <div className="space-y-4">
            <div>Total analyzed: {stats?.total ?? '—'}</div>
            <div>Average value: ${stats?.average ?? '—'}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
