/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary healing colors from design system
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#2563eb', // Primary Blue
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#0d9488', // Secondary Teal
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        accent: {
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981', // Accent Green
          600: '#10b981',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
        },
        success: '#059669',
        warning: '#d97706',
        danger: '#dc2626',
        info: '#2563eb',
        neutral: {
          50: '#f9fafb', // Background
          100: '#f3f4f6',
          200: '#e5e7eb', // Border
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280', // Text Secondary
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827', // Text Primary
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', 'monospace'],
      },
      fontSize: {
        'h1': ['2.25rem', { lineHeight: '2.5rem' }], // 36px/40px
        'h2': ['1.875rem', { lineHeight: '2.25rem' }], // 30px/36px
        'h3': ['1.5rem', { lineHeight: '2rem' }], // 24px/32px
        'body-lg': ['1.125rem', { lineHeight: '1.75rem' }], // 18px/28px
        'body': ['1rem', { lineHeight: '1.5rem' }], // 16px/24px
        'body-sm': ['0.875rem', { lineHeight: '1.25rem' }], // 14px/20px
        'caption': ['0.75rem', { lineHeight: '1rem' }], // 12px/16px
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        breathe: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'healing': '0 4px 20px -2px rgba(13, 148, 136, 0.1)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
