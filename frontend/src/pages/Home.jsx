import React from 'react'
import { motion } from 'framer-motion'
import Hero from '../components/Hero'
// removed live market stats
import Footer from '../components/Footer'

export default function Home() {
  return (
    <div>
      <Hero />
      <section className="py-24">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-extrabold mb-6">Features</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 bg-white/3 rounded-2xl backdrop-blur-md">build By Aaron Biju The Pro Developer</div>
            <div className="p-6 bg-white/3 rounded-2xl backdrop-blur-md">Accurate AI Valuations</div>
            <div className="p-6 bg-white/3 rounded-2xl backdrop-blur-md">Premium Analytics Dashboard</div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}
