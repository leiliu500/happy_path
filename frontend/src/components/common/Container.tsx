import React from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

// Import theme
import { useTheme } from '../../theme/ThemeProvider';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface ContainerProps {
  children: React.ReactNode;
  style?: any;
  scrollable?: boolean;
  centered?: boolean;
  gradient?: boolean;
  safeArea?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  backgroundColor?: string;
}

const Container: React.FC<ContainerProps> = ({
  children,
  style,
  scrollable = false,
  centered = false,
  gradient = false,
  safeArea = true,
  padding = 'lg',
  backgroundColor,
}) => {
  const { colors, spacing } = useTheme();

  const getPadding = () => {
    switch (padding) {
      case 'none': return 0;
      case 'sm': return spacing.sm;
      case 'md': return spacing.md;
      case 'lg': return spacing.lg;
      case 'xl': return spacing.xl;
      default: return spacing.lg;
    }
  };

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: backgroundColor || colors.background,
    },
    gradientContainer: {
      flex: 1,
    },
    content: {
      flex: 1,
      padding: getPadding(),
      justifyContent: centered ? 'center' : 'flex-start',
      alignItems: centered ? 'center' : 'stretch',
    },
    scrollContent: {
      flexGrow: 1,
      padding: getPadding(),
      justifyContent: centered ? 'center' : 'flex-start',
      alignItems: centered ? 'center' : 'stretch',
      minHeight: centered ? screenHeight - 100 : undefined,
    },
  });

  const renderContent = () => (
    <>
      <StatusBar 
        barStyle="dark-content" 
        backgroundColor="transparent" 
        translucent 
      />
      {scrollable ? (
        <ScrollView
          style={{ flex: 1 }}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {children}
        </ScrollView>
      ) : (
        <View style={styles.content}>
          {children}
        </View>
      )}
    </>
  );

  const containerContent = gradient ? (
    <LinearGradient
      colors={[
        'rgba(59, 130, 246, 0.03)',
        'rgba(20, 184, 166, 0.03)',
        'rgba(139, 92, 246, 0.03)',
      ]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.gradientContainer}
    >
      {renderContent()}
    </LinearGradient>
  ) : (
    renderContent()
  );

  if (safeArea) {
    return (
      <SafeAreaView style={[styles.container, style]}>
        {containerContent}
      </SafeAreaView>
    );
  }

  return (
    <View style={[styles.container, style]}>
      {containerContent}
    </View>
  );
};

export default Container;
