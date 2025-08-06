'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  HeartIcon, 
  MoonIcon, 
  UserGroupIcon, 
  TargetIcon,
  PuzzlePieceIcon,
  FaceSmileIcon 
} from '@heroicons/react/24/outline'

interface WelcomeScreenProps {
  onComplete: (data: { wellnessFocus: string }) => void
  platform: 'web' | 'ios' | 'android'
}

const wellnessFocusOptions = [
  {
    id: 'stress-anxiety',
    title: 'Stress & Anxiety',
    description: 'Find calm in daily chaos',
    icon: HeartIcon,
    color: 'from-blue-500 to-purple-500'
  },
  {
    id: 'depression-support',
    title: 'Depression Support',
    description: 'Professional guidance & community',
    icon: FaceSmileIcon,
    color: 'from-purple-500 to-pink-500'
  },
  {
    id: 'sleep-rest',
    title: 'Sleep & Rest',
    description: 'Better nights, brighter days',
    icon: MoonIcon,
    color: 'from-indigo-500 to-blue-500'
  },
  {
    id: 'general-wellness',
    title: 'General Wellness',
    description: 'Overall mental health maintenance',
    icon: TargetIcon,
    color: 'from-green-500 to-teal-500'
  },
  {
    id: 'relationship-health',
    title: 'Relationship Health',
    description: 'Stronger connections, better communication',
    icon: UserGroupIcon,
    color: 'from-teal-500 to-cyan-500'
  },
  {
    id: 'personal-growth',
    title: 'Personal Growth',
    description: 'Unlock your potential',
    icon: PuzzlePieceIcon,
    color: 'from-orange-500 to-red-500'
  }
]

export function WelcomeScreen({ onComplete, platform }: WelcomeScreenProps) {
  const [selectedFocus, setSelectedFocus] = useState<string>('')
  const [showOptions, setShowOptions] = useState(false)

  const handleContinue = () => {
    if (selectedFocus) {
      onComplete({ wellnessFocus: selectedFocus })
    }
  }

  const handleSkip = () => {
    onComplete({ wellnessFocus: 'general-wellness' })
  }

  return (
    <div className="min-h-screen flex flex-col justify-center px-4 py-8">
      <div className="max-w-2xl mx-auto text-center">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="mb-8">
            <motion.div
              className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-secondary-400 to-accent-400 flex items-center justify-center"
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
            >
              <span className="text-4xl">🌱</span>
            </motion.div>
            
            <h1 className="text-h1 font-bold text-neutral-900 mb-4">
              Welcome to Your Wellness Journey
            </h1>
            
            <p className="text-body-lg text-neutral-600 mb-8 max-w-lg mx-auto">
              Let's personalize your experience. Choose your primary wellness focus to get started with tailored recommendations.
            </p>
          </div>
        </motion.div>

        {/* Wellness Focus Options */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            {wellnessFocusOptions.map((option, index) => {
              const IconComponent = option.icon
              return (
                <motion.button
                  key={option.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * index, duration: 0.4 }}
                  onClick={() => {
                    setSelectedFocus(option.id)
                    setShowOptions(true)
                  }}
                  className={`p-6 rounded-2xl text-left transition-all duration-300 hover:scale-105 active:scale-95 ${
                    selectedFocus === option.id
                      ? 'bg-white shadow-healing border-2 border-secondary-300'
                      : 'bg-white/60 hover:bg-white shadow-soft border border-neutral-200'
                  }`}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${option.color} flex items-center justify-center flex-shrink-0`}>
                      <IconComponent className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-h3 font-semibold text-neutral-900 mb-1">
                        {option.title}
                      </h3>
                      <p className="text-body-sm text-neutral-600">
                        {option.description}
                      </p>
                    </div>
                    {selectedFocus === option.id && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6 rounded-full bg-secondary-500 flex items-center justify-center"
                      >
                        <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </motion.div>
                    )}
                  </div>
                </motion.button>
              )
            })}
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <button
            onClick={handleContinue}
            disabled={!selectedFocus}
            className={`btn-primary px-8 py-4 text-lg ${
              !selectedFocus ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            Continue
          </button>
          <button
            onClick={handleSkip}
            className="btn-ghost px-8 py-4 text-lg"
          >
            Skip - I'll explore first
          </button>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.4 }}
          className="mt-12 p-4 bg-blue-50 rounded-xl border border-blue-200"
        >
          <p className="text-body-sm text-blue-800">
            <span className="font-semibold">Important:</span> This platform provides wellness support and is NOT a licensed therapist or mental health professional. 
            For emergency situations, please call 988 (Suicide & Crisis Lifeline) or your local emergency services.
          </p>
        </motion.div>
      </div>
    </div>
  )
}
