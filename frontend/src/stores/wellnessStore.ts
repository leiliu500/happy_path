import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface MoodEntry {
  id: string;
  mood: number; // 1-10 scale
  energy: number; // 1-10 scale
  stress: number; // 1-10 scale
  note?: string;
  timestamp: string;
  tags?: string[];
}

export interface WellnessGoal {
  id: string;
  title: string;
  description: string;
  type: 'mood' | 'habit' | 'activity' | 'mindfulness';
  targetValue: number;
  currentValue: number;
  unit: string;
  deadline?: string;
  isCompleted: boolean;
  createdAt: string;
}

export interface WellnessActivity {
  id: string;
  type: 'breathing' | 'meditation' | 'journaling' | 'reflection' | 'music';
  title: string;
  description: string;
  duration: number; // in minutes
  completedAt?: string;
  rating?: number; // 1-5 scale
  notes?: string;
}

export interface WellnessInsight {
  id: string;
  type: 'mood_trend' | 'goal_progress' | 'activity_streak' | 'correlation';
  title: string;
  description: string;
  data: any;
  generatedAt: string;
  isViewed: boolean;
}

export interface WellnessState {
  // Current wellness metrics
  currentMood: number;
  currentEnergy: number;
  currentStress: number;
  wellnessScore: number; // 0-100
  
  // Historical data
  moodEntries: MoodEntry[];
  completedActivities: WellnessActivity[];
  goals: WellnessGoal[];
  insights: WellnessInsight[];
  
  // Streaks and achievements
  currentStreak: number;
  longestStreak: number;
  totalActivitiesCompleted: number;
  
  // Loading states
  isLoading: boolean;
  error: string | null;
}

export interface WellnessActions {
  // Mood tracking
  logMood: (entry: Omit<MoodEntry, 'id' | 'timestamp'>) => void;
  updateMoodEntry: (id: string, updates: Partial<MoodEntry>) => void;
  deleteMoodEntry: (id: string) => void;
  
  // Activities
  completeActivity: (activity: Omit<WellnessActivity, 'id' | 'completedAt'>) => void;
  rateActivity: (id: string, rating: number, notes?: string) => void;
  
  // Goals
  createGoal: (goal: Omit<WellnessGoal, 'id' | 'createdAt' | 'isCompleted' | 'currentValue'>) => void;
  updateGoal: (id: string, updates: Partial<WellnessGoal>) => void;
  incrementGoalProgress: (id: string, amount: number) => void;
  completeGoal: (id: string) => void;
  deleteGoal: (id: string) => void;
  
  // Insights
  addInsight: (insight: Omit<WellnessInsight, 'id' | 'generatedAt' | 'isViewed'>) => void;
  markInsightViewed: (id: string) => void;
  
  // Calculations
  calculateWellnessScore: () => void;
  updateStreaks: () => void;
  
  // Utils
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearData: () => void;
}

export type WellnessStore = WellnessState & WellnessActions;

const initialState: WellnessState = {
  currentMood: 5,
  currentEnergy: 5,
  currentStress: 5,
  wellnessScore: 0,
  moodEntries: [],
  completedActivities: [],
  goals: [],
  insights: [],
  currentStreak: 0,
  longestStreak: 0,
  totalActivitiesCompleted: 0,
  isLoading: false,
  error: null,
};

export const useWellnessStore = create<WellnessStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      // Mood tracking actions
      logMood: (entry: Omit<MoodEntry, 'id' | 'timestamp'>) => {
        const newEntry: MoodEntry = {
          ...entry,
          id: `mood_${Date.now()}`,
          timestamp: new Date().toISOString(),
        };
        
        set((state) => ({
          moodEntries: [newEntry, ...state.moodEntries],
          currentMood: entry.mood,
          currentEnergy: entry.energy,
          currentStress: entry.stress,
        }));
        
        // Recalculate wellness score and streaks
        get().calculateWellnessScore();
        get().updateStreaks();
      },
      
      updateMoodEntry: (id: string, updates: Partial<MoodEntry>) =>
        set((state) => ({
          moodEntries: state.moodEntries.map(entry =>
            entry.id === id ? { ...entry, ...updates } : entry
          )
        })),
      
      deleteMoodEntry: (id: string) =>
        set((state) => ({
          moodEntries: state.moodEntries.filter(entry => entry.id !== id)
        })),
      
      // Activity actions
      completeActivity: (activity: Omit<WellnessActivity, 'id' | 'completedAt'>) => {
        const newActivity: WellnessActivity = {
          ...activity,
          id: `activity_${Date.now()}`,
          completedAt: new Date().toISOString(),
        };
        
        set((state) => ({
          completedActivities: [newActivity, ...state.completedActivities],
          totalActivitiesCompleted: state.totalActivitiesCompleted + 1,
        }));
        
        get().calculateWellnessScore();
        get().updateStreaks();
      },
      
      rateActivity: (id: string, rating: number, notes?: string) =>
        set((state) => ({
          completedActivities: state.completedActivities.map(activity =>
            activity.id === id ? { ...activity, rating, notes } : activity
          )
        })),
      
      // Goal actions
      createGoal: (goal: Omit<WellnessGoal, 'id' | 'createdAt' | 'isCompleted' | 'currentValue'>) => {
        const newGoal: WellnessGoal = {
          ...goal,
          id: `goal_${Date.now()}`,
          createdAt: new Date().toISOString(),
          isCompleted: false,
          currentValue: 0,
        };
        
        set((state) => ({
          goals: [newGoal, ...state.goals]
        }));
      },
      
      updateGoal: (id: string, updates: Partial<WellnessGoal>) =>
        set((state) => ({
          goals: state.goals.map(goal =>
            goal.id === id ? { ...goal, ...updates } : goal
          )
        })),
      
      incrementGoalProgress: (id: string, amount: number) =>
        set((state) => ({
          goals: state.goals.map(goal =>
            goal.id === id 
              ? { 
                  ...goal, 
                  currentValue: Math.min(goal.currentValue + amount, goal.targetValue),
                  isCompleted: goal.currentValue + amount >= goal.targetValue
                } 
              : goal
          )
        })),
      
      completeGoal: (id: string) =>
        set((state) => ({
          goals: state.goals.map(goal =>
            goal.id === id ? { ...goal, isCompleted: true } : goal
          )
        })),
      
      deleteGoal: (id: string) =>
        set((state) => ({
          goals: state.goals.filter(goal => goal.id !== id)
        })),
      
      // Insight actions
      addInsight: (insight: Omit<WellnessInsight, 'id' | 'generatedAt' | 'isViewed'>) => {
        const newInsight: WellnessInsight = {
          ...insight,
          id: `insight_${Date.now()}`,
          generatedAt: new Date().toISOString(),
          isViewed: false,
        };
        
        set((state) => ({
          insights: [newInsight, ...state.insights]
        }));
      },
      
      markInsightViewed: (id: string) =>
        set((state) => ({
          insights: state.insights.map(insight =>
            insight.id === id ? { ...insight, isViewed: true } : insight
          )
        })),
      
      // Calculation functions
      calculateWellnessScore: () => {
        const state = get();
        const recentMoodEntries = state.moodEntries.slice(0, 7); // Last 7 entries
        const recentActivities = state.completedActivities.filter(
          activity => {
            const activityDate = new Date(activity.completedAt!);
            const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
            return activityDate > weekAgo;
          }
        );
        
        let score = 50; // Base score
        
        // Mood component (40% of score)
        if (recentMoodEntries.length > 0) {
          const avgMood = recentMoodEntries.reduce((sum, entry) => sum + entry.mood, 0) / recentMoodEntries.length;
          const avgEnergy = recentMoodEntries.reduce((sum, entry) => sum + entry.energy, 0) / recentMoodEntries.length;
          const avgStress = recentMoodEntries.reduce((sum, entry) => sum + (11 - entry.stress), 0) / recentMoodEntries.length; // Invert stress
          
          score = (avgMood + avgEnergy + avgStress) / 3 * 10 * 0.4 + score * 0.6;
        }
        
        // Activity component (30% of score)
        const activityBonus = Math.min(recentActivities.length * 5, 30);
        
        // Goal completion component (30% of score)
        const completedGoals = state.goals.filter(goal => goal.isCompleted).length;
        const goalBonus = Math.min(completedGoals * 10, 30);
        
        const finalScore = Math.min(Math.max(score + activityBonus + goalBonus, 0), 100);
        
        set({ wellnessScore: Math.round(finalScore) });
      },
      
      updateStreaks: () => {
        const state = get();
        const sortedEntries = [...state.moodEntries].sort(
          (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        );
        
        let currentStreak = 0;
        let longestStreak = 0;
        let tempStreak = 0;
        
        const today = new Date();
        let checkDate = new Date(today);
        
        // Calculate current streak
        for (let i = 0; i < sortedEntries.length; i++) {
          const entryDate = new Date(sortedEntries[i].timestamp);
          const diffDays = Math.floor((checkDate.getTime() - entryDate.getTime()) / (1000 * 60 * 60 * 24));
          
          if (diffDays === i) {
            currentStreak++;
            tempStreak++;
            longestStreak = Math.max(longestStreak, tempStreak);
          } else {
            break;
          }
        }
        
        // Calculate longest streak from all entries
        tempStreak = 0;
        for (let i = 0; i < sortedEntries.length - 1; i++) {
          const currentEntry = new Date(sortedEntries[i].timestamp);
          const nextEntry = new Date(sortedEntries[i + 1].timestamp);
          const diffDays = Math.floor((currentEntry.getTime() - nextEntry.getTime()) / (1000 * 60 * 60 * 24));
          
          if (diffDays === 1) {
            tempStreak++;
          } else {
            longestStreak = Math.max(longestStreak, tempStreak + 1);
            tempStreak = 0;
          }
        }
        
        set({ 
          currentStreak,
          longestStreak: Math.max(longestStreak, state.longestStreak)
        });
      },
      
      // Utility actions
      setLoading: (loading: boolean) => set({ isLoading: loading }),
      setError: (error: string | null) => set({ error }),
      clearData: () => set(initialState),
    }),
    {
      name: 'wellness-store',
      partialize: (state) => ({
        moodEntries: state.moodEntries,
        completedActivities: state.completedActivities,
        goals: state.goals,
        insights: state.insights,
        currentStreak: state.currentStreak,
        longestStreak: state.longestStreak,
        totalActivitiesCompleted: state.totalActivitiesCompleted,
        wellnessScore: state.wellnessScore,
      }),
    }
  )
);
