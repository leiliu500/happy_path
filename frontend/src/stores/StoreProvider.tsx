import React, { ReactNode } from 'react';
import { createContext, useContext } from 'react';

// Import individual stores
import { useUserStore } from './userStore';
import { useWellnessStore } from './wellnessStore';
import { useOnboardingStore } from './onboardingStore';
import { useCommunityStore } from './communityStore';

interface StoreContextType {
  userStore: ReturnType<typeof useUserStore>;
  wellnessStore: ReturnType<typeof useWellnessStore>;
  onboardingStore: ReturnType<typeof useOnboardingStore>;
  communityStore: ReturnType<typeof useCommunityStore>;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

interface StoreProviderProps {
  children: ReactNode;
}

export const StoreProvider: React.FC<StoreProviderProps> = ({ children }) => {
  const userStore = useUserStore();
  const wellnessStore = useWellnessStore();
  const onboardingStore = useOnboardingStore();
  const communityStore = useCommunityStore();

  const value: StoreContextType = {
    userStore,
    wellnessStore,
    onboardingStore,
    communityStore,
  };

  return (
    <StoreContext.Provider value={value}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStores = (): StoreContextType => {
  const context = useContext(StoreContext);
  if (context === undefined) {
    throw new Error('useStores must be used within a StoreProvider');
  }
  return context;
};
