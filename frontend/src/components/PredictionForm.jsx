import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'

const defaultInput = {
  brand: '',
  model: '',
  year: '',
  km_driven: '',
}

export default function PredictionForm() {
  const [input, setInput] = useState(defaultInput)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // optional: fetch car lists
    axios.get('/api/cars').then(r => {})
  }, [])

  const handlePredict = async () => {
    setLoading(true)
    try {
      const payload = {
        brand: input.brand,
        model: input.model,
        year: parseInt(input.year) || 2018,
        fuel: input.fuel,
        transmission: input.transmission,
        km_driven: parseInt(input.km_driven) || 20000,
        owner_count: parseInt(input.owner_count) || 1,
        engine_cc: parseInt(input.engine_cc) || 2000,
      }
      const r = await axios.post('/api/predict', payload)
      if (r.data.success) setResult(r.data.result)
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  return (
    <motion.div className="w-full max-w-3xl p-8 bg-gradient-to-br from-white/5 to-white/3 rounded-3xl backdrop-blur-lg shadow-2xl border border-white/5"
      initial={{ scale: 0.98, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.6 }}>
      <h2 className="text-2xl font-bold mb-4">Premium Price Prediction</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm opacity-80">Brand</label>
          <input placeholder="Enter car brand" value={input.brand} onChange={e => setInput({ ...input, brand: e.target.value })} className="p-3 bg-transparent border rounded-lg w-full" />
        </div>
        <div>
          <label className="text-sm opacity-80">Model</label>
          <input placeholder="Enter car model" value={input.model} onChange={e => setInput({ ...input, model: e.target.value })} className="p-3 bg-transparent border rounded-lg w-full" />
        </div>
        <div>
          <label className="text-sm opacity-80">Manufacturing Year</label>
          <input type="number" placeholder="Enter 4-digit year (e.g., 2018)" value={input.year} onChange={e => setInput({ ...input, year: e.target.value })} className="p-3 bg-transparent border rounded-lg w-full" />
        </div>
        <div>
          <label className="text-sm opacity-80">KM Driven</label>
          <input type="number" placeholder="Enter total kilometers driven (e.g., 45000)" value={input.km_driven} onChange={e => setInput({ ...input, km_driven: e.target.value })} className="p-3 bg-transparent border rounded-lg w-full" />
        </div>
      </div>
      <div className="mt-6 flex items-center gap-4">
        <button onClick={handlePredict} className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-400 rounded-full shadow-lg">{loading ? 'Predicting…' : 'Predict'}</button>
        {result && (
          <div className="ml-auto text-right">
            <div className="text-2xl font-bold">${result.predicted_value}</div>
            <div className="text-sm opacity-70">Range: ${result.lower_bound} — ${result.upper_bound}</div>
          </div>
        )}
      </div>
    </motion.div>
  )
}
