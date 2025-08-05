import React, { createContext, useContext, ReactNode } from 'react';
import { Appearance, ColorSchemeName } from 'react-native';

// Define healing-focused color palette for professional wellness platform
export const Colors = {
  // Primary Colors - Calming Blues for Trust & Stability
  primary: '#2563EB',
  primaryLight: '#3B82F6',
  primaryDark: '#1D4ED8',
  
  // Secondary Colors - Healing Teals for Growth & Balance
  secondary: '#0D9488',
  secondaryLight: '#14B8A6',
  secondaryDark: '#0F766E',
  
  // Accent Colors - Supportive Purples for Wisdom & Calm
  accent: '#8B5CF6',
  accentLight: '#A78BFA',
  accentDark: '#7C3AED',
  
  // Semantic Colors
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  info: '#06B6D4',
  
  // Text Colors with Professional Hierarchy
  textPrimary: '#1F2937',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  textInverse: '#FFFFFF',
  
  // Background Colors for Sanctuary Feel
  background: '#FFFFFF',
  backgroundSecondary: '#F8FAFC',
  surface: '#F1F5F9',
  card: '#FFFFFF',
  border: '#E2E8F0',
  divider: '#F1F5F9',
  overlay: 'rgba(0, 0, 0, 0.5)',
  
  // Wellness-specific Healing Colors
  calm: '#E0E7FF',      // Soft blue for tranquility
  growth: '#D1FAE5',    // Gentle green for progress
  focus: '#FEF3C7',     // Warm yellow for concentration
  peace: '#CFFAFE',     // Light cyan for serenity
  strength: '#FEE2E2',  // Soft red for courage
  wisdom: '#F3E8FF',    // Light purple for insight
  
  // Mood-specific Colors
  moodVeryLow: '#FEE2E2',    // Very soft red
  moodLow: '#FEF3C7',        // Soft yellow
  moodNeutral: '#F0F9FF',    // Very light blue
  moodGood: '#D1FAE5',       // Soft green
  moodGreat: '#E0E7FF',      // Soft blue
  
  // Gradient Backgrounds for Premium Feel
  gradientPrimary: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
  gradientSecondary: 'linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)',
  gradientCalm: 'linear-gradient(135deg, #A855F7 0%, #8B5CF6 100%)',
  gradientGrowth: 'linear-gradient(135deg, #22C55E 0%, #10B981 100%)',
  gradientPeace: 'linear-gradient(135deg, #0EA5E9 0%, #06B6D4 100%)',
  
  // Shadow Colors for Depth
  shadowLight: 'rgba(0, 0, 0, 0.08)',
  shadowMedium: 'rgba(0, 0, 0, 0.12)',
  shadowHeavy: 'rgba(0, 0, 0, 0.20)',
  shadowColored: 'rgba(59, 130, 246, 0.15)',
  
  // Dark mode variants with healing considerations
  dark: {
    primary: '#3B82F6',
    primaryLight: '#60A5FA',
    primaryDark: '#2563EB',
    secondary: '#14B8A6',
    secondaryLight: '#2DD4BF',
    secondaryDark: '#0D9488',
    accent: '#A78BFA',
    accentLight: '#C4B5FD',
    accentDark: '#8B5CF6',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
    info: '#06B6D4',
    textPrimary: '#F8FAFC',
    textSecondary: '#CBD5E1',
    textTertiary: '#94A3B8',
    textInverse: '#1F2937',
    background: '#0F172A',
    backgroundSecondary: '#1E293B',
    surface: '#334155',
    card: '#1E293B',
    border: '#475569',
    divider: '#374151',
    overlay: 'rgba(0, 0, 0, 0.7)',
    calm: '#1E3A8A',
    growth: '#065F46',
    focus: '#92400E',
    peace: '#164E63',
    strength: '#991B1B',
    wisdom: '#581C87',
    moodVeryLow: '#7F1D1D',
    moodLow: '#78350F',
    moodNeutral: '#1E3A8A',
    moodGood: '#064E3B',
    moodGreat: '#312E81',
    shadowLight: 'rgba(0, 0, 0, 0.3)',
    shadowMedium: 'rgba(0, 0, 0, 0.4)',
    shadowHeavy: 'rgba(0, 0, 0, 0.6)',
    shadowColored: 'rgba(59, 130, 246, 0.3)',
  }
};

// Typography scale optimized for wellness and healing
export const Typography = {
  // Display fonts for headings - Merriweather for warmth
  display: {
    fontFamily: 'Merriweather, serif',
    fontWeight: '400',
    letterSpacing: -0.025,
  },
  
  // Body fonts for content - Inter for clarity
  bodyFont: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontWeight: '400',
    letterSpacing: 0,
  },
  
  // Font sizes with healing hierarchy
  h1: {
    fontSize: 48,
    fontWeight: '700',
    lineHeight: 1.2,
    letterSpacing: -0.025,
    fontFamily: 'Merriweather, serif',
  },
  h2: {
    fontSize: 36,
    fontWeight: '600',
    lineHeight: 1.3,
    letterSpacing: -0.02,
    fontFamily: 'Merriweather, serif',
  },
  h3: {
    fontSize: 30,
    fontWeight: '600',
    lineHeight: 1.3,
    letterSpacing: -0.01,
    fontFamily: 'Inter, sans-serif',
  },
  h4: {
    fontSize: 24,
    fontWeight: '600',
    lineHeight: 1.4,
    fontFamily: 'Inter, sans-serif',
  },
  h5: {
    fontSize: 20,
    fontWeight: '600',
    lineHeight: 1.4,
    fontFamily: 'Inter, sans-serif',
  },
  h6: {
    fontSize: 18,
    fontWeight: '600',
    lineHeight: 1.4,
    fontFamily: 'Inter, sans-serif',
  },
  body: {
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 1.6,
    fontFamily: 'Inter, sans-serif',
  },
  bodyLarge: {
    fontSize: 18,
    fontWeight: '400',
    lineHeight: 1.6,
    fontFamily: 'Inter, sans-serif',
  },
  bodySmall: {
    fontSize: 14,
    fontWeight: '400',
    lineHeight: 1.5,
    fontFamily: 'Inter, sans-serif',
  },
  caption: {
    fontSize: 12,
    fontWeight: '400',
    lineHeight: 1.4,
    fontFamily: 'Inter, sans-serif',
  },
  button: {
    fontSize: 16,
    fontWeight: '600',
    lineHeight: 1.2,
    fontFamily: 'Inter, sans-serif',
    letterSpacing: 0.01,
  },
  overline: {
    fontSize: 12,
    fontWeight: '700',
    lineHeight: 1.2,
    fontFamily: 'Inter, sans-serif',
    letterSpacing: 0.1,
    textTransform: 'uppercase',
  },
};

// Spacing system for consistent layout
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Border radius
export const BorderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 9999,
};

// Shadow styles
export const Shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.15,
    shadowRadius: 15,
    elevation: 6,
  },
};

interface ThemeContextType {
  colors: typeof Colors;
  typography: typeof Typography;
  spacing: typeof Spacing;
  borderRadius: typeof BorderRadius;
  shadows: typeof Shadows;
  isDark: boolean;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [colorScheme, setColorScheme] = React.useState<ColorSchemeName>(
    Appearance.getColorScheme()
  );

  React.useEffect(() => {
    const subscription = Appearance.addChangeListener(({ colorScheme }) => {
      setColorScheme(colorScheme);
    });

    return () => subscription?.remove();
  }, []);

  const isDark = colorScheme === 'dark';

  const toggleTheme = () => {
    setColorScheme(isDark ? 'light' : 'dark');
  };

  const theme: ThemeContextType = {
    colors: isDark ? { ...Colors, ...Colors.dark } : Colors,
    typography: Typography,
    spacing: Spacing,
    borderRadius: BorderRadius,
    shadows: Shadows,
    isDark,
    toggleTheme,
  };

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
