'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { CheckIcon, ShieldCheckIcon, UsersIcon, ChartBarIcon, HeartIcon } from '@heroicons/react/24/outline'

interface RegistrationPromptProps {
  onComplete: (data: { registered: boolean; email?: string; guestMode?: boolean }) => void
  improvementScore: number
  completedActivity: boolean
}

export function RegistrationPrompt({ onComplete, improvementScore, completedActivity }: RegistrationPromptProps) {
  const [email, setEmail] = useState('')
  const [showGuestInfo, setShowGuestInfo] = useState(false)
  const [agreedToTerms, setAgreedToTerms] = useState(false)

  const benefits = [
    {
      icon: ChartBarIcon,
      title: 'Track your wellness journey over time',
      description: 'See your progress and identify patterns'
    },
    {
      icon: HeartIcon,
      title: 'Get personalized recommendations',
      description: 'AI-powered insights tailored just for you'
    },
    {
      icon: UsersIcon,
      title: 'Connect with supportive community',
      description: 'Find accountability partners and peer support'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Access advanced wellness tools',
      description: 'Crisis support, goal setting, and expert content'
    }
  ]

  const handleSaveProgress = () => {
    if (email && agreedToTerms) {
      onComplete({ registered: true, email })
    }
  }

  const handleGuestMode = () => {
    onComplete({ registered: false, guestMode: true })
  }

  const handleContinueExploring = () => {
    setShowGuestInfo(true)
  }

  if (showGuestInfo) {
    return (
      <div className="min-h-screen flex flex-col justify-center px-4 py-8">
        <div className="max-w-2xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-orange-400 to-red-400 flex items-center justify-center">
              <span className="text-3xl">🏃‍♀️</span>
            </div>
            
            <h1 className="text-h1 font-bold text-neutral-900 mb-4">
              Continue in Guest Mode
            </h1>
            
            <p className="text-body-lg text-neutral-600 mb-8">
              You can explore our platform for the next 3 days without registering. 
              Here's what you can access:
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-green-50 rounded-2xl p-6 border border-green-200"
            >
              <h3 className="text-h3 font-semibold text-green-800 mb-4">✅ Available Now</h3>
              <ul className="space-y-2 text-body-sm text-green-700">
                <li>• All wellness activities</li>
                <li>• Basic mood tracking</li>
                <li>• Community browsing</li>
                <li>• Crisis support resources</li>
                <li>• Guest progress tracking</li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-amber-50 rounded-2xl p-6 border border-amber-200"
            >
              <h3 className="text-h3 font-semibold text-amber-800 mb-4">⏳ Locked After 3 Days</h3>
              <ul className="space-y-2 text-body-sm text-amber-700">
                <li>• Personalized insights</li>
                <li>• Community participation</li>
                <li>• Progress history</li>
                <li>• Advanced AI coaching</li>
                <li>• Goal tracking</li>
              </ul>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="bg-blue-50 rounded-2xl p-6 border border-blue-200 mb-8"
          >
            <div className="flex items-center justify-center space-x-2 mb-2">
              <ShieldCheckIcon className="w-5 h-5 text-blue-600" />
              <span className="font-semibold text-blue-800">Privacy Promise</span>
            </div>
            <p className="text-body-sm text-blue-700">
              Your guest activities are stored locally and will be preserved if you decide to register within 3 days.
              You maintain full control over your data.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={handleGuestMode}
              className="btn-primary px-8 py-4 text-lg"
            >
              Start 3-Day Trial
            </button>
            <button
              onClick={() => setShowGuestInfo(false)}
              className="btn-outline px-8 py-4 text-lg"
            >
              Back to Registration
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col justify-center px-4 py-8">
      <div className="max-w-2xl mx-auto">
        {/* Success Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-accent-400 to-secondary-400 flex items-center justify-center"
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 2, ease: "easeInOut" }}
          >
            <span className="text-4xl">🎉</span>
          </motion.div>
          
          <h1 className="text-h1 font-bold text-neutral-900 mb-4">
            Amazing! You just improved your wellness score by {improvementScore}%
          </h1>
          
          <div className="bg-gradient-to-r from-accent-100 to-secondary-100 rounded-2xl p-6 mb-6">
            <div className="flex items-center justify-center space-x-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-neutral-900">{85}%</div>
                <div className="text-body-sm text-neutral-600">Before</div>
              </div>
              <div className="text-2xl text-neutral-400">→</div>
              <div className="text-center">
                <div className="text-2xl font-bold text-accent-600">{85 + improvementScore}%</div>
                <div className="text-body-sm text-neutral-600">After</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Benefits Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-h2 font-semibold text-neutral-900 mb-6 text-center">
            🎯 Save your progress to:
          </h2>
          
          <div className="space-y-4">
            {benefits.map((benefit, index) => {
              const IconComponent = benefit.icon
              return (
                <motion.div
                  key={benefit.title}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * index }}
                  className="flex items-start space-x-4 p-4 bg-white rounded-xl border border-neutral-200 hover:shadow-soft transition-shadow"
                >
                  <div className="w-10 h-10 rounded-lg bg-secondary-100 flex items-center justify-center flex-shrink-0">
                    <IconComponent className="w-5 h-5 text-secondary-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-neutral-900 mb-1">
                      {benefit.title}
                    </h3>
                    <p className="text-body-sm text-neutral-600">
                      {benefit.description}
                    </p>
                  </div>
                  <CheckIcon className="w-5 h-5 text-accent-500 flex-shrink-0 mt-1" />
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Registration Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-8 mb-6"
        >
          <div className="space-y-6">
            <div>
              <label className="block text-body font-medium text-neutral-700 mb-2">
                Email Address (optional - you can also use guest mode)
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                className="input-wellness"
              />
            </div>

            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={agreedToTerms}
                onChange={(e) => setAgreedToTerms(e.target.checked)}
                className="mt-1 w-4 h-4 text-secondary-600 border-2 border-neutral-300 rounded focus:ring-secondary-500"
              />
              <div className="flex-1">
                <span className="text-body-sm text-neutral-700">
                  I agree to the{' '}
                  <a href="/terms" className="text-secondary-600 hover:text-secondary-700 underline">
                    Terms of Service
                  </a>
                  {' '}and{' '}
                  <a href="/privacy" className="text-secondary-600 hover:text-secondary-700 underline">
                    Privacy Policy
                  </a>
                </span>
                <div className="text-body-sm text-neutral-500 mt-1">
                  🔒 We respect your privacy - you control your data
                </div>
              </div>
            </label>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-4"
        >
          <button
            onClick={handleSaveProgress}
            disabled={!agreedToTerms || !email}
            className={`btn-primary flex-1 px-8 py-4 text-lg ${
              !agreedToTerms || !email ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            Save My Progress
          </button>
          <button
            onClick={handleContinueExploring}
            className="btn-outline flex-1 px-8 py-4 text-lg"
          >
            Continue Exploring First
          </button>
        </motion.div>

        {/* Privacy Notice */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 p-4 bg-neutral-50 rounded-xl border border-neutral-200"
        >
          <div className="flex items-start space-x-3">
            <ShieldCheckIcon className="w-5 h-5 text-neutral-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-body-sm text-neutral-600">
                <span className="font-semibold">Your privacy matters:</span> All data is encrypted, 
                you can export or delete your information anytime, and we never share personal 
                details without your explicit consent.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
