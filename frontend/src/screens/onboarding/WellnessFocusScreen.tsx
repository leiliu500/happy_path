import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Pressable,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withDelay,
  useAnimatedRef,
} from 'react-native-reanimated';

// Import components
import Button from '../../components/common/Button';
import HeaderProgress from '../../components/common/HeaderProgress';
import FocusCard from '../../components/onboarding/FocusCard';

// Import hooks and stores
import { useTheme } from '../../theme/ThemeProvider';
import { useStores } from '../../stores/StoreProvider';
import { useNavigation } from '@react-navigation/native';

// Import types
import type { StackNavigationProp } from '@react-navigation/stack';
import type { OnboardingStackParamList } from '../../navigation/OnboardingNavigator';
import { WELLNESS_FOCUS_OPTIONS, WellnessFocus } from '../../stores/onboardingStore';

type WellnessFocusNavigationProp = StackNavigationProp<OnboardingStackParamList, 'WellnessFocus'>;

const WellnessFocusScreen: React.FC = () => {
  const { colors, typography, spacing } = useTheme();
  const { onboardingStore } = useStores();
  const navigation = useNavigation<WellnessFocusNavigationProp>();

  const [selectedFocus, setSelectedFocus] = useState<WellnessFocus | null>(
    onboardingStore.selectedWellnessFocus
  );

  // Animation values
  const titleOpacity = useSharedValue(0);
  const cardsOpacity = useSharedValue(0);
  const buttonOpacity = useSharedValue(0);

  React.useEffect(() => {
    titleOpacity.value = withDelay(200, withSpring(1));
    cardsOpacity.value = withDelay(400, withSpring(1));
    buttonOpacity.value = withDelay(600, withSpring(1));
  }, []);

  // Animated styles
  const titleAnimatedStyle = useAnimatedStyle(() => ({
    opacity: titleOpacity.value,
    transform: [{ translateY: withSpring(titleOpacity.value === 1 ? 0 : 30) }],
  }));

  const cardsAnimatedStyle = useAnimatedStyle(() => ({
    opacity: cardsOpacity.value,
  }));

  const buttonAnimatedStyle = useAnimatedStyle(() => ({
    opacity: buttonOpacity.value,
  }));

  // Handle focus selection
  const handleFocusSelect = async (focus: WellnessFocus) => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }

    setSelectedFocus(focus);
    onboardingStore.setWellnessFocus(focus);
  };

  // Handle continue
  const handleContinue = async () => {
    if (!selectedFocus) return;

    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }

    onboardingStore.nextStep();
    navigation.navigate('QuickAssessment');
  };

  // Handle skip
  const handleSkip = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }

    // Set a default focus if skipping
    onboardingStore.setWellnessFocus(WELLNESS_FOCUS_OPTIONS[3]); // General Wellness
    onboardingStore.nextStep();
    navigation.navigate('QuickAssessment');
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
    focusGrid: {
      marginBottom: spacing.xl,
    },
    row: {
      flexDirection: 'row',
      marginBottom: spacing.md,
    },
    focusCard: {
      flex: 1,
      marginHorizontal: spacing.xs,
    },
    buttonContainer: {
      paddingBottom: spacing.xl,
      paddingTop: spacing.md,
    },
    continueButton: {
      marginBottom: spacing.md,
    },
    skipButton: {
      backgroundColor: 'transparent',
      borderWidth: 0,
    },
    skipButtonText: {
      color: colors.textSecondary,
      ...typography.body,
    },
    selectedIndicator: {
      position: 'absolute',
      top: spacing.sm,
      right: spacing.sm,
      width: 24,
      height: 24,
      borderRadius: 12,
      backgroundColor: colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
    },
    checkmark: {
      color: 'white',
      fontSize: 14,
      fontWeight: 'bold',
    },
  });

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      
      {/* Header with progress */}
      <View style={styles.header}>
        <HeaderProgress 
          currentStep={1} 
          totalSteps={onboardingStore.totalSteps}
          onBack={() => navigation.goBack()}
        />
      </View>

      <ScrollView 
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        bounces={false}
      >
        {/* Title Section */}
        <Animated.View style={[styles.titleContainer, titleAnimatedStyle]}>
          <Text style={styles.title}>
            Choose Your Primary{'\n'}Wellness Focus 🌱
          </Text>
          <Text style={styles.subtitle}>
            Help us personalize your experience by selecting{'\n'}
            what you'd like to focus on most
          </Text>
        </Animated.View>

        {/* Focus Options Grid */}
        <Animated.View style={[styles.focusGrid, cardsAnimatedStyle]}>
          {/* Row 1 */}
          <View style={styles.row}>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[0])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[0]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[0].id}
              />
            </Pressable>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[1])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[1]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[1].id}
              />
            </Pressable>
          </View>

          {/* Row 2 */}
          <View style={styles.row}>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[2])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[2]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[2].id}
              />
            </Pressable>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[3])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[3]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[3].id}
              />
            </Pressable>
          </View>

          {/* Row 3 */}
          <View style={styles.row}>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[4])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[4]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[4].id}
              />
            </Pressable>
            <Pressable
              style={[styles.focusCard]}
              onPress={() => handleFocusSelect(WELLNESS_FOCUS_OPTIONS[5])}
            >
              <FocusCard
                focus={WELLNESS_FOCUS_OPTIONS[5]}
                isSelected={selectedFocus?.id === WELLNESS_FOCUS_OPTIONS[5].id}
              />
            </Pressable>
          </View>
        </Animated.View>

        {/* Action Buttons */}
        <Animated.View style={[styles.buttonContainer, buttonAnimatedStyle]}>
          <Button
            title="Continue"
            onPress={handleContinue}
            style={styles.continueButton}
            variant="primary"
            size="large"
            disabled={!selectedFocus}
            icon="arrow-right"
          />
          
          <Button
            title="Skip for now"
            onPress={handleSkip}
            style={styles.skipButton}
            textStyle={styles.skipButtonText}
            variant="ghost"
            size="medium"
          />
        </Animated.View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default WellnessFocusScreen;
