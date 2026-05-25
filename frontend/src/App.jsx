import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import Home from './pages/Home'
import Predict from './pages/Predict'
import Dashboard from './pages/Dashboard'
import About from './pages/About'

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white antialiased">
      <nav className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
        <div className="backdrop-blur-md bg-white/5 border border-white/5 rounded-full px-6 py-2 flex gap-6 items-center">
          <Link to="/" className="text-lg font-bold tracking-wide">AutoPulse</Link>
          <div className="flex gap-4">
            <Link to="/predict" className="opacity-80 hover:opacity-100">Predict</Link>
            <Link to="/dashboard" className="opacity-80 hover:opacity-100">Dashboard</Link>
            <Link to="/about" className="opacity-80 hover:opacity-100">About</Link>
          </div>
        </div>
      </nav>

      <motion.main initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </motion.main>
    </div>
  )
}
