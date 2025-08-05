/**
 * Professional Mood Tracking Flow Data
 * Production-ready data structures for healing-focused mood tracking
 */

// User Profile Data
export const userProfile = {
  userId: "user_12345",
  name: "Alex Chen",
  email: "alex.chen@example.com",
  joinDate: "2025-07-15",
  timezone: "America/Los_Angeles",
  healingPreferences: {
    enableCrisisSupport: true,
    privacyLevel: "private",
    healingGoals: ["anxiety_management", "sleep_improvement", "emotional_balance"],
    preferredInterventions: ["breathing_exercises", "mindfulness", "journaling"],
    notificationSettings: {
      dailyCheckins: true,
      healingReminders: true,
      achievementAlerts: false
    }
  },
  clinicalInfo: {
    riskLevel: "low",
    hasTherapist: false,
    emergencyContacts: [],
    medications: []
  }
};

// Current Mood Entry (Production Format)
export const moodEntry = {
  entryId: "mood_67890",
  userId: "user_12345",
  timestamp: "2025-08-05T14:30:00Z",
  mood: {
    overall: 7,
    anxiety: 3, // 1-5 scale
    depression: 2,
    stress: 3,
    energy: 4,
    motivation: 4
  },
  physicalWellness: {
    sleepHours: 7.5,
    sleepQuality: 4, // 1-5 scale
    exerciseMinutes: 30,
    appetite: 4,
    physicalSymptoms: []
  },
  emotionalState: {
    primaryEmotions: ["hopeful", "focused", "mildly_anxious"],
    emotionalIntensity: 3, // 1-5 scale
    triggers: ["work_presentation"],
    copingStrategies: ["deep_breathing", "morning_walk"],
    socialConnections: 3 // 1-5 scale
  },
  contextualFactors: {
    location: "work",
    weather: "sunny",
    timeOfDay: "afternoon",
    socialSituation: "alone"
  },
  notes: {
    gratitude: "Grateful for supportive team and beautiful weather",
    reflection: "Feeling more confident about the presentation after practicing. Morning walk really helped.",
    goals: "Complete presentation prep, practice self-compassion"
  },
  assessments: {
    riskLevel: "low",
    interventionNeeded: false,
    followUpRequired: false
  }
};

// Historical mood data for trends
export const moodHistory = [
  { date: "2025-08-04", mood: 6, sleep: 6.5, exercise: 0, stress: "high" },
  { date: "2025-08-03", mood: 5, sleep: 5.0, exercise: 45, stress: "high" },
  { date: "2025-08-02", mood: 8, sleep: 8.0, exercise: 60, stress: "low" },
  { date: "2025-08-01", mood: 7, sleep: 7.5, exercise: 30, stress: "moderate" },
  { date: "2025-07-31", mood: 6, sleep: 6.0, exercise: 0, stress: "moderate" },
  { date: "2025-07-30", mood: 9, sleep: 8.5, exercise: 45, stress: "low" },
  { date: "2025-07-29", mood: 7, sleep: 7.0, exercise: 30, stress: "moderate" }
];

// Healing-Focused AI Insights
export const healingInsights = {
  wellnessAssessment: {
    currentState: "stable_with_growth_opportunities",
    wellnessScore: 73,
    scoreChange: +15,
    strengthAreas: ["sleep_consistency", "exercise_routine"],
    growthAreas: ["anxiety_management", "stress_response"],
    riskFactors: []
  },
  personalizedRecommendations: [
    {
      id: "rec_breathing",
      type: "immediate_intervention",
      priority: "high",
      category: "anxiety_support",
      title: "Guided Breathing for Presentation Calm",
      description: "A 4-7-8 breathing technique specifically designed for pre-presentation anxiety",
      duration: "3 minutes",
      evidenceBased: true,
      healingBenefit: "Activates parasympathetic nervous system, reduces cortisol",
      icon: "🌿",
      action: "start_breathing_exercise"
    },
    {
      id: "rec_mindfulness",
      type: "healing_practice",
      priority: "medium",
      category: "emotional_balance",
      title: "Present Moment Awareness",
      description: "Ground yourself with a brief mindfulness exercise",
      duration: "5 minutes",
      evidenceBased: true,
      healingBenefit: "Reduces rumination, increases emotional regulation",
      icon: "🧘‍♀️",
      action: "start_mindfulness"
    },
    {
      id: "rec_gratitude",
      type: "reflective_practice",
      priority: "medium",
      category: "emotional_healing",
      title: "Expand Your Gratitude Practice",
      description: "Build on today's gratitude to strengthen resilience",
      duration: "4 minutes",
      evidenceBased: true,
      healingBenefit: "Increases positive neural pathways, improves mood stability",
      icon: "💝",
      action: "gratitude_journal"
    }
  ],
  healingPatterns: {
    trends: {
      moodStability: "improving",
      stressResponse: "learning_to_cope",
      sleepImpact: "strongly_positive",
      exerciseCorrelation: "moderately_positive"
    },
    insights: [
      "Your mood shows 23% improvement on days with 7+ hours of sleep - prioritizing rest is healing",
      "Exercise creates lasting mood benefits for 2-3 days - your body remembers movement",
      "You're developing healthy coping strategies - this is emotional growth in action"
    ],
    healingMilestones: [
      {
        achievement: "5-day consistency streak",
        healingValue: "Building self-awareness is the foundation of emotional healing",
        dateAchieved: "2025-08-05"
      }
    ]
  }
};

// Healing Goals and Progress
export const healingGoals = {
  activeGoals: [
    {
      goalId: "goal_emotional_regulation",
      category: "emotional_healing",
      title: "Emotional Awareness & Regulation",
      description: "Develop deeper awareness of emotional patterns and healthy regulation strategies",
      targetMetrics: {
        moodConsistency: { current: 75, target: 85 },
        anxietyManagement: { current: 60, target: 80 },
        stressResponse: { current: 70, target: 85 }
      },
      healingPractices: [
        "Daily mood tracking",
        "Breathing exercises",
        "Mindfulness meditation"
      ],
      progress: {
        streak: 5,
        weeklyCompletion: 85,
        milestones: ["First week completed", "Anxiety awareness improved"]
      },
      isActive: true
    },
    {
      goalId: "goal_sleep_restoration",
      category: "physical_healing",
      title: "Restorative Sleep Patterns",
      description: "Establish consistent, healing sleep patterns for emotional regulation",
      targetMetrics: {
        sleepConsistency: { current: 80, target: 90 },
        sleepQuality: { current: 75, target: 85 },
        morningEnergy: { current: 70, target: 85 }
      },
      healingPractices: [
        "7+ hours nightly",
        "Evening wind-down routine",
        "Sleep hygiene practices"
      ],
      progress: {
        streak: 3,
        weeklyCompletion: 80,
        milestones: ["Consistent 7+ hours achieved"]
      },
      isActive: true
    },
    {
      goalId: "goal_stress_resilience",
      category: "coping_skills",
      title: "Stress Resilience Building",
      description: "Develop adaptive coping strategies and stress resilience",
      targetMetrics: {
        copingEffectiveness: { current: 65, target: 85 },
        recoveryTime: { current: 70, target: 80 },
        stressPreventtion: { current: 60, target: 75 }
      },
      healingPractices: [
        "Preventive stress management",
        "Adaptive coping strategies",
        "Regular self-care"
      ],
      progress: {
        streak: 2,
        weeklyCompletion: 70,
        milestones: ["Breathing techniques mastered"]
      },
      isActive: true
    }
  ]
};

// Community Data
export const communityData = {
  supportCircle: {
    name: "Young Professionals - Anxiety Support",
    memberCount: 127,
    activity: "high",
    newPosts: 3,
    yourRole: "active_member"
  },
  recentPosts: [
    {
      id: "post_1",
      author: "Anonymous",
      content: "Just hit a 7-day mood tracking streak! The insights are amazing.",
      timestamp: "2 hours ago",
      reactions: 12,
      replies: 3
    },
    {
      id: "post_2", 
      author: "MindfulMike",
      content: "Breathing exercises before presentations are game-changers 🧘",
      timestamp: "4 hours ago",
      reactions: 8,
      replies: 5
    }
  ],
  suggestedConnections: [
    {
      userId: "user_789",
      name: "Sam",
      compatibilityScore: 0.87,
      commonInterests: ["anxiety_management", "workplace_wellness"],
      status: "available_for_buddy"
    }
  ]
};

// Crisis Prevention and Safety
export const safetyAssessment = {
  currentRiskLevel: "low",
  riskFactors: [],
  protectiveFactors: [
    "Strong social support",
    "Active coping strategies",
    "Professional help awareness",
    "Consistent self-care"
  ],
  safetyPlan: {
    warningSignsIdentified: [
      "Persistent low mood for 3+ days",
      "Social withdrawal",
      "Sleep disruption"
    ],
    copingStrategies: [
      "Contact support person",
      "Use breathing exercises",
      "Engage in physical activity"
    ],
    emergencyContacts: [
      {
        name: "Crisis Text Line",
        contact: "Text HOME to 741741",
        available: "24/7",
        type: "crisis_support"
      },
      {
        name: "National Suicide Prevention Lifeline",
        contact: "988",
        available: "24/7",
        type: "crisis_support"
      }
    ],
    professionalSupport: {
      hasTherapist: false,
      recommendations: [
        {
          type: "therapy_referral",
          reason: "Preventive mental health support",
          urgency: "routine",
          specializations: ["anxiety", "stress_management"]
        }
      ]
    }
  }
};

// Healing Journey Flow
export const healingFlow = {
  immediate: {
    acknowledgment: {
      title: "Your healing journey continues 🌱",
      message: "Thank you for taking time to check in with yourself. This act of self-awareness is profound healing work.",
      moodValidation: "A mood of 7/10 with some anxiety is completely valid - you're human, and all feelings have wisdom."
    },
    healingSuggestion: {
      primary: {
        title: "Breathe into this moment",
        description: "Your body is holding some tension around your presentation. Let's release it together.",
        action: "guided_breathing",
        duration: "3 minutes",
        healingIntent: "nervous_system_regulation"
      },
      secondary: [
        {
          title: "Honor your growth",
          description: "Reflect on how you've grown through challenges before",
          action: "strength_reflection",
          duration: "2 minutes"
        },
        {
          title: "Set a healing intention",
          description: "Choose one way to nurture yourself today",
          action: "intention_setting",
          duration: "1 minute"
        }
      ]
    }
  },
  nextSteps: {
    healingPractices: [
      {
        id: "breathing_exercise",
        title: "Anxiety-Soothing Breath Work",
        type: "active_healing",
        description: "4-7-8 breathing technique with guided visualization",
        benefits: ["Calms nervous system", "Reduces cortisol", "Increases confidence"],
        duration: "3-5 minutes",
        difficulty: "beginner"
      },
      {
        id: "body_awareness",
        title: "Tension Release Scan",
        type: "somatic_healing",
        description: "Notice and gently release physical tension",
        benefits: ["Reduces anxiety", "Increases body awareness", "Promotes relaxation"],
        duration: "5 minutes",
        difficulty: "beginner"
      },
      {
        id: "positive_visualization",
        title: "Successful Outcome Visualization",
        type: "cognitive_healing",
        description: "Visualize your presentation going well with calm confidence",
        benefits: ["Builds confidence", "Reduces anticipatory anxiety", "Programs success"],
        duration: "3 minutes",
        difficulty: "intermediate"
      }
    ],
    reflectiveQuestions: [
      "What is one thing you're grateful for about your preparation process?",
      "How can you show yourself compassion during this challenging time?",
      "What would you tell a dear friend facing the same situation?"
    ],
    healingReminders: [
      {
        time: "1 hour before presentation",
        message: "You are prepared. You are capable. Breathe and trust yourself.",
        action: "quick_confidence_boost"
      },
      {
        time: "tonight before bed",
        message: "Reflect on today's courage - you faced anxiety with awareness and care.",
        action: "gratitude_practice"
      }
    ]
  }
};

// Gamification Elements
export const achievements = {
  justEarned: {
    id: "streak_5_days",
    name: "Consistency Champion",
    description: "5 days of mood tracking in a row!",
    icon: "🏆",
    points: 50,
    rarity: "common"
  },
  progress: [
    {
      id: "mood_master",
      name: "Mood Master",
      description: "Track mood for 30 consecutive days",
      progress: 5,
      target: 30,
      icon: "📈"
    },
    {
      id: "insight_seeker", 
      name: "Insight Seeker",
      description: "Discover 10 personal wellness patterns",
      progress: 3,
      target: 10,
      icon: "🔍"
    }
  ]
};

// Professional Integration (if applicable)
export const professionalIntegration = {
  hasTherapist: false,
  availableFeatures: {
    therapistFinder: true,
    progressSharing: true,
    sessionPlanning: false
  },
  recommendations: [
    {
      type: "find_therapist",
      title: "Connect with a Professional",
      description: "Based on your progress, you might benefit from professional support",
      cta: "Find Therapists in Your Area"
    }
  ]
};

// Notification Data
export const notifications = {
  immediate: [
    {
      id: "notif_1",
      type: "achievement",
      title: "Achievement Unlocked! 🏆",
      message: "5-day mood tracking streak completed",
      timestamp: "just now",
      priority: "medium"
    }
  ],
  scheduled: [
    {
      id: "notif_2",
      type: "reminder",
      title: "Tomorrow's Mood Check-in",
      message: "Don't forget your daily wellness check-in",
      scheduledFor: "2025-08-06T14:30:00Z"
    },
    {
      id: "notif_3",
      type: "insight",
      title: "Weekly Insights Ready",
      message: "Your personalized wellness report is available", 
      scheduledFor: "2025-08-11T10:00:00Z"
    }
  ]
};

// Export production-ready mood flow data
export const productionMoodFlowData = {
  userProfile,
  moodEntry,
  moodHistory,
  healingInsights,
  healingGoals,
  communityData,
  safetyAssessment,
  healingFlow,
  achievements,
  professionalIntegration,
  notifications
};

export default productionMoodFlowData;
