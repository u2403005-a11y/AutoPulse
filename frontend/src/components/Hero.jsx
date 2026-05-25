import React from 'react'
import { motion } from 'framer-motion'

export default function Hero() {
  return (
    <section className="h-screen flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-black to-black opacity-60" />
      <motion.div className="relative z-10 text-center px-6" initial={{ y: 40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.9 }}>
        <h1 className="text-6xl font-extrabold tracking-tight leading-tight">AI Powered Used Car Valuation</h1>
        <p className="mt-6 text-xl opacity-80">Cinematic. Premium. Accurate.</p>
      </motion.div>
    </section>
  )
}
