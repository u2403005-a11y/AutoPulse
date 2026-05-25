import React from 'react'
import PredictionForm from '../components/PredictionForm'
import Footer from '../components/Footer'

export default function Predict() {
  return (
    <div className="min-h-screen flex items-center justify-center py-24">
      <PredictionForm />
      <Footer />
    </div>
  )
}
