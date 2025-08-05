import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Pressable,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  withDelay,
  withSequence,
  runOnJS,
} from 'react-native-reanimated';

// Import components and stores
import Container from '../../components/common/Container';
import Button from '../../components/common/Button';
import { useTheme } from '../../theme/ThemeProvider';
import { useOnboardingStore } from '../../store/onboardingStore';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface EnhancedWelcomeScreenProps {
  navigation: any;
}

const EnhancedWelcomeScreen: React.FC<EnhancedWelcomeScreenProps> = ({ navigation }) => {
  const { colors, typography, spacing, borderRadius } = useTheme();
  const { setCurrentStep } = useOnboardingStore();

  // Animation values
  const fadeAnim = useSharedValue(0);
  const slideAnim = useSharedValue(50);
  const scaleAnim = useSharedValue(0.8);
  const iconRotation = useSharedValue(0);

  useEffect(() => {
    // Entrance animations
    const startAnimations = () => {
      fadeAnim.value = withTiming(1, { duration: 800 });
      slideAnim.value = withSpring(0, { damping: 10 });
      scaleAnim.value = withSpring(1, { damping: 10 });
      
      // Continuous icon rotation for healing energy
      iconRotation.value = withSequence(
        withTiming(360, { duration: 8000 }),
        withTiming(0, { duration: 0 })
      );
    };

    startAnimations();
    setCurrentStep(1);
  }, []);

  const handleContinue = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    navigation.navigate('WellnessFocus');
  };

  const handleSkip = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    navigation.navigate('WellnessFocus');
  };

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: fadeAnim.value,
    transform: [
      { translateY: slideAnim.value },
      { scale: scaleAnim.value },
    ],
  }));

  const iconAnimatedStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${iconRotation.value}deg` }],
  }));

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: colors.background,
    },
    gradientBackground: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
    },
    content: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingHorizontal: spacing.xl,
    },
    heroSection: {
      alignItems: 'center',
      marginBottom: spacing.xl * 2,
    },
    iconContainer: {
      width: 120,
      height: 120,
      borderRadius: 60,
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: spacing.xl,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 0.15,
      shadowRadius: 16,
      elevation: 8,
      borderWidth: 3,
      borderColor: `${colors.primary}20`,
    },
    floatingElements: {
      position: 'absolute',
      width: '100%',
      height: '100%',
    },
    floatingIcon: {
      position: 'absolute',
      opacity: 0.6,
    },
    title: {
      ...typography.h1,
      color: colors.textPrimary,
      textAlign: 'center',
      marginBottom: spacing.md,
      fontWeight: '700',
      letterSpacing: -0.5,
    },
    subtitle: {
      ...typography.h6,
      color: colors.primary,
      textAlign: 'center',
      marginBottom: spacing.lg,
      fontWeight: '500',
    },
    description: {
      ...typography.bodyLarge,
      color: colors.textSecondary,
      textAlign: 'center',
      lineHeight: 28,
      marginBottom: spacing.xl,
      maxWidth: screenWidth - (spacing.xl * 2),
    },
    featuresContainer: {
      width: '100%',
      marginBottom: spacing.xl * 2,
    },
    feature: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: spacing.lg,
      paddingHorizontal: spacing.md,
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      borderRadius: borderRadius.lg,
      paddingVertical: spacing.md,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.05,
      shadowRadius: 8,
      elevation: 2,
    },
    featureIcon: {
      width: 44,
      height: 44,
      borderRadius: 22,
      backgroundColor: `${colors.primary}15`,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: spacing.md,
    },
    featureText: {
      ...typography.body,
      color: colors.textPrimary,
      flex: 1,
      fontWeight: '500',
      lineHeight: 22,
    },
    buttonContainer: {
      width: '100%',
      gap: spacing.md,
      paddingHorizontal: spacing.lg,
    },
    skipButton: {
      alignSelf: 'center',
      marginTop: spacing.md,
      paddingVertical: spacing.sm,
      paddingHorizontal: spacing.md,
    },
    skipText: {
      ...typography.body,
      color: colors.textSecondary,
      textDecorationLine: 'underline',
    },
    decorativeElement: {
      position: 'absolute',
      width: 200,
      height: 200,
      borderRadius: 100,
      opacity: 0.1,
    },
  });

  const features = [
    {
      icon: 'heart-outline',
      text: 'Personalized wellness journey tailored to your unique needs',
    },
    {
      icon: 'people-outline',
      text: 'Connect with a supportive community on similar healing paths',
    },
    {
      icon: 'shield-checkmark-outline',
      text: 'Safe, private sanctuary for your mental health journey',
    },
    {
      icon: 'trending-up-outline',
      text: 'Track progress and celebrate meaningful growth milestones',
    },
  ];

  return (
    <Container safeArea={true} padding="none">
      <LinearGradient
        colors={[
          '#FFFFFF',
          '#F8FAFC',
          '#E2E8F0',
          '#F1F5F9',
        ]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.gradientBackground}
      />

      {/* Decorative background elements */}
      <View style={styles.decorativeElement}>
        <LinearGradient
          colors={[colors.primary, colors.secondary]}
          style={[styles.decorativeElement, { top: '10%', left: '-20%' }]}
        />
        <LinearGradient
          colors={[colors.peace, colors.calm]}
          style={[styles.decorativeElement, { bottom: '15%', right: '-25%' }]}
        />
      </View>

      {/* Floating background elements */}
      <View style={styles.floatingElements}>
        <Animated.View 
          style={[
            styles.floatingIcon,
            { 
              top: '15%', 
              left: '10%',
            },
            iconAnimatedStyle,
          ]}
        >
          <Ionicons name="leaf-outline" size={24} color={colors.growth} />
        </Animated.View>
        
        <Animated.View 
          style={[
            styles.floatingIcon,
            { 
              top: '25%', 
              right: '15%',
            },
            iconAnimatedStyle,
          ]}
        >
          <Ionicons name="heart-outline" size={20} color={colors.peace} />
        </Animated.View>
        
        <Animated.View 
          style={[
            styles.floatingIcon,
            { 
              bottom: '30%', 
              left: '15%',
            },
            iconAnimatedStyle,
          ]}
        >
          <Ionicons name="star-outline" size={18} color={colors.calm} />
        </Animated.View>
      </View>

      <View style={styles.content}>
        <Animated.View style={[styles.heroSection, animatedStyle]}>
          <View style={styles.iconContainer}>
            <LinearGradient
              colors={[colors.primary, colors.secondary]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={[StyleSheet.absoluteFillObject, { borderRadius: 60 }]}
            />
            <Animated.View style={iconAnimatedStyle}>
              <Ionicons 
                name="flower-outline" 
                size={60} 
                color="white" 
              />
            </Animated.View>
          </View>

          <Text style={styles.title}>Welcome to Your{'\n'}Wellness Journey</Text>
          <Text style={styles.subtitle}>A sanctuary for growth and healing</Text>
          <Text style={styles.description}>
            Discover personalized tools, connect with a caring community, and take meaningful steps toward better mental health and wellbeing.
          </Text>
        </Animated.View>

        <Animated.View style={[styles.featuresContainer, animatedStyle]}>
          {features.map((feature, index) => (
            <View key={index} style={styles.feature}>
              <View style={styles.featureIcon}>
                <Ionicons 
                  name={feature.icon as any} 
                  size={22} 
                  color={colors.primary} 
                />
              </View>
              <Text style={styles.featureText}>{feature.text}</Text>
            </View>
          ))}
        </Animated.View>

        <Animated.View style={[styles.buttonContainer, animatedStyle]}>
          <Button
            title="Begin Your Healing Journey"
            onPress={handleContinue}
            variant="primary"
            icon="arrow-forward"
            iconPosition="right"
          />
          
          <Pressable style={styles.skipButton} onPress={handleSkip}>
            <Text style={styles.skipText}>Skip introduction</Text>
          </Pressable>
        </Animated.View>
      </View>
    </Container>
  );
};

export default EnhancedWelcomeScreen;
