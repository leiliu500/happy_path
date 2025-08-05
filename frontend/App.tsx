import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Platform } from 'react-native';

// Import navigation
import AppNavigator from './src/navigation/AppNavigator';

// Import stores
import { StoreProvider } from './src/stores/StoreProvider';

// Import theme
import { ThemeProvider } from './src/theme/ThemeProvider';

// Import global styles
import './src/styles/globals.css';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <ThemeProvider>
          <StoreProvider>
            <NavigationContainer>
              <AppNavigator />
              <StatusBar 
                style="auto" 
                backgroundColor="transparent"
                translucent={Platform.OS === 'android'}
              />
            </NavigationContainer>
          </StoreProvider>
        </ThemeProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
