import React from 'react'

export default function About() {
  return (
    <div className="container mx-auto px-6 py-24">
      <h1 className="text-4xl font-extrabold mb-6">About AutoPulse</h1>
      <p className="text-lg">AutoPulse uses a RandomForest model trained on curated car data to estimate market values. Input the brand, model, year and kilometers driven — the AI returns a predicted value with a confidence range. Predictions are stored locally for analytics.</p>
    </div>
  )
}
