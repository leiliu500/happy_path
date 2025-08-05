import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Platform,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withDelay,
  withSequence,
  runOnJS,
} from 'react-native-reanimated';

// Import components
import Button from '../../components/common/Button';
import GradientBackground from '../../components/common/GradientBackground';
import WellnessIcon from '../../components/common/WellnessIcon';

// Import hooks
import { useTheme } from '../../theme/ThemeProvider';
import { useStores } from '../../stores/StoreProvider';
import { useNavigation } from '@react-navigation/native';

// Import types
import type { StackNavigationProp } from '@react-navigation/stack';
import type { OnboardingStackParamList } from '../../navigation/OnboardingNavigator';

type WelcomeScreenNavigationProp = StackNavigationProp<OnboardingStackParamList, 'Welcome'>;

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

const WelcomeScreen: React.FC = () => {
  const { colors, typography, spacing } = useTheme();
  const { onboardingStore } = useStores();
  const navigation = useNavigation<WelcomeScreenNavigationProp>();

  // Animation values
  const logoScale = useSharedValue(0);
  const titleOpacity = useSharedValue(0);
  const subtitleOpacity = useSharedValue(0);
  const buttonOpacity = useSharedValue(0);
  const iconTranslateY = useSharedValue(50);

  // Initialize animations
  useEffect(() => {
    const startAnimations = () => {
      logoScale.value = withSpring(1, { damping: 15, stiffness: 100 });
      titleOpacity.value = withDelay(300, withSpring(1));
      subtitleOpacity.value = withDelay(600, withSpring(1));
      iconTranslateY.value = withDelay(400, withSpring(0));
      buttonOpacity.value = withDelay(900, withSpring(1));
    };

    startAnimations();
  }, []);

  // Animated styles
  const logoAnimatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: logoScale.value }],
  }));

  const titleAnimatedStyle = useAnimatedStyle(() => ({
    opacity: titleOpacity.value,
  }));

  const subtitleAnimatedStyle = useAnimatedStyle(() => ({
    opacity: subtitleOpacity.value,
  }));

  const buttonAnimatedStyle = useAnimatedStyle(() => ({
    opacity: buttonOpacity.value,
  }));

  const iconAnimatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: iconTranslateY.value }],
  }));

  // Handle continue button press
  const handleContinue = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
    
    onboardingStore.markStepCompleted('welcomeCompleted');
    onboardingStore.nextStep();
    navigation.navigate('WellnessFocus');
  };

  // Handle explore first button press
  const handleExploreFirst = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    
    // Skip directly to quick assessment for immediate value
    onboardingStore.setCurrentStep(2);
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
      justifyContent: 'center',
      alignItems: 'center',
    },
    logoContainer: {
      marginBottom: spacing.xxl,
      alignItems: 'center',
    },
    logo: {
      width: 120,
      height: 120,
      borderRadius: 60,
      backgroundColor: colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: spacing.lg,
    },
    logoText: {
      ...typography.h3,
      color: 'white',
      fontWeight: '700',
    },
    titleContainer: {
      alignItems: 'center',
      marginBottom: spacing.xl,
    },
    title: {
      ...typography.h1,
      color: colors.textPrimary,
      textAlign: 'center',
      marginBottom: spacing.md,
      fontWeight: '700',
    },
    subtitle: {
      ...typography.bodyLarge,
      color: colors.textSecondary,
      textAlign: 'center',
      lineHeight: 28,
      marginBottom: spacing.lg,
    },
    highlight: {
      color: colors.primary,
      fontWeight: '600',
    },
    iconGrid: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'center',
      marginBottom: spacing.xxl,
      paddingHorizontal: spacing.lg,
    },
    iconItem: {
      margin: spacing.sm,
      alignItems: 'center',
    },
    buttonContainer: {
      width: '100%',
      paddingHorizontal: spacing.lg,
      paddingBottom: spacing.xl,
    },
    primaryButton: {
      marginBottom: spacing.md,
    },
    secondaryButton: {
      backgroundColor: 'transparent',
      borderWidth: 2,
      borderColor: colors.border,
    },
    secondaryButtonText: {
      color: colors.textSecondary,
    },
    disclaimer: {
      ...typography.caption,
      color: colors.textSecondary,
      textAlign: 'center',
      marginTop: spacing.lg,
      paddingHorizontal: spacing.md,
    },
  });

  const wellnessIcons = [
    { icon: '🧘', label: 'Mindfulness', color: colors.calm },
    { icon: '📝', label: 'Journaling', color: colors.growth },
    { icon: '😊', label: 'Mood Tracking', color: colors.focus },
    { icon: '🤝', label: 'Community', color: colors.energy },
    { icon: '🎯', label: 'Goals', color: colors.primary },
    { icon: '📊', label: 'Insights', color: colors.secondary },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      <GradientBackground />
      
      <ScrollView 
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        bounces={false}
      >
        {/* Logo Section */}
        <Animated.View style={[styles.logoContainer, logoAnimatedStyle]}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>🌱</Text>
          </View>
        </Animated.View>

        {/* Title Section */}
        <Animated.View style={[styles.titleContainer, titleAnimatedStyle]}>
          <Text style={styles.title}>
            Welcome to Your{'\n'}
            <Text style={styles.highlight}>Wellness Journey</Text>
          </Text>
        </Animated.View>

        <Animated.View style={[subtitleAnimatedStyle]}>
          <Text style={styles.subtitle}>
            Take control of your mental wellness through{'\n'}
            <Text style={styles.highlight}>evidence-based practices</Text>{'\n'}
            and supportive community connections
          </Text>
        </Animated.View>

        {/* Wellness Icons Grid */}
        <Animated.View style={[styles.iconGrid, iconAnimatedStyle]}>
          {wellnessIcons.map((item, index) => (
            <Animated.View
              key={index}
              style={[
                styles.iconItem,
                {
                  transform: [
                    {
                      translateY: withDelay(
                        500 + index * 100,
                        withSpring(0, { damping: 15 })
                      ),
                    },
                  ],
                },
              ]}
            >
              <WellnessIcon
                icon={item.icon}
                label={item.label}
                backgroundColor={item.color}
                size={48}
              />
            </Animated.View>
          ))}
        </Animated.View>

        {/* Action Buttons */}
        <Animated.View style={[styles.buttonContainer, buttonAnimatedStyle]}>
          <Button
            title="Start Your Journey"
            onPress={handleContinue}
            style={styles.primaryButton}
            variant="primary"
            size="large"
            icon="arrow-right"
          />
          
          <Button
            title="Skip - I'll explore first"
            onPress={handleExploreFirst}
            style={styles.secondaryButton}
            textStyle={styles.secondaryButtonText}
            variant="outline"
            size="large"
          />
          
          <Text style={styles.disclaimer}>
            🔒 This platform provides wellness support and is{'\n'}
            NOT a substitute for professional mental health care
          </Text>
        </Animated.View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default WelcomeScreen;
