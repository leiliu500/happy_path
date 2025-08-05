import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  PanGestureHandler,
  State,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  useAnimatedGestureHandler,
  runOnJS,
  interpolate,
  interpolateColor,
  withSpring,
} from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';

// Import theme
import { useTheme } from '../../theme/ThemeProvider';

interface MoodSliderProps {
  value: number;
  onValueChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
  showLabels?: boolean;
  showEmojis?: boolean;
  width?: number;
}

const MoodSlider: React.FC<MoodSliderProps> = ({
  value,
  onValueChange,
  min = 1,
  max = 10,
  step = 1,
  showLabels = true,
  showEmojis = true,
  width = 300,
}) => {
  const { colors, typography, spacing } = useTheme();
  
  // Slider dimensions
  const sliderWidth = width - 40; // Account for thumb size
  const thumbSize = 32;
  
  // Shared values for animation
  const translateX = useSharedValue(0);
  const scale = useSharedValue(1);
  
  // Calculate initial position
  React.useEffect(() => {
    const percentage = (value - min) / (max - min);
    translateX.value = percentage * sliderWidth;
  }, [value, min, max, sliderWidth]);

  // Gesture handler
  const gestureHandler = useAnimatedGestureHandler({
    onStart: () => {
      scale.value = withSpring(1.2);
    },
    onActive: (event) => {
      const newTranslateX = Math.max(0, Math.min(sliderWidth, event.translationX + translateX.value));
      translateX.value = newTranslateX;
      
      // Calculate new value
      const percentage = newTranslateX / sliderWidth;
      const newValue = Math.round(min + percentage * (max - min));
      runOnJS(onValueChange)(newValue);
    },
    onEnd: () => {
      scale.value = withSpring(1);
      
      // Snap to step
      const percentage = translateX.value / sliderWidth;
      const rawValue = min + percentage * (max - min);
      const steppedValue = Math.round(rawValue / step) * step;
      const clampedValue = Math.max(min, Math.min(max, steppedValue));
      
      const finalPercentage = (clampedValue - min) / (max - min);
      translateX.value = withSpring(finalPercentage * sliderWidth);
      
      runOnJS(onValueChange)(clampedValue);
    },
  });

  // Animated styles
  const thumbStyle = useAnimatedStyle(() => {
    const percentage = translateX.value / sliderWidth;
    
    return {
      transform: [
        { translateX: translateX.value },
        { scale: scale.value },
      ],
      backgroundColor: interpolateColor(
        percentage,
        [0, 0.5, 1],
        [colors.danger, colors.warning, colors.success]
      ),
    };
  });

  const trackFillStyle = useAnimatedStyle(() => ({
    width: translateX.value + thumbSize / 2,
    backgroundColor: interpolateColor(
      translateX.value / sliderWidth,
      [0, 0.5, 1],
      [colors.danger, colors.warning, colors.success]
    ),
  }));

  // Mood labels and emojis
  const getMoodData = (val: number) => {
    if (val <= 2) return { emoji: '😢', label: 'Very Low', color: colors.danger };
    if (val <= 4) return { emoji: '😔', label: 'Low', color: colors.warning };
    if (val <= 6) return { emoji: '😐', label: 'Okay', color: colors.info };
    if (val <= 8) return { emoji: '🙂', label: 'Good', color: colors.success };
    return { emoji: '😊', label: 'Great', color: colors.success };
  };

  const currentMood = getMoodData(value);

  const styles = StyleSheet.create({
    container: {
      width,
      alignItems: 'center',
    },
    moodDisplay: {
      alignItems: 'center',
      marginBottom: spacing.lg,
    },
    emoji: {
      fontSize: 48,
      marginBottom: spacing.sm,
    },
    moodLabel: {
      ...typography.h3,
      color: currentMood.color,
      marginBottom: spacing.xs,
    },
    moodValue: {
      ...typography.body,
      color: colors.textSecondary,
    },
    sliderContainer: {
      height: 60,
      justifyContent: 'center',
      marginBottom: spacing.md,
    },
    track: {
      width: sliderWidth,
      height: 8,
      backgroundColor: colors.border,
      borderRadius: 4,
      position: 'relative',
    },
    trackFill: {
      height: '100%',
      borderRadius: 4,
      position: 'absolute',
      left: 0,
      top: 0,
    },
    thumb: {
      width: thumbSize,
      height: thumbSize,
      borderRadius: thumbSize / 2,
      position: 'absolute',
      top: -12,
      left: -thumbSize / 2,
      justifyContent: 'center',
      alignItems: 'center',
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 4,
      elevation: 4,
    },
    thumbIcon: {
      color: 'white',
    },
    labels: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: sliderWidth,
      paddingHorizontal: thumbSize / 2,
    },
    labelText: {
      ...typography.caption,
      color: colors.textSecondary,
    },
    scaleMarkers: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: sliderWidth,
      paddingHorizontal: thumbSize / 2,
      marginTop: spacing.xs,
    },
    marker: {
      width: 2,
      height: 8,
      backgroundColor: colors.border,
      borderRadius: 1,
    },
    activeMarker: {
      backgroundColor: colors.primary,
    },
  });

  const renderScaleMarkers = () => {
    const markers = [];
    const numberOfMarkers = max - min + 1;
    
    for (let i = 0; i < numberOfMarkers; i++) {
      const markerValue = min + i;
      const isActive = markerValue <= value;
      
      markers.push(
        <View
          key={i}
          style={[
            styles.marker,
            isActive && styles.activeMarker,
          ]}
        />
      );
    }
    
    return markers;
  };

  return (
    <View style={styles.container}>
      {/* Mood Display */}
      {showEmojis && (
        <View style={styles.moodDisplay}>
          <Text style={styles.emoji}>{currentMood.emoji}</Text>
          {showLabels && (
            <>
              <Text style={styles.moodLabel}>{currentMood.label}</Text>
              <Text style={styles.moodValue}>{value}/10</Text>
            </>
          )}
        </View>
      )}

      {/* Slider */}
      <View style={styles.sliderContainer}>
        <View style={styles.track}>
          <Animated.View style={[styles.trackFill, trackFillStyle]} />
          
          <PanGestureHandler onGestureEvent={gestureHandler}>
            <Animated.View style={[styles.thumb, thumbStyle]}>
              <Ionicons 
                name="ellipse" 
                size={12} 
                style={styles.thumbIcon}
              />
            </Animated.View>
          </PanGestureHandler>
        </View>
      </View>

      {/* Scale Markers */}
      <View style={styles.scaleMarkers}>
        {renderScaleMarkers()}
      </View>

      {/* Labels */}
      {showLabels && (
        <View style={styles.labels}>
          <Text style={styles.labelText}>Low</Text>
          <Text style={styles.labelText}>High</Text>
        </View>
      )}
    </View>
  );
};

export default MoodSlider;
