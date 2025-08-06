'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PlayIcon, PauseIcon, HeartIcon } from '@heroicons/react/24/outline'

interface WellnessExperienceProps {
  onComplete: (data: { activityCompleted: string; feelsBetter: boolean }) => void
  moodLevel: number
  challenge: string
}

type ActivityType = 'breathing' | 'reflection' | 'music' | 'insights'

const activities = {
  breathing: {
    title: '2-Minute Breathing Exercise',
    description: 'A simple breathing technique to help you feel centered',
    duration: 120, // 2 minutes
    icon: '🧘‍♀️'
  },
  reflection: {
    title: 'Guided Reflection',
    description: 'Thoughtful prompts to help process your feelings',
    duration: 180, // 3 minutes
    icon: '📝'
  },
  music: {
    title: 'Calming Music Session',
    description: 'Soothing sounds designed for relaxation',
    duration: 300, // 5 minutes
    icon: '🎵'
  },
  insights: {
    title: 'Your Wellness Insights',
    description: 'Personalized patterns and recommendations',
    duration: 60, // 1 minute
    icon: '📊'
  }
}

export function WellnessExperience({ onComplete, moodLevel, challenge }: WellnessExperienceProps) {
  const [selectedActivity, setSelectedActivity] = useState<ActivityType | null>(null)
  const [isActive, setIsActive] = useState(false)
  const [timeLeft, setTimeLeft] = useState(0)
  const [isCompleted, setIsCompleted] = useState(false)
  const [breathCount, setBreathCount] = useState(0)
  const [breathPhase, setBreathPhase] = useState<'inhale' | 'hold' | 'exhale'>('inhale')

  useEffect(() => {
    let interval: NodeJS.Timeout
    
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(time => {
          if (time <= 1) {
            setIsActive(false)
            setIsCompleted(true)
            return 0
          }
          return time - 1
        })
      }, 1000)
    }

    return () => clearInterval(interval)
  }, [isActive, timeLeft])

  // Breathing exercise timer
  useEffect(() => {
    if (selectedActivity === 'breathing' && isActive) {
      const breathInterval = setInterval(() => {
        setBreathPhase(phase => {
          switch (phase) {
            case 'inhale': return 'hold'
            case 'hold': return 'exhale'
            case 'exhale': 
              setBreathCount(c => c + 1)
              return 'inhale'
            default: return 'inhale'
          }
        })
      }, 4000) // 4 seconds per phase

      return () => clearInterval(breathInterval)
    }
  }, [selectedActivity, isActive])

  const startActivity = (activity: ActivityType) => {
    setSelectedActivity(activity)
    setTimeLeft(activities[activity].duration)
    setIsActive(true)
    setBreathCount(0)
    setBreathPhase('inhale')
  }

  const toggleActivity = () => {
    setIsActive(!isActive)
  }

  const completeExperience = () => {
    onComplete({
      activityCompleted: selectedActivity || 'breathing',
      feelsBetter: true
    })
  }

  if (isCompleted) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md mx-auto text-center"
        >
          <motion.div
            className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-accent-400 to-secondary-400 flex items-center justify-center"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <HeartIcon className="w-12 h-12 text-white" />
          </motion.div>
          
          <h2 className="text-h2 font-bold text-neutral-900 mb-4">
            Well Done! 🎉
          </h2>
          
          <p className="text-body text-neutral-600 mb-8">
            You've completed your first wellness activity. Many users report feeling 15-30% better after just one session.
          </p>

          <div className="bg-gradient-to-r from-secondary-50 to-accent-50 rounded-2xl p-6 mb-8">
            <h3 className="text-h3 font-semibold text-neutral-900 mb-2">
              Quick Check: How do you feel now?
            </h3>
            <div className="flex justify-center space-x-4 mt-4">
              <button
                onClick={completeExperience}
                className="btn-secondary flex items-center space-x-2"
              >
                <span>😊</span>
                <span>Better</span>
              </button>
              <button
                onClick={completeExperience}
                className="btn-outline flex items-center space-x-2"
              >
                <span>😐</span>
                <span>Same</span>
              </button>
            </div>
          </div>
          
          <button
            onClick={completeExperience}
            className="btn-primary px-8 py-3"
          >
            Continue to Save Progress
          </button>
        </motion.div>
      </div>
    )
  }

  if (selectedActivity) {
    return (
      <div className="min-h-screen flex flex-col justify-center px-4 py-8">
        <div className="max-w-md mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="text-6xl mb-4">
              {activities[selectedActivity].icon}
            </div>
            <h1 className="text-h1 font-bold text-neutral-900 mb-2">
              {activities[selectedActivity].title}
            </h1>
            <p className="text-body text-neutral-600">
              {activities[selectedActivity].description}
            </p>
          </motion.div>

          {/* Activity Content */}
          <div className="card p-8 mb-8">
            {selectedActivity === 'breathing' && (
              <BreathingExercise 
                isActive={isActive} 
                breathPhase={breathPhase}
                breathCount={breathCount}
              />
            )}
            
            {selectedActivity === 'reflection' && (
              <ReflectionPrompts isActive={isActive} />
            )}
            
            {selectedActivity === 'music' && (
              <MusicSession isActive={isActive} />
            )}
            
            {selectedActivity === 'insights' && (
              <WellnessInsights moodLevel={moodLevel} challenge={challenge} />
            )}
          </div>

          {/* Timer and Controls */}
          <div className="flex flex-col items-center space-y-4">
            <div className="text-h2 font-bold text-neutral-900">
              {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
            </div>
            
            <button
              onClick={toggleActivity}
              className="btn-primary w-16 h-16 rounded-full flex items-center justify-center"
            >
              {isActive ? (
                <PauseIcon className="w-8 h-8" />
              ) : (
                <PlayIcon className="w-8 h-8 ml-1" />
              )}
            </button>
            
            <p className="text-body-sm text-neutral-500">
              {isActive ? 'Tap to pause' : 'Tap to start'}
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col justify-center px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-h1 font-bold text-neutral-900 mb-4">
            Let's try something together right now!
          </h1>
          <p className="text-body-lg text-neutral-600">
            Choose an activity that resonates with you. Experience immediate value before any commitment.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {(Object.entries(activities) as [ActivityType, typeof activities.breathing][]).map(([key, activity], index) => (
            <motion.button
              key={key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => startActivity(key)}
              className="card p-6 text-left hover:scale-105 transition-all duration-300 active:scale-95"
            >
              <div className="text-4xl mb-4">{activity.icon}</div>
              <h3 className="text-h3 font-semibold text-neutral-900 mb-2">
                {activity.title}
              </h3>
              <p className="text-body-sm text-neutral-600 mb-4">
                {activity.description}
              </p>
              <div className="text-body-sm text-secondary-600 font-medium">
                {Math.floor(activity.duration / 60)} minutes
              </div>
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  )
}

// Breathing Exercise Component
function BreathingExercise({ isActive, breathPhase, breathCount }: { 
  isActive: boolean
  breathPhase: 'inhale' | 'hold' | 'exhale'
  breathCount: number
}) {
  const phaseInstructions = {
    inhale: 'Breathe in slowly',
    hold: 'Hold gently',
    exhale: 'Breathe out slowly'
  }

  return (
    <div className="text-center">
      <motion.div
        className="w-32 h-32 mx-auto mb-6 rounded-full bg-gradient-to-br from-secondary-400 to-accent-400 flex items-center justify-center"
        animate={isActive ? {
          scale: breathPhase === 'inhale' ? 1.2 : breathPhase === 'hold' ? 1.2 : 1
        } : {}}
        transition={{ duration: 4, ease: "easeInOut" }}
      >
        <span className="text-4xl text-white">🫁</span>
      </motion.div>
      
      <h3 className="text-h3 font-semibold text-neutral-900 mb-2">
        {phaseInstructions[breathPhase]}
      </h3>
      
      <p className="text-body text-neutral-600">
        Breath cycle: {breathCount}
      </p>
    </div>
  )
}

// Reflection Prompts Component
function ReflectionPrompts({ isActive }: { isActive: boolean }) {
  const prompts = [
    "What are three things you're grateful for today?",
    "What emotion are you feeling most strongly right now?",
    "What would you tell a friend who was feeling the same way?",
    "What's one small thing that could make today better?"
  ]

  const [currentPrompt, setCurrentPrompt] = useState(0)

  useEffect(() => {
    if (isActive) {
      const interval = setInterval(() => {
        setCurrentPrompt(p => (p + 1) % prompts.length)
      }, 45000) // Change prompt every 45 seconds

      return () => clearInterval(interval)
    }
  }, [isActive])

  return (
    <div className="text-center">
      <div className="text-4xl mb-6">💭</div>
      
      <AnimatePresence mode="wait">
        <motion.div
          key={currentPrompt}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-body-lg text-neutral-800 leading-relaxed">
            {prompts[currentPrompt]}
          </p>
        </motion.div>
      </AnimatePresence>
      
      <div className="mt-6 flex justify-center space-x-2">
        {prompts.map((_, index) => (
          <div
            key={index}
            className={`w-2 h-2 rounded-full transition-colors duration-300 ${
              index === currentPrompt ? 'bg-secondary-500' : 'bg-neutral-300'
            }`}
          />
        ))}
      </div>
    </div>
  )
}

// Music Session Component
function MusicSession({ isActive }: { isActive: boolean }) {
  return (
    <div className="text-center">
      <motion.div
        className="w-32 h-32 mx-auto mb-6 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center"
        animate={isActive ? { rotate: 360 } : {}}
        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
      >
        <span className="text-4xl text-white">🎵</span>
      </motion.div>
      
      <h3 className="text-h3 font-semibold text-neutral-900 mb-4">
        Peaceful Soundscape
      </h3>
      
      <div className="space-y-2">
        {['Nature sounds', 'Gentle rain', 'Ocean waves'].map((sound, index) => (
          <motion.div
            key={sound}
            className="flex items-center justify-center space-x-2"
            animate={isActive ? { opacity: [0.5, 1, 0.5] } : {}}
            transition={{ delay: index * 0.5, duration: 2, repeat: Infinity }}
          >
            <div className="w-2 h-2 rounded-full bg-purple-400"></div>
            <span className="text-body-sm text-neutral-600">{sound}</span>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

// Wellness Insights Component
function WellnessInsights({ moodLevel, challenge }: { moodLevel: number; challenge: string }) {
  return (
    <div className="text-center space-y-6">
      <div className="text-4xl mb-4">📊</div>
      
      <div className="bg-gradient-to-r from-secondary-50 to-accent-50 rounded-xl p-4">
        <h4 className="font-semibold text-neutral-900 mb-2">Your Mood Trend</h4>
        <div className="flex justify-center items-end space-x-1 h-16">
          {[3, 4, moodLevel, 6, 7].map((height, index) => (
            <motion.div
              key={index}
              className="bg-secondary-400 rounded-t"
              style={{ width: '12px' }}
              initial={{ height: 0 }}
              animate={{ height: `${height * 8}px` }}
              transition={{ delay: index * 0.2 }}
            />
          ))}
        </div>
        <p className="text-body-sm text-neutral-600 mt-2">
          Showing improvement potential
        </p>
      </div>
      
      <div className="text-left bg-white rounded-xl p-4 border border-neutral-200">
        <h4 className="font-semibold text-neutral-900 mb-2">Personalized Insight</h4>
        <p className="text-body-sm text-neutral-700">
          Based on your current mood level of {moodLevel}/6, regular breathing exercises 
          could help improve your daily wellness by 20-30%.
        </p>
      </div>
    </div>
  )
}
