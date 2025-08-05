import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email?: string;
  name?: string;
  avatar?: string;
  isGuest: boolean;
  createdAt: string;
  preferences: {
    notifications: boolean;
    reminderTime: string;
    privacyLevel: 'private' | 'community' | 'public';
    language: string;
    theme: 'light' | 'dark' | 'auto';
  };
}

export interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface UserActions {
  setUser: (user: User) => void;
  updateUser: (updates: Partial<User>) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  createGuestUser: () => void;
  updatePreferences: (preferences: Partial<User['preferences']>) => void;
}

export type UserStore = UserState & UserActions;

const initialState: UserState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

export const useUserStore = create<UserStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      setUser: (user: User) => 
        set({ user, isAuthenticated: true, error: null }),
      
      updateUser: (updates: Partial<User>) => 
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null
        })),
      
      logout: () => 
        set({ user: null, isAuthenticated: false, error: null }),
      
      setLoading: (loading: boolean) => 
        set({ isLoading: loading }),
      
      setError: (error: string | null) => 
        set({ error }),
      
      createGuestUser: () => {
        const guestUser: User = {
          id: `guest_${Date.now()}`,
          isGuest: true,
          createdAt: new Date().toISOString(),
          preferences: {
            notifications: false,
            reminderTime: '09:00',
            privacyLevel: 'private',
            language: 'en',
            theme: 'auto',
          }
        };
        set({ user: guestUser, isAuthenticated: true });
      },
      
      updatePreferences: (preferences: Partial<User['preferences']>) =>
        set((state) => ({
          user: state.user ? {
            ...state.user,
            preferences: { ...state.user.preferences, ...preferences }
          } : null
        })),
    }),
    {
      name: 'user-store',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
