import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TextInput,
  Platform,
  Keyboard,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withDelay,
  interpolate,
} from 'react-native-reanimated';

// Import components
import Button from '../../components/common/Button';
import HeaderProgress from '../../components/common/HeaderProgress';
import MoodSlider from '../../components/common/MoodSlider';
import AIInsightCard from '../../components/common/AIInsightCard';

// Import hooks and stores
import { useTheme } from '../../theme/ThemeProvider';
import { useStores } from '../../stores/StoreProvider';
import { useNavigation } from '@react-navigation/native';

// Import types
import type { StackNavigationProp } from '@react-navigation/stack';
import type { OnboardingStackParamList } from '../../navigation/OnboardingNavigator';

type QuickAssessmentNavigationProp = StackNavigationProp<OnboardingStackParamList, 'QuickAssessment'>;

const QuickAssessmentScreen: React.FC = () => {
  const { colors, typography, spacing } = useTheme();
  const { onboardingStore } = useStores();
  const navigation = useNavigation<QuickAssessmentNavigationProp>();

  // State
  const [currentMood, setCurrentMood] = useState<number>(onboardingStore.currentMood);
  const [biggestChallenge, setBiggestChallenge] = useState<string>(onboardingStore.biggestChallenge);
  const [showInsight, setShowInsight] = useState<boolean>(false);
  const [personalizedRecommendation, setPersonalizedRecommendation] = useState<string>('');

  // Refs
  const challengeInputRef = useRef<TextInput>(null);

  // Animation values
  const titleOpacity = useSharedValue(0);
  const moodSliderOpacity = useSharedValue(0);
  const challengeOpacity = useSharedValue(0);
  const insightOpacity = useSharedValue(0);
  const buttonOpacity = useSharedValue(0);

  React.useEffect(() => {
    titleOpacity.value = withDelay(200, withSpring(1));
    moodSliderOpacity.value = withDelay(400, withSpring(1));
    challengeOpacity.value = withDelay(600, withSpring(1));
    buttonOpacity.value = withDelay(800, withSpring(1));
  }, []);

  // Generate personalized recommendation when mood or challenge changes
  React.useEffect(() => {
    if (currentMood !== 5 || biggestChallenge.length > 0) {
      generatePersonalizedRecommendation();
    }
  }, [currentMood, biggestChallenge]);

  // Animated styles
  const titleAnimatedStyle = useAnimatedStyle(() => ({
    opacity: titleOpacity.value,
    transform: [{ translateY: withSpring(titleOpacity.value === 1 ? 0 : 30) }],
  }));

  const moodSliderAnimatedStyle = useAnimatedStyle(() => ({
    opacity: moodSliderOpacity.value,
  }));

  const challengeAnimatedStyle = useAnimatedStyle(() => ({
    opacity: challengeOpacity.value,
  }));

  const insightAnimatedStyle = useAnimatedStyle(() => ({
    opacity: insightOpacity.value,
    transform: [{ scale: withSpring(insightOpacity.value === 1 ? 1 : 0.9) }],
  }));

  const buttonAnimatedStyle = useAnimatedStyle(() => ({
    opacity: buttonOpacity.value,
  }));

  // Handle mood change
  const handleMoodChange = async (mood: number) => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }

    setCurrentMood(mood);
    onboardingStore.setCurrentMood(mood);
  };

  // Handle challenge input change
  const handleChallengeChange = (text: string) => {
    setBiggestChallenge(text);
    onboardingStore.setBiggestChallenge(text);
  };

  // Generate personalized recommendation based on inputs
  const generatePersonalizedRecommendation = () => {
    let recommendation = '';
    
    // Base recommendation on mood level
    if (currentMood <= 3) {
      recommendation = "I notice you're feeling low today. Let's start with a gentle 2-minute breathing exercise to help you feel more grounded.";
    } else if (currentMood >= 8) {
      recommendation = "You're feeling great! Let's channel that positive energy into setting a meaningful wellness goal for today.";
    } else {
      recommendation = "You're in a balanced space today. This is perfect for exploring some mindful reflection or light meditation.";
    }

    // Enhance based on challenge if provided
    if (biggestChallenge.toLowerCase().includes('stress')) {
      recommendation += " Since you mentioned stress, I'll also recommend our stress-reduction techniques.";
    } else if (biggestChallenge.toLowerCase().includes('sleep')) {
      recommendation += " I see sleep is a concern - our evening wind-down routine might be perfect for you.";
    } else if (biggestChallenge.toLowerCase().includes('anxiety')) {
      recommendation += " For anxiety, our guided breathing exercises have helped thousands of users find calm.";
    } else if (biggestChallenge.length > 0) {
      recommendation += ` I understand that "${biggestChallenge}" is challenging for you right now. Let's work on this together.`;
    }

    setPersonalizedRecommendation(recommendation);
    
    // Show insight with animation
    setShowInsight(true);
    insightOpacity.value = withSpring(1);
  };

  // Handle continue
  const handleContinue = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }

    onboardingStore.markStepCompleted('assessmentCompleted');
    onboardingStore.nextStep();
    
    // Navigate to first experience with activity type based on assessment
    const activityType = currentMood <= 4 ? 'breathing' : currentMood >= 7 ? 'reflection' : 'meditation';
    navigation.navigate('FirstExperience', { activityType });
  };

  const getMoodEmoji = (mood: number): string => {
    if (mood <= 2) return '😢';
    if (mood <= 4) return '😔';
    if (mood <= 6) return '😐';
    if (mood <= 8) return '🙂';
    return '😊';
  };

  const getMoodLabel = (mood: number): string => {
    if (mood <= 2) return 'Very Low';
    if (mood <= 4) return 'Low';
    if (mood <= 6) return 'Neutral';
    if (mood <= 8) return 'Good';
    return 'Excellent';
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
    sectionContainer: {
      marginBottom: spacing.xl,
    },
    sectionTitle: {
      ...typography.h3,
      color: colors.textPrimary,
      marginBottom: spacing.md,
      fontWeight: '600',
    },
    moodContainer: {
      backgroundColor: 'white',
      borderRadius: 16,
      padding: spacing.lg,
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
    moodDisplay: {
      alignItems: 'center',
      marginBottom: spacing.lg,
    },
    moodEmoji: {
      fontSize: 48,
      marginBottom: spacing.sm,
    },
    moodLabel: {
      ...typography.bodyLarge,
      color: colors.textPrimary,
      fontWeight: '600',
    },
    challengeContainer: {
      backgroundColor: 'white',
      borderRadius: 16,
      padding: spacing.lg,
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
    challengeInput: {
      ...typography.body,
      color: colors.textPrimary,
      borderWidth: 1,
      borderColor: colors.border,
      borderRadius: 12,
      padding: spacing.md,
      minHeight: 100,
      textAlignVertical: 'top',
    },
    challengePlaceholder: {
      color: colors.textSecondary,
    },
    insightContainer: {
      marginBottom: spacing.xl,
    },
    buttonContainer: {
      paddingBottom: spacing.xl,
      paddingTop: spacing.md,
    },
    continueButton: {
      marginBottom: spacing.md,
    },
  });

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      
      {/* Header with progress */}
      <View style={styles.header}>
        <HeaderProgress 
          currentStep={2} 
          totalSteps={onboardingStore.totalSteps}
          onBack={() => navigation.goBack()}
        />
      </View>

      <ScrollView 
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        {/* Title Section */}
        <Animated.View style={[styles.titleContainer, titleAnimatedStyle]}>
          <Text style={styles.title}>
            Quick Wellness Check-In ✨
          </Text>
          <Text style={styles.subtitle}>
            Help us understand how you're feeling{'\n'}
            so we can personalize your experience
          </Text>
        </Animated.View>

        {/* Mood Assessment */}
        <Animated.View style={[styles.sectionContainer, moodSliderAnimatedStyle]}>
          <Text style={styles.sectionTitle}>How are you feeling right now?</Text>
          <View style={styles.moodContainer}>
            <View style={styles.moodDisplay}>
              <Text style={styles.moodEmoji}>{getMoodEmoji(currentMood)}</Text>
              <Text style={styles.moodLabel}>{getMoodLabel(currentMood)}</Text>
            </View>
            <MoodSlider
              value={currentMood}
              onValueChange={handleMoodChange}
              minimumValue={1}
              maximumValue={10}
            />
          </View>
        </Animated.View>

        {/* Challenge Input */}
        <Animated.View style={[styles.sectionContainer, challengeAnimatedStyle]}>
          <Text style={styles.sectionTitle}>What's your biggest wellness challenge today?</Text>
          <View style={styles.challengeContainer}>
            <TextInput
              ref={challengeInputRef}
              style={styles.challengeInput}
              placeholder="e.g., I've been feeling stressed about work lately..."
              placeholderTextColor={colors.textSecondary}
              value={biggestChallenge}
              onChangeText={handleChallengeChange}
              multiline
              numberOfLines={4}
              maxLength={200}
              returnKeyType="done"
              onSubmitEditing={() => Keyboard.dismiss()}
            />
          </View>
        </Animated.View>

        {/* AI Insight */}
        {showInsight && personalizedRecommendation && (
          <Animated.View style={[styles.insightContainer, insightAnimatedStyle]}>
            <AIInsightCard
              title="✨ Instant personalized recommendation"
              content={personalizedRecommendation}
              type="recommendation"
            />
          </Animated.View>
        )}

        {/* Action Button */}
        <Animated.View style={[styles.buttonContainer, buttonAnimatedStyle]}>
          <Button
            title={showInsight ? "Let's try something together!" : "Get My Recommendation"}
            onPress={showInsight ? handleContinue : generatePersonalizedRecommendation}
            style={styles.continueButton}
            variant="primary"
            size="large"
            icon={showInsight ? "arrow-right" : "sparkles"}
          />
        </Animated.View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default QuickAssessmentScreen;
