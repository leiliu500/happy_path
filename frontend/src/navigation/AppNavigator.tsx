import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Platform } from 'react-native';

// Import screens
import OnboardingNavigator from './OnboardingNavigator';
import DashboardScreen from '../screens/DashboardScreen';
import ProgressScreen from '../screens/ProgressScreen';
import CommunityScreen from '../screens/CommunityScreen';
import SettingsScreen from '../screens/SettingsScreen';

// Import components
import TabBar from '../components/navigation/TabBar';
import { useStores } from '../stores/StoreProvider';

export type RootStackParamList = {
  Onboarding: undefined;
  Main: undefined;
  Dashboard: undefined;
  Progress: undefined;
  Community: undefined;
  Settings: undefined;
  MoodCheckin: undefined;
  JournalingSession: undefined;
  MeditationSession: { type: string; duration: number };
  CrisisSupport: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();

// Main tab navigator for authenticated users
const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      tabBar={(props) => <TabBar {...props} />}
      screenOptions={{
        headerShown: false,
        tabBarShowLabel: Platform.OS !== 'web',
      }}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{
          tabBarIcon: 'home',
          tabBarLabel: 'Home',
        }}
      />
      <Tab.Screen 
        name="Progress" 
        component={ProgressScreen}
        options={{
          tabBarIcon: 'trending-up',
          tabBarLabel: 'Progress',
        }}
      />
      <Tab.Screen 
        name="Community" 
        component={CommunityScreen}
        options={{
          tabBarIcon: 'users',
          tabBarLabel: 'Community',
        }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{
          tabBarIcon: 'settings',
          tabBarLabel: 'Settings',
        }}
      />
    </Tab.Navigator>
  );
};

// Main app navigator
const AppNavigator = () => {
  const { userStore, onboardingStore } = useStores();
  
  // Determine initial route based on authentication and onboarding status
  const getInitialRoute = () => {
    if (!userStore.isAuthenticated) {
      return 'Onboarding';
    }
    
    if (!onboardingStore.onboardingProgress.registrationCompleted) {
      return 'Onboarding';
    }
    
    return 'Main';
  };

  return (
    <Stack.Navigator
      initialRouteName={getInitialRoute()}
      screenOptions={{
        headerShown: false,
        gestureEnabled: true,
        cardStyleInterpolator: ({ current, layouts }) => {
          return {
            cardStyle: {
              transform: [
                {
                  translateX: current.progress.interpolate({
                    inputRange: [0, 1],
                    outputRange: [layouts.screen.width, 0],
                  }),
                },
              ],
            },
          };
        },
      }}
    >
      <Stack.Screen 
        name="Onboarding" 
        component={OnboardingNavigator}
        options={{ gestureEnabled: false }}
      />
      <Stack.Screen 
        name="Main" 
        component={MainTabNavigator}
        options={{ gestureEnabled: false }}
      />
    </Stack.Navigator>
  );
};

export default AppNavigator;
