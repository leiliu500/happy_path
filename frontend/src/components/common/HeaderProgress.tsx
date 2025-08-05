import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Pressable,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  Easing,
} from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';

// Import theme
import { useTheme } from '../../theme/ThemeProvider';

interface HeaderProgressProps {
  title: string;
  subtitle?: string;
  currentStep: number;
  totalSteps: number;
  onBack?: () => void;
  showBack?: boolean;
}

const HeaderProgress: React.FC<HeaderProgressProps> = ({
  title,
  subtitle,
  currentStep,
  totalSteps,
  onBack,
  showBack = true,
}) => {
  const { colors, typography, spacing, borderRadius } = useTheme();
  
  // Calculate progress percentage
  const progressPercentage = (currentStep / totalSteps) * 100;
  
  // Animated progress value
  const progressWidth = useSharedValue(0);
  
  React.useEffect(() => {
    progressWidth.value = withTiming(progressPercentage, {
      duration: 500,
      easing: Easing.bezier(0.4, 0, 0.2, 1),
    });
  }, [progressPercentage]);

  // Animated style for progress bar
  const animatedProgressStyle = useAnimatedStyle(() => ({
    width: `${progressWidth.value}%`,
  }));

  const styles = StyleSheet.create({
    container: {
      backgroundColor: colors.background,
      borderBottomWidth: 1,
      borderBottomColor: colors.border,
    },
    header: {
      paddingHorizontal: spacing.lg,
      paddingVertical: spacing.md,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
    },
    leftSection: {
      flex: 1,
      flexDirection: 'row',
      alignItems: 'center',
    },
    backButton: {
      width: 40,
      height: 40,
      borderRadius: 20,
      backgroundColor: colors.backgroundSecondary,
      alignItems: 'center',
      justifyContent: 'center',
      marginRight: spacing.md,
    },
    titleSection: {
      flex: 1,
    },
    title: {
      ...typography.h2,
      color: colors.textPrimary,
      marginBottom: subtitle ? spacing.xs : 0,
    },
    subtitle: {
      ...typography.body,
      color: colors.textSecondary,
    },
    stepIndicator: {
      alignItems: 'flex-end',
    },
    stepText: {
      ...typography.caption,
      color: colors.textSecondary,
      marginBottom: spacing.xs,
    },
    progressContainer: {
      paddingHorizontal: spacing.lg,
      paddingBottom: spacing.md,
    },
    progressTrack: {
      height: 4,
      backgroundColor: colors.border,
      borderRadius: borderRadius.sm,
      overflow: 'hidden',
    },
    progressBar: {
      height: '100%',
      backgroundColor: colors.primary,
      borderRadius: borderRadius.sm,
    },
    progressDots: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginTop: spacing.sm,
    },
    dot: {
      width: 8,
      height: 8,
      borderRadius: 4,
      marginHorizontal: 2,
    },
    dotActive: {
      backgroundColor: colors.primary,
    },
    dotInactive: {
      backgroundColor: colors.border,
    },
    dotCompleted: {
      backgroundColor: colors.success,
    },
  });

  const renderBackButton = () => {
    if (!showBack || !onBack) return null;

    return (
      <Pressable style={styles.backButton} onPress={onBack}>
        <Ionicons 
          name="chevron-back" 
          size={20} 
          color={colors.textPrimary} 
        />
      </Pressable>
    );
  };

  const renderProgressDots = () => {
    const dots = [];
    for (let i = 1; i <= totalSteps; i++) {
      const isActive = i === currentStep;
      const isCompleted = i < currentStep;
      
      let dotStyle = styles.dotInactive;
      if (isCompleted) {
        dotStyle = styles.dotCompleted;
      } else if (isActive) {
        dotStyle = styles.dotActive;
      }

      dots.push(
        <View 
          key={i} 
          style={[styles.dot, dotStyle]} 
        />
      );
    }
    return dots;
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.leftSection}>
          {renderBackButton()}
          <View style={styles.titleSection}>
            <Text style={styles.title}>{title}</Text>
            {subtitle && (
              <Text style={styles.subtitle}>{subtitle}</Text>
            )}
          </View>
        </View>
        
        <View style={styles.stepIndicator}>
          <Text style={styles.stepText}>
            {currentStep} of {totalSteps}
          </Text>
        </View>
      </View>

      <View style={styles.progressContainer}>
        {/* Progress Bar */}
        <View style={styles.progressTrack}>
          <Animated.View 
            style={[styles.progressBar, animatedProgressStyle]} 
          />
        </View>

        {/* Progress Dots */}
        <View style={styles.progressDots}>
          {renderProgressDots()}
        </View>
      </View>
    </SafeAreaView>
  );
};

export default HeaderProgress;
