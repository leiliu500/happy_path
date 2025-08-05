import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Pressable,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

// Import theme
import { useTheme } from '../../theme/ThemeProvider';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface WellnessCardProps {
  title: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
  gradient: string[];
  onPress: () => void;
  selected?: boolean;
  disabled?: boolean;
  style?: any;
}

const WellnessCard: React.FC<WellnessCardProps> = ({
  title,
  description,
  icon,
  gradient,
  onPress,
  selected = false,
  disabled = false,
  style,
}) => {
  const { colors, typography, spacing, borderRadius } = useTheme();
  const scaleValue = React.useRef(new Animated.Value(1)).current;
  const opacityValue = React.useRef(new Animated.Value(1)).current;

  const handlePressIn = () => {
    if (disabled) return;
    
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    Animated.parallel([
      Animated.spring(scaleValue, {
        toValue: 0.95,
        useNativeDriver: true,
        tension: 300,
        friction: 10,
      }),
      Animated.timing(opacityValue, {
        toValue: 0.8,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const handlePressOut = () => {
    if (disabled) return;
    
    Animated.parallel([
      Animated.spring(scaleValue, {
        toValue: 1,
        useNativeDriver: true,
        tension: 300,
        friction: 10,
      }),
      Animated.timing(opacityValue, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const styles = StyleSheet.create({
    container: {
      width: (screenWidth - 48) / 2,
      minHeight: 140,
      margin: 6,
    },
    card: {
      flex: 1,
      borderRadius: borderRadius.lg,
      padding: spacing.lg,
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.1,
      shadowRadius: 12,
      elevation: 6,
      borderWidth: selected ? 3 : 1,
      borderColor: selected ? colors.primary : colors.border,
    },
    selectedOverlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      borderRadius: borderRadius.lg,
      backgroundColor: `${colors.primary}15`,
    },
    iconContainer: {
      width: 56,
      height: 56,
      borderRadius: 28,
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: spacing.md,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    },
    title: {
      ...typography.h6,
      color: colors.textPrimary,
      textAlign: 'center',
      marginBottom: spacing.xs,
      fontWeight: '600',
    },
    description: {
      ...typography.caption,
      color: colors.textSecondary,
      textAlign: 'center',
      lineHeight: 16,
    },
    checkmark: {
      position: 'absolute',
      top: 8,
      right: 8,
      width: 24,
      height: 24,
      borderRadius: 12,
      backgroundColor: colors.success,
      alignItems: 'center',
      justifyContent: 'center',
    },
    disabledOverlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      borderRadius: borderRadius.lg,
      backgroundColor: 'rgba(255, 255, 255, 0.7)',
    },
  });

  return (
    <Animated.View
      style={[
        styles.container,
        {
          transform: [{ scale: scaleValue }],
          opacity: opacityValue,
        },
        style,
      ]}
    >
      <Pressable
        style={styles.card}
        onPress={disabled ? undefined : onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={disabled}
      >
        <LinearGradient
          colors={gradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={StyleSheet.absoluteFillObject}
        />
        
        {selected && <View style={styles.selectedOverlay} />}
        
        <View style={styles.iconContainer}>
          <Ionicons 
            name={icon} 
            size={28} 
            color={colors.primary} 
          />
        </View>
        
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.description}>{description}</Text>
        
        {selected && (
          <View style={styles.checkmark}>
            <Ionicons 
              name="checkmark" 
              size={16} 
              color="white" 
            />
          </View>
        )}
        
        {disabled && <View style={styles.disabledOverlay} />}
      </Pressable>
    </Animated.View>
  );
};

export default WellnessCard;
