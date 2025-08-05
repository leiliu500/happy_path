import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Dimensions,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withDelay,
  withTiming,
  withRepeat,
  withSequence,
  interpolate,
} from 'react-native-reanimated';

// Import components
import Button from '../../components/common/Button';
import HeaderProgress from '../../components/common/HeaderProgress';
import BreathingExercise from '../../components/wellness/BreathingExercise';
import MeditationTimer from '../../components/wellness/MeditationTimer';
import GuidedReflection from '../../components/wellness/GuidedReflection';
import CalmingMusic from '../../components/wellness/CalmingMusic';

// Import hooks and stores
import { useTheme } from '../../theme/ThemeProvider';
import { useStores } from '../../stores/StoreProvider';
import { useNavigation, useRoute } from '@react-navigation/native';

// Import types
import type { StackNavigationProp } from '@react-navigation/stack';
import type { RouteProp } from '@react-navigation/native';
import type { OnboardingStackParamList } from '../../navigation/OnboardingNavigator';

type FirstExperienceNavigationProp = StackNavigationProp<OnboardingStackParamList, 'FirstExperience'>;
type FirstExperienceRouteProp = RouteProp<OnboardingStackParamList, 'FirstExperience'>;

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface ActivityOption {
  id: string;
  title: string;
  description: string;
  icon: string;
  duration: string;
  color: string;
  component: React.ComponentType<any>;
}

const FirstExperienceScreen: React.FC = () => {
  const { colors, typography, spacing } = useTheme();
  const { onboardingStore, wellnessStore } = useStores();
  const navigation = useNavigation<FirstExperienceNavigationProp>();
  const route = useRoute<FirstExperienceRouteProp>();

  const [selectedActivity, setSelectedActivity] = useState<ActivityOption | null>(null);
  const [isActivityActive, setIsActivityActive] = useState<boolean>(false);
  const [activityCompleted, setActivityCompleted] = useState<boolean>(false);
  const [wellnessScoreIncrease, setWellnessScoreIncrease] = useState<number>(0);

  // Animation values
  const titleOpacity = useSharedValue(0);
  const optionsOpacity = useSharedValue(0);
  const activityOpacity = useSharedValue(0);
  const completionOpacity = useSharedValue(0);
  const celebrationScale = useSharedValue(0);

  // Activity options based on user's mood and preferences
  const activityOptions: ActivityOption[] = [
    {
      id: 'breathing',
      title: '2-min Breathing Exercise',
      description: 'Guided deep breathing to calm your mind',
      icon: '🫁',
      duration: '2 min',
      color: colors.calm,
      component: BreathingExercise,
    },
    {
      id: 'reflection',
      title: 'Guided Reflection',
      description: 'Thoughtful prompts for self-discovery',
      icon: '💭',
      duration: '3 min',
      color: colors.growth,
      component: GuidedReflection,
    },
    {
      id: 'meditation',
      title: 'Mini Meditation',
      description: 'Brief mindfulness practice',
      icon: '🧘',
      duration: '5 min',
      color: colors.focus,
      component: MeditationTimer,
    },
    {
      id: 'music',
      title: 'Calming Music',
      description: 'Soothing sounds to relax your mind',
      icon: '🎵',
      duration: '3 min',
      color: colors.energy,
      component: CalmingMusic,
    },
  ];

  useEffect(() => {
    // Auto-select activity based on route params or user mood
    const activityType = route.params?.activityType || 'breathing';
    const autoSelectedActivity = activityOptions.find(option => option.id === activityType) || activityOptions[0];
    setSelectedActivity(autoSelectedActivity);

    // Start animations
    titleOpacity.value = withDelay(200, withSpring(1));
    optionsOpacity.value = withDelay(400, withSpring(1));
  }, []);

  // Animated styles
  const titleAnimatedStyle = useAnimatedStyle(() => ({
    opacity: titleOpacity.value,
    transform: [{ translateY: withSpring(titleOpacity.value === 1 ? 0 : 30) }],
  }));

  const optionsAnimatedStyle = useAnimatedStyle(() => ({
    opacity: optionsOpacity.value,
  }));

  const activityAnimatedStyle = useAnimatedStyle(() => ({
    opacity: activityOpacity.value,
    transform: [{ scale: withSpring(activityOpacity.value === 1 ? 1 : 0.9) }],
  }));

  const completionAnimatedStyle = useAnimatedStyle(() => ({
    opacity: completionOpacity.value,
  }));

  const celebrationAnimatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: celebrationScale.value }],
  }));

  // Handle activity selection
  const handleActivitySelect = async (activity: ActivityOption) => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }

    setSelectedActivity(activity);
  };

  // Handle start activity
  const handleStartActivity = async () => {
    if (!selectedActivity) return;

    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }

    setIsActivityActive(true);
    activityOpacity.value = withSpring(1);
  };

  // Handle activity completion
  const handleActivityComplete = async () => {
    if (!selectedActivity) return;

    if (Platform.OS !== 'web') {
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    }

    // Mark activity as completed in stores
    wellnessStore.completeActivity({
      type: selectedActivity.id as any,
      title: selectedActivity.title,
      description: selectedActivity.description,
      duration: parseInt(selectedActivity.duration),
    });

    onboardingStore.markFirstActivityCompleted();
    onboardingStore.markStepCompleted('firstActivityCompleted');

    // Calculate wellness score increase (for demo purposes)
    const increase = Math.floor(Math.random() * 20) + 10; // 10-30% increase
    setWellnessScoreIncrease(increase);

    // Show completion animation
    setActivityCompleted(true);
    completionOpacity.value = withSpring(1);
    celebrationScale.value = withSequence(
      withSpring(1.2),
      withSpring(1),
      withSpring(1.1),
      withSpring(1)
    );
  };

  // Handle continue to registration
  const handleContinue = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }

    onboardingStore.nextStep();
    navigation.navigate('Registration', { fromActivity: true });
  };

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: colors.background,
    },
    content: {
      flex: 1,
      paddingHorizontal: spacing.lg,
    },
    header: {
      paddingTop: spacing.lg,
      paddingBottom: spacing.md,
    },
    titleContainer: {
      marginBottom: spacing.xl,
      paddingTop: spacing.lg,
    },
    title: {
      ...typography.h2,
      color: colors.textPrimary,
      textAlign: 'center',
      marginBottom: spacing.md,
      fontWeight: '700',
    },
    subtitle: {
      ...typography.bodyLarge,
      color: colors.textSecondary,
      textAlign: 'center',
      lineHeight: 26,
    },
    optionsContainer: {
      marginBottom: spacing.xl,
    },
    optionCard: {
      backgroundColor: 'white',
      borderRadius: 16,
      padding: spacing.lg,
      marginBottom: spacing.md,
      borderWidth: 2,
      borderColor: 'transparent',
      ...Platform.select({
        ios: {
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.1,
          shadowRadius: 8,
        },
        android: {
          elevation: 4,
        },
        web: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      }),
    },
    selectedOptionCard: {
      borderColor: colors.primary,
      backgroundColor: colors.primary + '08',
    },
    optionHeader: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: spacing.sm,
    },
    optionIcon: {
      fontSize: 32,
      marginRight: spacing.md,
    },
    optionInfo: {
      flex: 1,
    },
    optionTitle: {
      ...typography.h3,
      color: colors.textPrimary,
      fontWeight: '600',
      marginBottom: spacing.xs,
    },
    optionDescription: {
      ...typography.body,
      color: colors.textSecondary,
    },
    optionDuration: {
      ...typography.bodySmall,
      color: colors.primary,
      fontWeight: '600',
    },
    activityContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingVertical: spacing.xxl,
    },
    completionContainer: {
      alignItems: 'center',
      paddingVertical: spacing.xxl,
    },
    completionIcon: {
      fontSize: 80,
      marginBottom: spacing.lg,
    },
    completionTitle: {
      ...typography.h2,
      color: colors.primary,
      textAlign: 'center',
      marginBottom: spacing.md,
      fontWeight: '700',
    },
    completionMessage: {
      ...typography.bodyLarge,
      color: colors.textSecondary,
      textAlign: 'center',
      marginBottom: spacing.lg,
    },
    scoreIncrease: {
      ...typography.h3,
      color: colors.success,
      textAlign: 'center',
      fontWeight: '700',
      marginBottom: spacing.xl,
    },
    buttonContainer: {
      paddingBottom: spacing.xl,
      paddingTop: spacing.md,
    },
    startButton: {
      marginBottom: spacing.md,
    },
  });

  if (activityCompleted) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="auto" />
        
        <Animated.View style={[styles.completionContainer, completionAnimatedStyle]}>
          <Animated.Text style={[styles.completionIcon, celebrationAnimatedStyle]}>
            ✨
          </Animated.Text>
          <Text style={styles.completionTitle}>
            Amazing! You just improved your wellness
          </Text>
          <Text style={styles.completionMessage}>
            You've experienced immediate value from our platform
          </Text>
          <Text style={styles.scoreIncrease}>
            +{wellnessScoreIncrease}% wellness boost! 📈
          </Text>
          
          <Button
            title="Save My Progress"
            onPress={handleContinue}
            variant="primary"
            size="large"
            icon="arrow-right"
          />
        </Animated.View>
      </SafeAreaView>
    );
  }

  if (isActivityActive && selectedActivity) {
    const ActivityComponent = selectedActivity.component;
    
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="auto" />
        
        <Animated.View style={[styles.activityContainer, activityAnimatedStyle]}>
          <ActivityComponent
            onComplete={handleActivityComplete}
            duration={parseInt(selectedActivity.duration)}
          />
        </Animated.View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      
      {/* Header with progress */}
      <View style={styles.header}>
        <HeaderProgress 
          currentStep={3} 
          totalSteps={onboardingStore.totalSteps}
          onBack={() => navigation.goBack()}
        />
      </View>

      <View style={styles.content}>
        {/* Title Section */}
        <Animated.View style={[styles.titleContainer, titleAnimatedStyle]}>
          <Text style={styles.title}>
            Let's try something together right now! 🎯
          </Text>
          <Text style={styles.subtitle}>
            Experience immediate wellness benefits{'\n'}
            with this personalized activity
          </Text>
        </Animated.View>

        {/* Activity Options */}
        <Animated.View style={[styles.optionsContainer, optionsAnimatedStyle]}>
          {activityOptions.map((option) => (
            <Animated.View
              key={option.id}
              style={[
                styles.optionCard,
                selectedActivity?.id === option.id && styles.selectedOptionCard,
              ]}
            >
              <View style={styles.optionHeader}>
                <Text style={styles.optionIcon}>{option.icon}</Text>
                <View style={styles.optionInfo}>
                  <Text style={styles.optionTitle}>{option.title}</Text>
                  <Text style={styles.optionDescription}>{option.description}</Text>
                </View>
                <Text style={styles.optionDuration}>{option.duration}</Text>
              </View>
            </Animated.View>
          ))}
        </Animated.View>

        {/* Start Button */}
        <View style={styles.buttonContainer}>
          <Button
            title={`Start ${selectedActivity?.title || 'Activity'}`}
            onPress={handleStartActivity}
            style={styles.startButton}
            variant="primary"
            size="large"
            icon="play"
          />
        </View>
      </View>
    </SafeAreaView>
  );
};

export default FirstExperienceScreen;
