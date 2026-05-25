import React from 'react'

export default function StatsSection() {
  return (
    <section className="py-12">
      <div className="container mx-auto px-6">
        <h3 className="text-3xl font-bold mb-6">Live Market Stats</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-6 bg-white/3 rounded-2xl">Total Analyses: <strong>1,234</strong></div>
          <div className="p-6 bg-white/3 rounded-2xl">Avg. Value: <strong>$42,300</strong></div>
          <div className="p-6 bg-white/3 rounded-2xl">Top Brand: <strong>Tesla</strong></div>
        </div>
      </div>
    </section>
  )
}
