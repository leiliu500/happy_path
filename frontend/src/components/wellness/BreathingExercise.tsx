import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  Easing,
} from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';

// Import theme and components
import { useTheme } from '../../theme/ThemeProvider';
import Button from '../common/Button';

const { width: screenWidth } = Dimensions.get('window');

interface BreathingExerciseProps {
  onComplete: () => void;
  duration?: number; // in minutes
}

type BreathingPhase = 'inhale' | 'hold' | 'exhale' | 'rest';

const BreathingExercise: React.FC<BreathingExerciseProps> = ({
  onComplete,
  duration = 3,
}) => {
  const { colors, typography, spacing } = useTheme();
  
  // State
  const [isActive, setIsActive] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<BreathingPhase>('inhale');
  const [cycleCount, setCycleCount] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(duration * 60);
  
  // Animation values
  const circleScale = useSharedValue(1);
  const circleOpacity = useSharedValue(0.3);
  
  // Breathing pattern (4-4-4-4 technique)
  const breathingPattern = {
    inhale: 4,
    hold: 4,
    exhale: 4,
    rest: 4,
  };

  // Start breathing animation
  const startBreathingAnimation = () => {
    const totalCycleTime = Object.values(breathingPattern).reduce((a, b) => a + b, 0) * 1000;
    
    circleScale.value = withRepeat(
      withSequence(
        withTiming(1.3, { duration: breathingPattern.inhale * 1000, easing: Easing.inOut(Easing.ease) }),
        withTiming(1.3, { duration: breathingPattern.hold * 1000 }),
        withTiming(1, { duration: breathingPattern.exhale * 1000, easing: Easing.inOut(Easing.ease) }),
        withTiming(1, { duration: breathingPattern.rest * 1000 })
      ),
      Math.ceil((duration * 60 * 1000) / totalCycleTime),
      false
    );

    circleOpacity.value = withRepeat(
      withSequence(
        withTiming(0.8, { duration: breathingPattern.inhale * 1000 }),
        withTiming(0.8, { duration: breathingPattern.hold * 1000 }),
        withTiming(0.3, { duration: breathingPattern.exhale * 1000 }),
        withTiming(0.3, { duration: breathingPattern.rest * 1000 })
      ),
      Math.ceil((duration * 60 * 1000) / totalCycleTime),
      false
    );
  };

  // Stop breathing animation
  const stopBreathingAnimation = () => {
    circleScale.value = withTiming(1);
    circleOpacity.value = withTiming(0.3);
  };

  // Breathing cycle management
  useEffect(() => {
    if (!isActive) return;

    const phaseOrder: BreathingPhase[] = ['inhale', 'hold', 'exhale', 'rest'];
    let phaseIndex = 0;
    let phaseTimer: NodeJS.Timeout;

    const nextPhase = () => {
      setCurrentPhase(phaseOrder[phaseIndex]);
      
      phaseTimer = setTimeout(() => {
        phaseIndex = (phaseIndex + 1) % phaseOrder.length;
        if (phaseIndex === 0) {
          setCycleCount(prev => prev + 1);
        }
        nextPhase();
      }, breathingPattern[phaseOrder[phaseIndex]] * 1000);
    };

    nextPhase();

    return () => {
      if (phaseTimer) clearTimeout(phaseTimer);
    };
  }, [isActive]);

  // Timer management
  useEffect(() => {
    if (!isActive || timeRemaining <= 0) return;

    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          setIsActive(false);
          onComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isActive, timeRemaining, onComplete]);

  // Start/stop exercise
  const toggleExercise = () => {
    if (isActive) {
      setIsActive(false);
      stopBreathingAnimation();
    } else {
      setIsActive(true);
      startBreathingAnimation();
    }
  };

  // Reset exercise
  const resetExercise = () => {
    setIsActive(false);
    setCurrentPhase('inhale');
    setCycleCount(0);
    setTimeRemaining(duration * 60);
    stopBreathingAnimation();
  };

  // Animated styles
  const circleStyle = useAnimatedStyle(() => ({
    transform: [{ scale: circleScale.value }],
    opacity: circleOpacity.value,
  }));

  // Get phase instruction
  const getPhaseInstruction = () => {
    switch (currentPhase) {
      case 'inhale':
        return 'Breathe In';
      case 'hold':
        return 'Hold';
      case 'exhale':
        return 'Breathe Out';
      case 'rest':
        return 'Rest';
      default:
        return 'Breathe';
    }
  };

  // Get phase color
  const getPhaseColor = () => {
    switch (currentPhase) {
      case 'inhale':
        return colors.primary;
      case 'hold':
        return colors.warning;
      case 'exhale':
        return colors.secondary;
      case 'rest':
        return colors.success;
      default:
        return colors.primary;
    }
  };

  // Format time
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: colors.background,
      padding: spacing.lg,
    },
    header: {
      alignItems: 'center',
      marginBottom: spacing.xl,
    },
    title: {
      ...typography.h2,
      color: colors.textPrimary,
      marginBottom: spacing.sm,
    },
    subtitle: {
      ...typography.body,
      color: colors.textSecondary,
      textAlign: 'center',
    },
    circleContainer: {
      alignItems: 'center',
      justifyContent: 'center',
      marginVertical: spacing.xl * 2,
    },
    circle: {
      width: 200,
      height: 200,
      borderRadius: 100,
      backgroundColor: colors.primary,
      alignItems: 'center',
      justifyContent: 'center',
    },
    innerCircle: {
      alignItems: 'center',
      justifyContent: 'center',
    },
    phaseIcon: {
      marginBottom: spacing.sm,
    },
    phaseText: {
      ...typography.h3,
      color: 'white',
      fontWeight: '600',
    },
    stats: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      width: '100%',
      marginBottom: spacing.xl,
      paddingHorizontal: spacing.lg,
    },
    stat: {
      alignItems: 'center',
    },
    statValue: {
      ...typography.h3,
      color: colors.textPrimary,
      marginBottom: spacing.xs,
    },
    statLabel: {
      ...typography.caption,
      color: colors.textSecondary,
    },
    controls: {
      width: '100%',
      gap: spacing.md,
    },
    controlRow: {
      flexDirection: 'row',
      gap: spacing.md,
    },
  });

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Breathing Exercise</Text>
        <Text style={styles.subtitle}>
          Follow the circle and breathe deeply
        </Text>
      </View>

      <View style={styles.circleContainer}>
        <Animated.View 
          style={[
            styles.circle,
            { backgroundColor: getPhaseColor() },
            circleStyle,
          ]}
        >
          <View style={styles.innerCircle}>
            <Ionicons 
              name="leaf-outline" 
              size={32} 
              color="white"
              style={styles.phaseIcon}
            />
            <Text style={styles.phaseText}>
              {getPhaseInstruction()}
            </Text>
          </View>
        </Animated.View>
      </View>

      <View style={styles.stats}>
        <View style={styles.stat}>
          <Text style={styles.statValue}>{formatTime(timeRemaining)}</Text>
          <Text style={styles.statLabel}>Time Left</Text>
        </View>
        
        <View style={styles.stat}>
          <Text style={styles.statValue}>{cycleCount}</Text>
          <Text style={styles.statLabel}>Cycles</Text>
        </View>
        
        <View style={styles.stat}>
          <Text style={styles.statValue}>4-4-4-4</Text>
          <Text style={styles.statLabel}>Pattern</Text>
        </View>
      </View>

      <View style={styles.controls}>
        <Button
          title={isActive ? 'Pause' : 'Start'}
          onPress={toggleExercise}
          icon={isActive ? 'pause' : 'play'}
          variant="primary"
        />
        
        <View style={styles.controlRow}>
          <Button
            title="Reset"
            onPress={resetExercise}
            icon="refresh"
            variant="outline"
            style={{ flex: 1 }}
          />
          
          <Button
            title="Complete"
            onPress={onComplete}
            icon="checkmark"
            variant="secondary"
            style={{ flex: 1 }}
          />
        </View>
      </View>
    </View>
  );
};

export default BreathingExercise;
