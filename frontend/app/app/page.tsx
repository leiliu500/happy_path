'use client'

import React, { useState, useEffect } from 'react'

export default function HomePage() {
  const [currentStep, setCurrentStep] = useState('welcome')
  const [userProgress, setUserProgress] = useState({
    wellnessFocus: '',
    moodLevel: 5,
    challenge: '',
    experienceMinutes: 0,
    hasCompletedAssessment: false
  })
  const [showCrisisSupport, setShowCrisisSupport] = useState(false)

  const stepProgress = {
    welcome: 25,
    assessment: 50,
    experience: 75,
    registration: 90,
    complete: 100
  }

  // Auto-advance after experience
  useEffect(() => {
    if (currentStep === 'experience' && userProgress.experienceMinutes >= 2) {
      setTimeout(() => setCurrentStep('registration'), 1000)
    }
  }, [currentStep, userProgress.experienceMinutes])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-teal-50 to-emerald-50 relative overflow-hidden">
      {/* Crisis Support Button - Always Available */}
      <button
        onClick={() => setShowCrisisSupport(true)}
        className="fixed top-4 right-4 z-50 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full shadow-lg transition-all duration-200 font-medium"
        aria-label="Crisis Support - Get immediate help"
      >
        🆘 Crisis Support
      </button>

      {/* Progress Indicator */}
      <div className="fixed top-0 left-0 w-full h-1 bg-blue-100 z-40">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-teal-500 transition-all duration-500"
          style={{ width: `${stepProgress[currentStep] || 0}%` }}
        />
      </div>

      {/* Main Content */}
      <main className="flex-1 px-4 py-8">
        {/* Step 1: Welcome Screen (30 seconds) */}
        {currentStep === 'welcome' && (
          <div className="max-w-4xl mx-auto text-center animate-fade-in">
            <div className="mb-8">
              <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-4">
                Welcome to Your Wellness Journey 🌱
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Take the first step towards better mental health in just 5 minutes
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">
                Choose your primary wellness focus:
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
                {[
                  { id: 'stress', icon: '🧘', label: 'Stress & Anxiety' },
                  { id: 'depression', icon: '😔', label: 'Depression Support' },
                  { id: 'sleep', icon: '😴', label: 'Sleep & Rest' },
                  { id: 'general', icon: '🏃', label: 'General Wellness' },
                  { id: 'relationships', icon: '👥', label: 'Relationship Health' },
                  { id: 'growth', icon: '🎯', label: 'Personal Growth' }
                ].map(focus => (
                  <button
                    key={focus.id}
                    onClick={() => {
                      setUserProgress(prev => ({ ...prev, wellnessFocus: focus.id }))
                      setCurrentStep('assessment')
                    }}
                    className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                      userProgress.wellnessFocus === focus.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'
                    }`}
                  >
                    <div className="text-3xl mb-2">{focus.icon}</div>
                    <div className="font-medium text-gray-700">{focus.label}</div>
                  </button>
                ))}
              </div>
              <div className="flex gap-4 justify-center">
                <button
                  onClick={() => setCurrentStep('assessment')}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
                >
                  Continue
                </button>
                <button
                  onClick={() => setCurrentStep('assessment')}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-8 py-3 rounded-lg font-medium transition-colors"
                >
                  Skip - I'll explore first
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Quick Assessment (2 minutes) */}
        {currentStep === 'assessment' && (
          <div className="max-w-2xl mx-auto animate-slide-in">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
                Quick Wellness Check-In
              </h2>
              
              <div className="mb-8">
                <label className="block text-lg font-medium text-gray-700 mb-4">
                  How are you feeling right now?
                </label>
                <div className="relative">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={userProgress.moodLevel}
                    onChange={(e) => setUserProgress(prev => ({ ...prev, moodLevel: parseInt(e.target.value) }))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-2">
                    <span>😢 Very Low</span>
                    <span>😊 Excellent</span>
                  </div>
                  <div className="text-center mt-2 text-lg font-semibold text-blue-600">
                    Current Mood: {userProgress.moodLevel}/10
                  </div>
                </div>
              </div>

              <div className="mb-8">
                <label className="block text-lg font-medium text-gray-700 mb-4">
                  What's your biggest wellness challenge today?
                </label>
                <textarea
                  value={userProgress.challenge}
                  onChange={(e) => setUserProgress(prev => ({ ...prev, challenge: e.target.value }))}
                  placeholder="Share what's on your mind... (optional)"
                  className="w-full p-4 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  rows={3}
                />
              </div>

              {userProgress.moodLevel <= 7 && (
                <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-teal-800 mb-2">
                    ✨ Instant Personalized Recommendation
                  </h3>
                  <p className="text-teal-700">
                    Based on your mood level, we recommend starting with a 2-minute breathing exercise 
                    to help you feel more centered and relaxed.
                  </p>
                </div>
              )}

              <div className="flex gap-4 justify-center">
                <button
                  onClick={() => setCurrentStep('welcome')}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={() => {
                    setUserProgress(prev => ({ ...prev, hasCompletedAssessment: true }))
                    setCurrentStep('experience')
                  }}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
                >
                  Let's Try Something Together!
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: First Wellness Experience (2-3 minutes) */}
        {currentStep === 'experience' && (
          <WellnessExperience 
            userProgress={userProgress}
            setUserProgress={setUserProgress}
            onNext={() => setCurrentStep('registration')}
            onBack={() => setCurrentStep('assessment')}
          />
        )}

        {/* Step 4: Value-Driven Registration */}
        {currentStep === 'registration' && (
          <RegistrationPrompt 
            userProgress={userProgress}
            onComplete={() => setCurrentStep('complete')}
            onBack={() => setCurrentStep('experience')}
          />
        )}

        {/* Step 5: Welcome to Community */}
        {currentStep === 'complete' && (
          <WelcomeComplete />
        )}
      </main>

      {/* Crisis Support Modal */}
      {showCrisisSupport && (
        <CrisisSupport onClose={() => setShowCrisisSupport(false)} />
      )}

      {/* Background Effects */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div 
          className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full opacity-20 animate-float"
        />
        <div 
          className="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-200 rounded-full opacity-20 animate-float-delayed"
        />
      </div>
    </div>
  )
}

// Wellness Experience Component
function WellnessExperience({ userProgress, setUserProgress, onNext, onBack }: {
  userProgress: any;
  setUserProgress: (update: any) => void;
  onNext: () => void;
  onBack: () => void;
}) {
  const [selectedActivity, setSelectedActivity] = useState('')
  const [activityStarted, setActivityStarted] = useState(false)
  const [timer, setTimer] = useState(0)
  const [breathingPhase, setBreathingPhase] = useState('inhale')

  useEffect(() => {
    let interval: NodeJS.Timeout
    if (activityStarted) {
      interval = setInterval(() => {
        setTimer(prev => {
          const newTime = prev + 1
          if (newTime % 60 === 0) {
            setUserProgress((current: any) => ({ 
              ...current, 
              experienceMinutes: Math.floor(newTime / 60) 
            }))
          }
          return newTime
        })
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [activityStarted, setUserProgress])

  // Breathing exercise timer
  useEffect(() => {
    if (selectedActivity === 'breathing' && activityStarted) {
      const breathingInterval = setInterval(() => {
        setBreathingPhase(prev => prev === 'inhale' ? 'exhale' : 'inhale')
      }, 4000)
      return () => clearInterval(breathingInterval)
    }
  }, [selectedActivity, activityStarted])

  const activities = [
    {
      id: 'breathing',
      icon: '🧘',
      title: '2-min Breathing Exercise',
      description: 'Guided deep breathing to calm your mind',
      duration: '2 minutes'
    },
    {
      id: 'journaling',
      icon: '📓',
      title: 'AI Journaling Coach',
      description: 'CBT-based prompts and reflection guidance',
      duration: '3-5 minutes'
    },
    {
      id: 'mood-tracking',
      icon: '📊',
      title: 'Daily Mood Tracker',
      description: 'Track your emotional patterns with insights',
      duration: '2 minutes'
    },
    {
      id: 'reflection',
      icon: '📝',
      title: 'Guided Reflection',
      description: 'Mindful prompts to center your thoughts',
      duration: '3 minutes'
    },
    {
      id: 'music',
      icon: '🎵',
      title: 'Calming Music Session',
      description: 'Therapeutic sounds for relaxation',
      duration: '2-5 minutes'
    },
    {
      id: 'insights',
      icon: '�',
      title: 'Your Wellness Insights',
      description: 'See your personalized wellness overview',
      duration: '1 minute'
    }
  ]

  if (activityStarted && selectedActivity === 'breathing') {
    return (
      <div className="max-w-2xl mx-auto text-center animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Breathing Exercise
          </h2>
          <p className="text-gray-600 mb-8">
            Follow the circle and breathe deeply
          </p>
          
          <div className="relative mx-auto mb-8" style={{ width: '200px', height: '200px' }}>
            <div 
              className={`w-full h-full rounded-full bg-gradient-to-br from-blue-400 to-teal-400 transition-transform duration-4000 ${
                breathingPhase === 'inhale' ? 'scale-110' : 'scale-90'
              }`}
              style={{ 
                transition: 'transform 4s ease-in-out',
                transform: breathingPhase === 'inhale' ? 'scale(1.1)' : 'scale(0.9)'
              }}
            />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-white font-semibold text-lg">
                {breathingPhase === 'inhale' ? 'Breathe In' : 'Breathe Out'}
              </div>
            </div>
          </div>

          <div className="text-lg font-semibold text-blue-600 mb-4">
            {Math.floor(timer / 60)}:{(timer % 60).toString().padStart(2, '0')}
          </div>

          {timer >= 120 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-green-800 mb-2">
                🎉 Great job! You've completed the breathing exercise.
              </h3>
              <p className="text-green-700">
                You should feel more relaxed and centered now.
              </p>
            </div>
          )}

          <button
            onClick={() => {
              setActivityStarted(false)
              setSelectedActivity('')
              onNext()
            }}
            className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Continue to Next Step
          </button>
        </div>
      </div>
    )
  }

  // Mood Tracking Activity
  if (activityStarted && selectedActivity === 'mood-tracking') {
    return <MoodTracker onComplete={() => { setActivityStarted(false); setSelectedActivity(''); onNext(); }} timer={timer} />
  }

  // Journaling Activity
  if (activityStarted && selectedActivity === 'journaling') {
    return <JournalingCoach onComplete={() => { setActivityStarted(false); setSelectedActivity(''); onNext(); }} timer={timer} />
  }

  return (
    <div className="max-w-4xl mx-auto animate-slide-in">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">
          Let's try something together right now!
        </h2>
        <p className="text-lg text-gray-600 mb-8 text-center">
          Experience immediate value before any registration
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {activities.map(activity => (
            <button
              key={activity.id}
              onClick={() => setSelectedActivity(activity.id)}
              className={`p-6 rounded-lg border-2 text-left transition-all duration-200 ${
                selectedActivity === activity.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'
              }`}
            >
              <div className="text-4xl mb-3">{activity.icon}</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {activity.title}
              </h3>
              <p className="text-gray-600 mb-2">{activity.description}</p>
              <div className="text-sm text-blue-600 font-medium">
                {activity.duration}
              </div>
            </button>
          ))}
        </div>

        <div className="flex gap-4 justify-center">
          <button
            onClick={onBack}
            className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Back
          </button>
          <button
            onClick={() => {
              if (selectedActivity) {
                setActivityStarted(true)
              }
            }}
            disabled={!selectedActivity}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Start Activity
          </button>
        </div>
      </div>
    </div>
  )
}

// Registration Component
function RegistrationPrompt({ userProgress, onComplete, onBack }: {
  userProgress: any;
  onComplete: () => void;
  onBack: () => void;
}) {
  const [email, setEmail] = useState('')
  const [showGuestMode, setShowGuestMode] = useState(false)

  const improvementScore = Math.round((userProgress.experienceMinutes * 7.5) + 15)

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Amazing! You just improved your wellness score by {improvementScore}% 📈
          </h2>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <h3 className="text-xl font-semibold text-blue-800 mb-4">
            🎯 Save your progress to:
          </h3>
          <div className="space-y-3">
            <div className="flex items-center">
              <span className="text-green-500 mr-3">✅</span>
              <span className="text-blue-700">Track your wellness journey over time</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-500 mr-3">✅</span>
              <span className="text-blue-700">Get personalized recommendations</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-500 mr-3">✅</span>
              <span className="text-blue-700">Connect with supportive community</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-500 mr-3">✅</span>
              <span className="text-blue-700">Access advanced wellness tools</span>
            </div>
          </div>
        </div>

        <div className="space-y-4 mb-8">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📧 Email (optional - can use guest mode)
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            />
          </div>
          <p className="text-sm text-gray-600">
            🔒 We respect your privacy - you control your data
          </p>
        </div>

        <div className="flex flex-col gap-4">
          <button
            onClick={onComplete}
            className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Save My Progress
          </button>
          <button
            onClick={() => setShowGuestMode(true)}
            className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-8 py-3 rounded-lg font-medium transition-colors"
          >
            Continue Exploring First
          </button>
          <button
            onClick={onBack}
            className="text-gray-500 hover:text-gray-700 font-medium"
          >
            Back to Experience
          </button>
        </div>

        {showGuestMode && (
          <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-semibold text-yellow-800 mb-2">Guest Mode Activated</h4>
            <p className="text-yellow-700 text-sm">
              You have 3 days of full access. Your progress will be saved temporarily.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

// Welcome Complete Component
function WelcomeComplete() {
  return (
    <div className="max-w-2xl mx-auto text-center animate-bounce-in">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="text-8xl mb-6">🎉</div>
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Welcome to Your Wellness Journey!
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          You've taken the first step towards better mental health. 
          Continue exploring our platform for personalized support.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-3xl mb-2">📊</div>
            <h3 className="font-semibold text-gray-800">Track Progress</h3>
            <p className="text-sm text-gray-600">Monitor your wellness journey</p>
          </div>
          <div className="bg-teal-50 p-4 rounded-lg">
            <div className="text-3xl mb-2">👥</div>
            <h3 className="font-semibold text-gray-800">Join Community</h3>
            <p className="text-sm text-gray-600">Connect with others</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-3xl mb-2">🎯</div>
            <h3 className="font-semibold text-gray-800">Achieve Goals</h3>
            <p className="text-sm text-gray-600">Reach your wellness targets</p>
          </div>
        </div>

        <button
          onClick={() => window.location.href = '/dashboard'}
          className="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-8 py-3 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all duration-200"
        >
          Explore Your Dashboard
        </button>
      </div>
    </div>
  )
}

// Mood Tracker Component
function MoodTracker({ onComplete, timer }: { onComplete: () => void, timer: number }) {
  const [moodData, setMoodData] = useState({
    currentMood: 5,
    emotions: [] as string[],
    triggers: '',
    gratitude: '',
    notes: '',
    energyLevel: 5,
    stressLevel: 5,
    sleepQuality: 5,
    physicalSymptoms: [] as string[]
  })
  const [step, setStep] = useState(1)
  const [showMoodHistory, setShowMoodHistory] = useState(false)

  const moodEmojis = [
    { value: 1, emoji: '😢', label: 'Very Low', color: 'bg-red-100 border-red-300' },
    { value: 2, emoji: '😔', label: 'Low', color: 'bg-red-50 border-red-200' },
    { value: 3, emoji: '😐', label: 'Neutral', color: 'bg-yellow-50 border-yellow-200' },
    { value: 4, emoji: '🙂', label: 'Good', color: 'bg-yellow-100 border-yellow-300' },
    { value: 5, emoji: '😊', label: 'Great', color: 'bg-green-50 border-green-200' },
    { value: 6, emoji: '😄', label: 'Excellent', color: 'bg-green-100 border-green-300' },
    { value: 7, emoji: '🤗', label: 'Amazing', color: 'bg-green-200 border-green-400' },
    { value: 8, emoji: '🥰', label: 'Wonderful', color: 'bg-blue-100 border-blue-300' },
    { value: 9, emoji: '😍', label: 'Fantastic', color: 'bg-blue-200 border-blue-400' },
    { value: 10, emoji: '🌟', label: 'Perfect', color: 'bg-purple-100 border-purple-300' }
  ]

  const emotionOptions = [
    { id: 'happy', emoji: '😊', label: 'Happy', category: 'positive' },
    { id: 'sad', emoji: '😔', label: 'Sad', category: 'negative' },
    { id: 'anxious', emoji: '😰', label: 'Anxious', category: 'negative' },
    { id: 'calm', emoji: '😌', label: 'Calm', category: 'positive' },
    { id: 'excited', emoji: '🤗', label: 'Excited', category: 'positive' },
    { id: 'frustrated', emoji: '😤', label: 'Frustrated', category: 'negative' },
    { id: 'content', emoji: '😊', label: 'Content', category: 'positive' },
    { id: 'overwhelmed', emoji: '😵', label: 'Overwhelmed', category: 'negative' },
    { id: 'grateful', emoji: '🙏', label: 'Grateful', category: 'positive' },
    { id: 'angry', emoji: '😠', label: 'Angry', category: 'negative' },
    { id: 'peaceful', emoji: '☮️', label: 'Peaceful', category: 'positive' },
    { id: 'worried', emoji: '😟', label: 'Worried', category: 'negative' }
  ]

  const physicalSymptoms = [
    { id: 'headache', emoji: '🤕', label: 'Headache' },
    { id: 'fatigue', emoji: '😴', label: 'Fatigue' },
    { id: 'tension', emoji: '😣', label: 'Muscle Tension' },
    { id: 'nausea', emoji: '🤢', label: 'Nausea' },
    { id: 'restless', emoji: '😤', label: 'Restlessness' },
    { id: 'appetite', emoji: '🍽️', label: 'Appetite Changes' }
  ]

  const handleEmotionToggle = (emotionId: string) => {
    setMoodData(prev => ({
      ...prev,
      emotions: prev.emotions.includes(emotionId)
        ? prev.emotions.filter(e => e !== emotionId)
        : [...prev.emotions, emotionId]
    }))
  }

  const handleSymptomToggle = (symptomId: string) => {
    setMoodData(prev => ({
      ...prev,
      physicalSymptoms: prev.physicalSymptoms.includes(symptomId)
        ? prev.physicalSymptoms.filter(s => s !== symptomId)
        : [...prev.physicalSymptoms, symptomId]
    }))
  }

  const getMoodInsight = () => {
    const mood = moodData.currentMood
    if (mood <= 3) return {
      message: "It looks like you're having a tough time. Remember, difficult feelings are temporary.",
      suggestion: "Consider trying a breathing exercise or reaching out to someone you trust.",
      color: "text-red-600"
    }
    if (mood <= 6) return {
      message: "You're doing okay today. Small steps toward wellness can make a big difference.",
      suggestion: "Maybe try some gentle movement or practice gratitude.",
      color: "text-yellow-600"
    }
    return {
      message: "You're feeling great today! This is wonderful to see.",
      suggestion: "Consider sharing your positive energy with others or reflecting on what's going well.",
      color: "text-green-600"
    }
  }

  if (step === 1) {
    const insight = getMoodInsight()
    return (
      <div className="max-w-3xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Daily Mood Check-In 📊
            </h2>
            <p className="text-gray-600 mb-4">
              Track your emotional patterns with personalized insights
            </p>
            <div className="text-sm text-blue-600 bg-blue-50 rounded-lg p-3">
              💡 Tip: Regular mood tracking helps identify patterns and triggers in your mental health journey
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-6 text-center">
              How are you feeling right now?
            </h3>
            <div className="grid grid-cols-5 gap-3 mb-6">
              {moodEmojis.map(mood => (
                <button
                  key={mood.value}
                  onClick={() => setMoodData(prev => ({ ...prev, currentMood: mood.value }))}
                  className={`p-4 rounded-xl border-2 text-center transition-all transform hover:scale-105 ${
                    moodData.currentMood === mood.value
                      ? `border-blue-500 bg-blue-50 shadow-lg scale-105 ${mood.color}`
                      : `border-gray-200 hover:border-blue-300 hover:bg-blue-50 ${mood.color}`
                  }`}
                >
                  <div className="text-4xl mb-2">{mood.emoji}</div>
                  <div className="text-xs font-medium text-gray-700">{mood.label}</div>
                  <div className="text-xs text-gray-500">{mood.value}</div>
                </button>
              ))}
            </div>
            
            {/* Dynamic Mood Insight */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4 mb-4">
              <h4 className={`font-semibold mb-2 ${insight.color}`}>
                🧠 Mood Insight
              </h4>
              <p className="text-gray-700 mb-2">{insight.message}</p>
              <p className="text-sm text-gray-600">{insight.suggestion}</p>
            </div>

            {/* Additional Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Energy Level
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={moodData.energyLevel}
                  onChange={(e) => setMoodData(prev => ({ ...prev, energyLevel: parseInt(e.target.value) }))}
                  className="w-full h-2 bg-yellow-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-center text-sm text-gray-600 mt-1">
                  ⚡ {moodData.energyLevel}/10
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stress Level
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={moodData.stressLevel}
                  onChange={(e) => setMoodData(prev => ({ ...prev, stressLevel: parseInt(e.target.value) }))}
                  className="w-full h-2 bg-red-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-center text-sm text-gray-600 mt-1">
                  😤 {moodData.stressLevel}/10
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sleep Quality
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={moodData.sleepQuality}
                  onChange={(e) => setMoodData(prev => ({ ...prev, sleepQuality: parseInt(e.target.value) }))}
                  className="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-center text-sm text-gray-600 mt-1">
                  😴 {moodData.sleepQuality}/10
                </div>
              </div>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={() => setShowMoodHistory(true)}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              📈 View History
            </button>
            <button
              onClick={() => setStep(2)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Continue to Emotions
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (step === 2) {
    const positiveEmotions = emotionOptions.filter(e => e.category === 'positive')
    const negativeEmotions = emotionOptions.filter(e => e.category === 'negative')
    
    return (
      <div className="max-w-3xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            What emotions are you experiencing?
          </h3>
          <p className="text-gray-600 mb-8 text-center">
            Select all that apply. It's normal to feel multiple emotions at once.
          </p>

          {/* Positive Emotions */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-green-700 mb-4 flex items-center">
              ✨ Positive Emotions
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {positiveEmotions.map(emotion => (
                <button
                  key={emotion.id}
                  onClick={() => handleEmotionToggle(emotion.id)}
                  className={`p-4 rounded-lg border-2 text-center transition-all transform hover:scale-105 ${
                    moodData.emotions.includes(emotion.id)
                      ? 'border-green-500 bg-green-50 shadow-lg scale-105'
                      : 'border-gray-200 hover:border-green-300 hover:bg-green-50'
                  }`}
                >
                  <div className="text-2xl mb-2">{emotion.emoji}</div>
                  <div className="text-sm font-medium">{emotion.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Negative Emotions */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-orange-700 mb-4 flex items-center">
              🌧️ Challenging Emotions
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {negativeEmotions.map(emotion => (
                <button
                  key={emotion.id}
                  onClick={() => handleEmotionToggle(emotion.id)}
                  className={`p-4 rounded-lg border-2 text-center transition-all transform hover:scale-105 ${
                    moodData.emotions.includes(emotion.id)
                      ? 'border-orange-500 bg-orange-50 shadow-lg scale-105'
                      : 'border-gray-200 hover:border-orange-300 hover:bg-orange-50'
                  }`}
                >
                  <div className="text-2xl mb-2">{emotion.emoji}</div>
                  <div className="text-sm font-medium">{emotion.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Physical Symptoms */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-purple-700 mb-4 flex items-center">
              🩺 Physical Symptoms (optional)
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {physicalSymptoms.map(symptom => (
                <button
                  key={symptom.id}
                  onClick={() => handleSymptomToggle(symptom.id)}
                  className={`p-3 rounded-lg border-2 text-center transition-all ${
                    moodData.physicalSymptoms.includes(symptom.id)
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300 hover:bg-purple-50'
                  }`}
                >
                  <div className="text-lg mb-1">{symptom.emoji}</div>
                  <div className="text-xs font-medium">{symptom.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Selection Summary */}
          {moodData.emotions.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h4 className="font-semibold text-blue-800 mb-2">Selected Emotions:</h4>
              <div className="flex flex-wrap gap-2">
                {moodData.emotions.map(emotionId => {
                  const emotion = emotionOptions.find(e => e.id === emotionId)
                  return (
                    <span key={emotionId} className="bg-white px-3 py-1 rounded-full text-sm border">
                      {emotion?.emoji} {emotion?.label}
                    </span>
                  )
                })}
              </div>
            </div>
          )}

          <div className="flex gap-4 justify-center">
            <button
              onClick={() => setStep(1)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              ← Back to Mood
            </button>
            <button
              onClick={() => setStep(3)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Continue to Reflection
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (step === 3) {
    const currentMoodEmoji = moodEmojis.find(m => m.value === moodData.currentMood)
    const selectedEmotions = moodData.emotions.map(id => emotionOptions.find(e => e.id === id)).filter(Boolean)
    const selectedSymptoms = moodData.physicalSymptoms.map(id => physicalSymptoms.find(s => s.id === id)).filter(Boolean)
    
    const getWellnessScore = () => {
      const moodScore = moodData.currentMood * 10
      const energyScore = moodData.energyLevel * 5
      const stressScore = (11 - moodData.stressLevel) * 5 // Inverted because lower stress is better
      const sleepScore = moodData.sleepQuality * 5
      return Math.round((moodScore + energyScore + stressScore + sleepScore) / 4)
    }

    const wellnessScore = getWellnessScore()
    
    return (
      <div className="max-w-3xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            Reflection & Insights
          </h3>

          {/* Wellness Score Card */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl p-6 mb-8 text-center">
            <h4 className="text-xl font-bold mb-2">Today's Wellness Score</h4>
            <div className="text-4xl font-bold mb-2">{wellnessScore}/100</div>
            <div className="text-sm opacity-90">
              Based on mood, energy, stress, and sleep quality
            </div>
          </div>

          {/* Current Status Summary */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-3">📊 Current Status</h4>
              <div className="space-y-2 text-blue-700">
                <p>Mood: {currentMoodEmoji?.emoji} {currentMoodEmoji?.label} ({moodData.currentMood}/10)</p>
                <p>Energy: ⚡ {moodData.energyLevel}/10</p>
                <p>Stress: 😤 {moodData.stressLevel}/10</p>
                <p>Sleep: 😴 {moodData.sleepQuality}/10</p>
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-800 mb-3">😊 Emotions Today</h4>
              <div className="text-green-700">
                {selectedEmotions.length > 0 ? (
                  <div className="flex flex-wrap gap-1">
                    {selectedEmotions.map(emotion => (
                      <span key={emotion?.id} className="bg-white px-2 py-1 rounded text-xs">
                        {emotion?.emoji} {emotion?.label}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm">No emotions selected</p>
                )}
              </div>
            </div>
          </div>

          {/* Reflection Questions */}
          <div className="space-y-6 mb-8">
            <div>
              <label className="block text-lg font-medium text-gray-700 mb-3">
                💭 What triggered these feelings today? (optional)
              </label>
              <textarea
                value={moodData.triggers}
                onChange={(e) => setMoodData(prev => ({ ...prev, triggers: e.target.value }))}
                placeholder="Work stress, relationships, health, weather, news, social media, etc..."
                className="w-full p-4 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                rows={3}
              />
            </div>

            <div>
              <label className="block text-lg font-medium text-gray-700 mb-3">
                🙏 What are you grateful for today?
              </label>
              <input
                type="text"
                value={moodData.gratitude}
                onChange={(e) => setMoodData(prev => ({ ...prev, gratitude: e.target.value }))}
                placeholder="Something positive from your day, no matter how small..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-lg font-medium text-gray-700 mb-3">
                📝 Additional notes (optional)
              </label>
              <textarea
                value={moodData.notes}
                onChange={(e) => setMoodData(prev => ({ ...prev, notes: e.target.value }))}
                placeholder="Any other thoughts, goals, or observations about your day..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                rows={2}
              />
            </div>
          </div>

          {/* Physical Symptoms Summary */}
          {selectedSymptoms.length > 0 && (
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
              <h4 className="font-semibold text-purple-800 mb-2">🩺 Physical Symptoms Noted:</h4>
              <div className="flex flex-wrap gap-2">
                {selectedSymptoms.map(symptom => (
                  <span key={symptom?.id} className="bg-white px-3 py-1 rounded-full text-sm border">
                    {symptom?.emoji} {symptom?.label}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* AI Insights */}
          <div className="bg-gradient-to-r from-teal-50 to-blue-50 border border-teal-200 rounded-lg p-6 mb-8">
            <h4 className="font-semibold text-teal-800 mb-3">🤖 AI Insights & Recommendations</h4>
            <div className="space-y-3 text-teal-700">
              {wellnessScore >= 75 ? (
                <>
                  <p>✅ You're having a great day! Your wellness indicators are strong.</p>
                  <p>💡 Consider: Sharing your positive energy with others or documenting what's working well.</p>
                </>
              ) : wellnessScore >= 50 ? (
                <>
                  <p>⚡ You're doing okay today with room for improvement.</p>
                  <p>💡 Consider: Gentle movement, connecting with nature, or practicing mindfulness.</p>
                </>
              ) : (
                <>
                  <p>🤗 It looks like you're having a challenging day. That's completely normal.</p>
                  <p>💡 Consider: Deep breathing, reaching out to support, or engaging in self-care activities.</p>
                </>
              )}
              
              {moodData.stressLevel >= 7 && (
                <p>🧘 Your stress level is high. Try the breathing exercise or take a short walk.</p>
              )}
              
              {moodData.sleepQuality <= 4 && (
                <p>😴 Poor sleep affects mood and energy. Consider establishing a calming bedtime routine.</p>
              )}
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={() => setStep(2)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              ← Back to Emotions
            </button>
            <button
              onClick={() => setStep(4)}
              className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Review & Save
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Step 4: Final Review and Save
  if (step === 4) {
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h3 className="text-2xl font-bold text-gray-800 mb-4">
            Mood Entry Complete!
          </h3>
          <p className="text-gray-600 mb-8">
            Thank you for taking time to check in with yourself. Your mental health matters.
          </p>

          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
            <h4 className="font-semibold text-green-800 mb-3">✅ What you accomplished:</h4>
            <div className="space-y-2 text-green-700 text-left">
              <p>• Tracked your mood and wellness indicators</p>
              <p>• Identified your emotions and physical state</p>
              <p>• Reflected on triggers and gratitude</p>
              <p>• Received personalized insights</p>
              <p>• Contributed to your wellness journey data</p>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
            <h4 className="font-semibold text-blue-800 mb-2">🔄 Next Steps:</h4>
            <div className="text-blue-700 text-sm space-y-1">
              <p>• Check in again tomorrow to track patterns</p>
              <p>• Try the breathing exercise if feeling stressed</p>
              <p>• Explore the journaling feature for deeper reflection</p>
              <p>• Connect with your support network if needed</p>
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <button
              onClick={onComplete}
              className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Save & Continue Journey
            </button>
            <button
              onClick={() => setStep(1)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Start New Entry
            </button>
          </div>
        </div>
      </div>
    )
  }
}

// AI Journaling Coach Component
function JournalingCoach({ onComplete, timer }: { onComplete: () => void, timer: number }) {
  const [journalData, setJournalData] = useState({
    prompt: '',
    response: '',
    insights: []
  })
  const [currentPrompt, setCurrentPrompt] = useState<{
    category: string;
    prompt: string;
    insight: string;
  } | null>(null)
  const [step, setStep] = useState(1)

  const cbtPrompts = [
    {
      category: 'Thought Recognition',
      prompt: "What thoughts have been running through your mind today? Write them down without judgment.",
      insight: "Recognizing your thoughts is the first step to understanding your mental patterns."
    },
    {
      category: 'Emotion Awareness',
      prompt: "Describe how you're feeling right now. What emotions are present in your body?",
      insight: "Connecting with your emotions helps you understand your inner experience."
    },
    {
      category: 'Gratitude Practice',
      prompt: "Write about three things you're grateful for today, no matter how small.",
      insight: "Gratitude practice has been shown to improve mental health and resilience."
    },
    {
      category: 'Challenge Reframing',
      prompt: "Think of a challenge you're facing. How might you view this situation differently?",
      insight: "Reframing helps you find new perspectives and solutions to problems."
    },
    {
      category: 'Self-Compassion',
      prompt: "Write a kind letter to yourself as if you were comforting a good friend.",
      insight: "Self-compassion is crucial for mental health and personal growth."
    }
  ]

  useEffect(() => {
    if (step === 1) {
      const randomPrompt = cbtPrompts[Math.floor(Math.random() * cbtPrompts.length)]
      setCurrentPrompt(randomPrompt)
      setJournalData(prev => ({ ...prev, prompt: randomPrompt.prompt }))
    }
  }, [step])

  if (step === 1) {
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">
            AI Journaling Coach 📓
          </h2>
          <p className="text-gray-600 mb-8 text-center">
            CBT-based prompts and reflection guidance
          </p>

          <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold text-purple-800 mb-3">
              Today's Reflection Prompt:
            </h3>
            <p className="text-purple-700 text-lg leading-relaxed">
              {currentPrompt?.prompt || 'Loading prompt...'}
            </p>
          </div>

          <div className="mb-6">
            <label className="block text-lg font-medium text-gray-700 mb-3">
              Your Response:
            </label>
            <textarea
              value={journalData.response}
              onChange={(e) => setJournalData(prev => ({ ...prev, response: e.target.value }))}
              placeholder="Take your time... there's no right or wrong answer. Just write what comes to mind."
              className="w-full p-4 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
              rows={6}
            />
            <div className="text-sm text-gray-500 mt-2">
              {journalData.response.length} characters
            </div>
          </div>

          <div className="text-center">
            <button
              onClick={() => setStep(2)}
              disabled={journalData.response.length < 50}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Get AI Insights
            </button>
            {journalData.response.length < 50 && (
              <p className="text-sm text-gray-500 mt-2">
                Write at least 50 characters to continue
              </p>
            )}
          </div>
        </div>
      </div>
    )
  }

  if (step === 2) {
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            AI-Generated Insights ✨
          </h3>

          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
            <h4 className="font-semibold text-green-800 mb-3">Therapeutic Insight:</h4>
            <p className="text-green-700 leading-relaxed">
              {currentPrompt?.insight || 'Generating insights...'}
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h4 className="font-semibold text-blue-800 mb-3">Reflection Analysis:</h4>
            <div className="space-y-3 text-blue-700">
              <p>✅ You've engaged in meaningful self-reflection</p>
              <p>✅ Your response shows emotional awareness</p>
              <p>✅ You're building healthy coping strategies</p>
              {journalData.response.length > 200 && (
                <p>✅ Detailed reflection shows commitment to growth</p>
              )}
            </div>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
            <h4 className="font-semibold text-yellow-800 mb-3">Suggested Next Steps:</h4>
            <ul className="list-disc list-inside text-yellow-700 space-y-1">
              <li>Continue journaling regularly for best results</li>
              <li>Consider sharing insights with a trusted friend</li>
              <li>Practice the breathing exercise when stressed</li>
              <li>Return to this reflection in a few days</li>
            </ul>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={() => setStep(1)}
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Write More
            </button>
            <button
              onClick={onComplete}
              className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Complete Session
            </button>
          </div>
        </div>
      </div>
    )
  }
}

// Crisis Support Component
function CrisisSupport({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 animate-scale-in">
        <div className="text-center mb-6">
          <div className="text-4xl mb-2">🆘</div>
          <h2 className="text-2xl font-bold text-red-600">Crisis Support</h2>
        </div>

        <div className="space-y-4 mb-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="font-semibold text-red-800 mb-2">Immediate Help:</h3>
            <div className="space-y-2 text-red-700">
              <div>🆘 988 Suicide & Crisis Lifeline</div>
              <div>📱 Crisis Text: Text HOME to 741741</div>
              <div>🏥 Emergency Services: 911</div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-800 mb-2">24/7 Support:</h3>
            <div className="space-y-2 text-blue-700">
              <div>💬 Crisis Chat Support</div>
              <div>🌐 Online Resources</div>
              <div>📞 Professional Helplines</div>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => window.open('tel:988', '_blank')}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg font-medium"
          >
            Call 988
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 py-3 rounded-lg font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
