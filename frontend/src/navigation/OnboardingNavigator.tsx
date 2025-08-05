import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

// Import onboarding screens
import WelcomeScreen from '../screens/onboarding/WelcomeScreen';
import WellnessFocusScreen from '../screens/onboarding/WellnessFocusScreen';
import QuickAssessmentScreen from '../screens/onboarding/QuickAssessmentScreen';
import FirstExperienceScreen from '../screens/onboarding/FirstExperienceScreen';
import RegistrationScreen from '../screens/onboarding/RegistrationScreen';
import GuestModeScreen from '../screens/onboarding/GuestModeScreen';

export type OnboardingStackParamList = {
  Welcome: undefined;
  WellnessFocus: undefined;
  QuickAssessment: undefined;
  FirstExperience: { activityType?: string };
  Registration: { fromActivity?: boolean };
  GuestMode: undefined;
};

const Stack = createStackNavigator<OnboardingStackParamList>();

const OnboardingNavigator = () => {
  return (
    <Stack.Navigator
      initialRouteName="Welcome"
      screenOptions={{
        headerShown: false,
        gestureEnabled: true,
        cardStyleInterpolator: ({ current, next, layouts }) => {
          return {
            cardStyle: {
              transform: [
                {
                  translateX: current.progress.interpolate({
                    inputRange: [0, 1],
                    outputRange: [layouts.screen.width, 0],
                  }),
                },
                {
                  scale: next
                    ? next.progress.interpolate({
                        inputRange: [0, 1],
                        outputRange: [1, 0.9],
                      })
                    : 1,
                },
              ],
            },
            overlayStyle: {
              opacity: current.progress.interpolate({
                inputRange: [0, 1],
                outputRange: [0, 0.5],
              }),
            },
          };
        },
      }}
    >
      <Stack.Screen 
        name="Welcome" 
        component={WelcomeScreen}
        options={{ gestureEnabled: false }}
      />
      <Stack.Screen 
        name="WellnessFocus" 
        component={WellnessFocusScreen}
      />
      <Stack.Screen 
        name="QuickAssessment" 
        component={QuickAssessmentScreen}
      />
      <Stack.Screen 
        name="FirstExperience" 
        component={FirstExperienceScreen}
      />
      <Stack.Screen 
        name="Registration" 
        component={RegistrationScreen}
      />
      <Stack.Screen 
        name="GuestMode" 
        component={GuestModeScreen}
      />
    </Stack.Navigator>
  );
};

export default OnboardingNavigator;
