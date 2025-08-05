import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Types for onboarding flow
export interface WellnessFocus {
  id: string;
  label: string;
  icon: string;
  description: string;
}

export interface OnboardingState {
  // Current onboarding step
  currentStep: number;
  totalSteps: number;
  
  // User selections during onboarding
  selectedWellnessFocus: WellnessFocus | null;
  currentMood: number; // 1-10 scale
  biggestChallenge: string;
  hasCompletedFirstActivity: boolean;
  
  // Registration state
  isRegistered: boolean;
  isGuestMode: boolean;
  guestModeStartTime: number | null;
  
  // Progress tracking
  onboardingProgress: {
    welcomeCompleted: boolean;
    assessmentCompleted: boolean;
    firstActivityCompleted: boolean;
    registrationOffered: boolean;
    registrationCompleted: boolean;
  };
}

export interface OnboardingActions {
  // Navigation
  setCurrentStep: (step: number) => void;
  nextStep: () => void;
  previousStep: () => void;
  
  // Data collection
  setWellnessFocus: (focus: WellnessFocus) => void;
  setCurrentMood: (mood: number) => void;
  setBiggestChallenge: (challenge: string) => void;
  markFirstActivityCompleted: () => void;
  
  // Registration
  enterGuestMode: () => void;
  completeRegistration: () => void;
  
  // Progress tracking
  markStepCompleted: (step: keyof OnboardingState['onboardingProgress']) => void;
  resetOnboarding: () => void;
}

export type OnboardingStore = OnboardingState & OnboardingActions;

// Predefined wellness focus options based on UI dashboard spec
export const WELLNESS_FOCUS_OPTIONS: WellnessFocus[] = [
  {
    id: 'stress-anxiety',
    label: 'Stress & Anxiety',
    icon: '🧘',
    description: 'Manage daily stress and anxious thoughts'
  },
  {
    id: 'depression-support',
    label: 'Depression Support',
    icon: '😔',
    description: 'Support for low mood and depression'
  },
  {
    id: 'sleep-rest',
    label: 'Sleep & Rest',
    icon: '😴',
    description: 'Improve sleep quality and rest patterns'
  },
  {
    id: 'general-wellness',
    label: 'General Wellness',
    icon: '🏃',
    description: 'Overall mental and physical wellness'
  },
  {
    id: 'relationship-health',
    label: 'Relationship Health',
    icon: '👥',
    description: 'Improve relationships and social connections'
  },
  {
    id: 'personal-growth',
    label: 'Personal Growth',
    icon: '🎯',
    description: 'Self-improvement and personal development'
  }
];

const initialState: OnboardingState = {
  currentStep: 0,
  totalSteps: 5,
  selectedWellnessFocus: null,
  currentMood: 5,
  biggestChallenge: '',
  hasCompletedFirstActivity: false,
  isRegistered: false,
  isGuestMode: false,
  guestModeStartTime: null,
  onboardingProgress: {
    welcomeCompleted: false,
    assessmentCompleted: false,
    firstActivityCompleted: false,
    registrationOffered: false,
    registrationCompleted: false,
  }
};

export const useOnboardingStore = create<OnboardingStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      // Navigation actions
      setCurrentStep: (step: number) => 
        set({ currentStep: Math.max(0, Math.min(step, get().totalSteps - 1)) }),
      
      nextStep: () => 
        set((state) => ({ 
          currentStep: Math.min(state.currentStep + 1, state.totalSteps - 1) 
        })),
      
      previousStep: () => 
        set((state) => ({ 
          currentStep: Math.max(state.currentStep - 1, 0) 
        })),
      
      // Data collection actions
      setWellnessFocus: (focus: WellnessFocus) => 
        set({ selectedWellnessFocus: focus }),
      
      setCurrentMood: (mood: number) => 
        set({ currentMood: Math.max(1, Math.min(mood, 10)) }),
      
      setBiggestChallenge: (challenge: string) => 
        set({ biggestChallenge: challenge }),
      
      markFirstActivityCompleted: () => 
        set({ 
          hasCompletedFirstActivity: true,
          onboardingProgress: {
            ...get().onboardingProgress,
            firstActivityCompleted: true
          }
        }),
      
      // Registration actions
      enterGuestMode: () => 
        set({ 
          isGuestMode: true, 
          guestModeStartTime: Date.now() 
        }),
      
      completeRegistration: () => 
        set({ 
          isRegistered: true, 
          isGuestMode: false,
          onboardingProgress: {
            ...get().onboardingProgress,
            registrationCompleted: true
          }
        }),
      
      // Progress tracking
      markStepCompleted: (step: keyof OnboardingState['onboardingProgress']) =>
        set((state) => ({
          onboardingProgress: {
            ...state.onboardingProgress,
            [step]: true
          }
        })),
      
      resetOnboarding: () => set(initialState),
    }),
    {
      name: 'onboarding-store',
      partialize: (state) => ({
        selectedWellnessFocus: state.selectedWellnessFocus,
        currentMood: state.currentMood,
        biggestChallenge: state.biggestChallenge,
        hasCompletedFirstActivity: state.hasCompletedFirstActivity,
        isRegistered: state.isRegistered,
        isGuestMode: state.isGuestMode,
        guestModeStartTime: state.guestModeStartTime,
        onboardingProgress: state.onboardingProgress,
      }),
    }
  )
);
