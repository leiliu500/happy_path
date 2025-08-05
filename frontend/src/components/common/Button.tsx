import React from 'react';
import {
  Pressable,
  Text,
  StyleSheet,
  ViewStyle,
  TextStyle,
  Platform,
  View,
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

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  icon?: keyof typeof Ionicons.glyphMap;
  iconPosition?: 'left' | 'right';
  style?: ViewStyle;
  textStyle?: TextStyle;
  fullWidth?: boolean;
}

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  icon,
  iconPosition = 'right',
  style,
  textStyle,
  fullWidth = true,
}) => {
  const { colors, typography, spacing, borderRadius } = useTheme();
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

  // Get variant styles
  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          backgroundColor: disabled ? colors.border : colors.primary,
          borderWidth: 0,
        };
      case 'secondary':
        return {
          backgroundColor: disabled ? colors.border : colors.secondary,
          borderWidth: 0,
        };
      case 'outline':
        return {
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderColor: disabled ? colors.border : colors.primary,
        };
      case 'ghost':
        return {
          backgroundColor: 'transparent',
          borderWidth: 0,
        };
      default:
        return {
          backgroundColor: colors.primary,
          borderWidth: 0,
        };
    }
  };

  // Get size styles
  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          paddingVertical: spacing.sm,
          paddingHorizontal: spacing.md,
          minHeight: 36,
        };
      case 'medium':
        return {
          paddingVertical: spacing.md,
          paddingHorizontal: spacing.lg,
          minHeight: 44,
        };
      case 'large':
        return {
          paddingVertical: spacing.lg,
          paddingHorizontal: spacing.xl,
          minHeight: 52,
        };
      default:
        return {
          paddingVertical: spacing.md,
          paddingHorizontal: spacing.lg,
          minHeight: 44,
        };
    }
  };

  // Get text color based on variant
  const getTextColor = () => {
    if (disabled) return colors.textSecondary;
    
    switch (variant) {
      case 'primary':
      case 'secondary':
        return 'white';
      case 'outline':
        return colors.primary;
      case 'ghost':
        return colors.textPrimary;
      default:
        return 'white';
    }
  };

  // Get icon color
  const getIconColor = () => {
    return getTextColor();
  };

  // Get icon size based on button size
  const getIconSize = () => {
    switch (size) {
      case 'small':
        return 16;
      case 'medium':
        return 20;
      case 'large':
        return 24;
      default:
        return 20;
    }
  };

  const styles = StyleSheet.create({
    button: {
      ...getSizeStyles(),
      ...getVariantStyles(),
      borderRadius: borderRadius.lg,
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'row',
      width: fullWidth ? '100%' : 'auto',
      ...Platform.select({
        ios: {
          shadowColor: variant === 'primary' || variant === 'secondary' ? '#000' : 'transparent',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: disabled ? 0 : 0.1,
          shadowRadius: 4,
        },
        android: {
          elevation: disabled ? 0 : variant === 'primary' || variant === 'secondary' ? 2 : 0,
        },
        web: {
          boxShadow: disabled ? 'none' : variant === 'primary' || variant === 'secondary' ? '0 2px 4px rgba(0,0,0,0.1)' : 'none',
          cursor: disabled ? 'not-allowed' : 'pointer',
        },
      }),
    },
    content: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
    },
    text: {
      ...typography.body,
      color: getTextColor(),
      fontWeight: '600',
      textAlign: 'center',
    },
    iconLeft: {
      marginRight: spacing.sm,
    },
    iconRight: {
      marginLeft: spacing.sm,
    },
    loadingContainer: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    loadingText: {
      marginLeft: spacing.sm,
    },
  });

  const renderIcon = () => {
    if (!icon) return null;

    return (
      <Ionicons
        name={icon}
        size={getIconSize()}
        color={getIconColor()}
        style={iconPosition === 'left' ? styles.iconLeft : styles.iconRight}
      />
    );
  };

  const renderContent = () => {
    if (loading) {
      return (
        <View style={styles.loadingContainer}>
          <Ionicons
            name="refresh"
            size={getIconSize()}
            color={getIconColor()}
          />
          <Text style={[styles.text, styles.loadingText, textStyle]}>
            Loading...
          </Text>
        </View>
      );
    }

    return (
      <View style={styles.content}>
        {icon && iconPosition === 'left' && renderIcon()}
        <Text style={[styles.text, textStyle]}>{title}</Text>
        {icon && iconPosition === 'right' && renderIcon()}
      </View>
    );
  };

  return (
    <AnimatedPressable
      style={[styles.button, animatedStyle, style]}
      onPress={disabled || loading ? undefined : onPress}
      onPressIn={disabled || loading ? undefined : handlePressIn}
      onPressOut={disabled || loading ? undefined : handlePressOut}
      disabled={disabled || loading}
    >
      {renderContent()}
    </AnimatedPressable>
  );
};

export default Button;
