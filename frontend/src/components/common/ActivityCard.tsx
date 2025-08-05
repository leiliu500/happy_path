import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Dimensions,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';

// Import theme
import { useTheme } from '../../theme/ThemeProvider';

const { width: screenWidth } = Dimensions.get('window');

interface ActivityCardProps {
  title: string;
  description: string;
  duration: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  onPress: () => void;
  completed?: boolean;
  progress?: number;
  difficulty?: 'easy' | 'medium' | 'hard';
  style?: any;
}

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

const ActivityCard: React.FC<ActivityCardProps> = ({
  title,
  description,
  duration,
  icon,
  color,
  onPress,
  completed = false,
  progress = 0,
  difficulty = 'easy',
  style,
}) => {
  const { colors, typography, spacing, borderRadius } = useTheme();
  
  // Animation values
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  // Animation handlers
  const handlePressIn = () => {
    scale.value = withSpring(0.95);
    opacity.value = withTiming(0.8);
  };

  const handlePressOut = () => {
    scale.value = withSpring(1);
    opacity.value = withTiming(1);
  };

  // Animated styles
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  // Get difficulty color
  const getDifficultyColor = () => {
    switch (difficulty) {
      case 'easy':
        return colors.success;
      case 'medium':
        return colors.warning;
      case 'hard':
        return colors.danger;
      default:
        return colors.success;
    }
  };

  // Get difficulty label
  const getDifficultyLabel = () => {
    switch (difficulty) {
      case 'easy':
        return 'Beginner';
      case 'medium':
        return 'Intermediate';
      case 'hard':
        return 'Advanced';
      default:
        return 'Beginner';
    }
  };

  const styles = StyleSheet.create({
    card: {
      backgroundColor: colors.background,
      borderRadius: borderRadius.lg,
      padding: spacing.lg,
      marginBottom: spacing.md,
      borderWidth: 1,
      borderColor: colors.border,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 8,
      elevation: 3,
      width: screenWidth - (spacing.lg * 2),
    },
    completedCard: {
      borderColor: colors.success,
      backgroundColor: `${colors.success}08`,
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: spacing.md,
    },
    iconContainer: {
      width: 48,
      height: 48,
      borderRadius: 24,
      backgroundColor: `${color}20`,
      alignItems: 'center',
      justifyContent: 'center',
      marginRight: spacing.md,
    },
    completedIconContainer: {
      backgroundColor: `${colors.success}20`,
    },
    titleSection: {
      flex: 1,
    },
    title: {
      ...typography.h3,
      color: colors.textPrimary,
      marginBottom: spacing.xs,
    },
    duration: {
      ...typography.caption,
      color: colors.textSecondary,
    },
    description: {
      ...typography.body,
      color: colors.textSecondary,
      marginBottom: spacing.md,
      lineHeight: 20,
    },
    footer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    difficultyBadge: {
      paddingHorizontal: spacing.sm,
      paddingVertical: spacing.xs,
      borderRadius: borderRadius.sm,
      backgroundColor: colors.border,
    },
    difficultyText: {
      ...typography.caption,
      color: colors.textSecondary,
      fontWeight: '500',
    },
    statusSection: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    completedText: {
      ...typography.caption,
      color: colors.success,
      fontWeight: '600',
      marginLeft: spacing.xs,
    },
    progressSection: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    progressText: {
      ...typography.caption,
      color: colors.textSecondary,
      marginLeft: spacing.xs,
    },
    progressBar: {
      width: 60,
      height: 4,
      backgroundColor: colors.border,
      borderRadius: 2,
      marginTop: spacing.xs,
      overflow: 'hidden',
    },
    progressFill: {
      height: '100%',
      backgroundColor: color,
      borderRadius: 2,
    },
    chevron: {
      marginLeft: spacing.sm,
    },
  });

  const renderStatus = () => {
    if (completed) {
      return (
        <View style={styles.statusSection}>
          <Ionicons 
            name="checkmark-circle" 
            size={16} 
            color={colors.success} 
          />
          <Text style={styles.completedText}>Completed</Text>
        </View>
      );
    }

    if (progress > 0) {
      return (
        <View>
          <View style={styles.progressSection}>
            <Ionicons 
              name="play-circle-outline" 
              size={16} 
              color={colors.textSecondary} 
            />
            <Text style={styles.progressText}>
              {Math.round(progress * 100)}% complete
            </Text>
          </View>
          <View style={styles.progressBar}>
            <View 
              style={[
                styles.progressFill,
                { width: `${progress * 100}%` }
              ]} 
            />
          </View>
        </View>
      );
    }

    return (
      <View style={styles.statusSection}>
        <Ionicons 
          name="play-circle-outline" 
          size={16} 
          color={colors.textSecondary} 
        />
        <Text style={styles.progressText}>Start</Text>
      </View>
    );
  };

  return (
    <AnimatedPressable
      style={[
        styles.card,
        completed && styles.completedCard,
        animatedStyle,
        style,
      ]}
      onPress={onPress}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
    >
      <View style={styles.header}>
        <View style={[
          styles.iconContainer,
          completed && styles.completedIconContainer,
        ]}>
          <Ionicons 
            name={completed ? "checkmark-circle" : icon} 
            size={24} 
            color={completed ? colors.success : color} 
          />
        </View>
        
        <View style={styles.titleSection}>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.duration}>{duration}</Text>
        </View>

        <Ionicons 
          name="chevron-forward" 
          size={20} 
          color={colors.textSecondary}
          style={styles.chevron}
        />
      </View>

      <Text style={styles.description}>{description}</Text>

      <View style={styles.footer}>
        <View 
          style={[
            styles.difficultyBadge,
            { backgroundColor: `${getDifficultyColor()}20` }
          ]}
        >
          <Text 
            style={[
              styles.difficultyText,
              { color: getDifficultyColor() }
            ]}
          >
            {getDifficultyLabel()}
          </Text>
        </View>

        {renderStatus()}
      </View>
    </AnimatedPressable>
  );
};

export default ActivityCard;
