'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface QuickAssessmentProps {
  onComplete: (data: { moodLevel: number; challenge: string }) => void
  wellnessFocus: string
}

export function QuickAssessment({ onComplete, wellnessFocus }: QuickAssessmentProps) {
  const [moodLevel, setMoodLevel] = useState(5)
  const [challenge, setChallenge] = useState('')
  const [showRecommendation, setShowRecommendation] = useState(false)

  const moodEmojis = ['😢', '😞', '😐', '🙂', '😊', '😄']
  const moodLabels = ['Very Sad', 'Sad', 'Okay', 'Good', 'Happy', 'Very Happy']

  const handleContinue = () => {
    setShowRecommendation(true)
    setTimeout(() => {
      onComplete({ moodLevel, challenge })
    }, 2000)
  }

  if (showRecommendation) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md mx-auto text-center"
        >
          <motion.div
            className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-accent-400 to-secondary-400 flex items-center justify-center"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, ease: "easeInOut" }}
          >
            <span className="text-3xl">✨</span>
          </motion.div>
          
          <h2 className="text-h2 font-bold text-neutral-900 mb-4">
            Personalized Recommendation Ready!
          </h2>
          
          <p className="text-body text-neutral-600 mb-6">
            Based on your responses, we've prepared a perfect wellness activity for you.
          </p>
          
          <div className="animate-pulse">
            <div className="w-full h-2 bg-secondary-200 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-secondary-500 rounded-full"
                initial={{ width: '0%' }}
                animate={{ width: '100%' }}
                transition={{ duration: 2 }}
              />
            </div>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col justify-center px-4 py-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-h1 font-bold text-neutral-900 mb-4">
            Quick Wellness Check-In
          </h1>
          <p className="text-body-lg text-neutral-600">
            Help us understand how you're feeling right now so we can provide the best support.
          </p>
        </motion.div>

        {/* Mood Scale */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-8 mb-8"
        >
          <h2 className="text-h2 font-semibold text-neutral-900 mb-6 text-center">
            How are you feeling right now?
          </h2>

          {/* Mood Slider */}
          <div className="relative mb-6">
            <div className="flex justify-between items-center mb-4">
              {moodEmojis.map((emoji, index) => (
                <motion.button
                  key={index}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setMoodLevel(index + 1)}
                  className={`w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300 ${
                    moodLevel === index + 1
                      ? 'bg-secondary-100 scale-110 shadow-lg'
                      : 'hover:bg-neutral-100'
                  }`}
                >
                  {emoji}
                </motion.button>
              ))}
            </div>

            {/* Slider Track */}
            <div className="relative">
              <div className="w-full h-3 bg-gradient-to-r from-red-200 via-yellow-200 to-green-200 rounded-full"></div>
              <motion.div
                className="absolute top-0 w-6 h-6 bg-white border-4 border-secondary-500 rounded-full shadow-lg cursor-pointer"
                style={{
                  left: `calc(${((moodLevel - 1) / 5) * 100}% - 12px)`,
                }}
                drag="x"
                dragConstraints={{ left: 0, right: 0 }}
                onDrag={(_, info) => {
                  const slider = info.point.x / (window.innerWidth * 0.8)
                  const newMood = Math.max(1, Math.min(6, Math.round(slider * 5) + 1))
                  setMoodLevel(newMood)
                }}
                whileDrag={{ scale: 1.2 }}
              />
            </div>

            <div className="text-center mt-4">
              <span className="text-h3 font-medium text-neutral-800">
                {moodLabels[moodLevel - 1]}
              </span>
              <div className="text-body-sm text-neutral-500">
                {moodLevel}/6
              </div>
            </div>
          </div>
        </motion.div>

        {/* Challenge Input */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-8 mb-8"
        >
          <h2 className="text-h2 font-semibold text-neutral-900 mb-4">
            What's your biggest wellness challenge today?
          </h2>
          
          <div className="relative">
            <textarea
              value={challenge}
              onChange={(e) => setChallenge(e.target.value)}
              placeholder="Share what's on your mind... (optional)"
              className="input-wellness min-h-[120px] resize-none"
              maxLength={200}
            />
            <div className="absolute bottom-3 right-3 text-body-sm text-neutral-400">
              {challenge.length}/200
            </div>
          </div>

          {/* AI Suggestions */}
          {challenge.length > 10 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-4 p-4 bg-accent-50 rounded-xl border border-accent-200"
            >
              <p className="text-body-sm text-accent-800 font-medium mb-2">
                AI Insight:
              </p>
              <p className="text-body-sm text-accent-700">
                Based on your input, I recommend starting with a breathing exercise to help center yourself.
              </p>
            </motion.div>
          )}
        </motion.div>

        {/* Continue Button */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-center"
        >
          <button
            onClick={handleContinue}
            className="btn-primary px-12 py-4 text-lg"
          >
            Get My Personalized Recommendation
          </button>
        </motion.div>
      </div>
    </div>
  )
}
