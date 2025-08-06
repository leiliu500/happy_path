# Happy Path - Mental Wellness Platform

A professional, cross-platform mental wellness application built with Next.js, featuring healing themes, ethical AI support, and crisis intervention capabilities.

## 🌟 Features

### Core Wellness Features
- **Immediate Value Delivery**: Users experience wellness benefits within 5 minutes
- **Progressive Engagement**: AI-powered personalized wellness journey
- **Crisis Detection & Support**: 24/7 crisis intervention with professional oversight
- **Community Support**: Peer-to-peer wellness support and accountability
- **Privacy-First Design**: End-to-end encryption and user-controlled data

### Cross-Platform Support
- **Web Application**: Progressive Web App (PWA) with offline capabilities
- **Mobile Apps**: Native iOS and Android apps via Capacitor
- **Single Bootstrap Entry**: Unified codebase for all platforms
- **Responsive Design**: Optimized for all screen sizes and devices

### Professional Design
- **Healing Color Palette**: Calming teal, blue, and green themes
- **Accessibility**: WCAG 2.1 compliant design
- **Motion Design**: Smooth, therapeutic animations
- **Mobile-First**: Touch-optimized interface with safe area handling

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- iOS/Android development environment (for mobile builds)

### Installation

1. **Clone and install dependencies:**
   ```bash
   cd /Users/leiliu/projects/happy_path/frontend/app
   npm install
   ```

2. **Development server:**
   ```bash
   # Web development
   npm run dev

   # Mobile development (iOS)
   npm run dev:mobile

   # Mobile development (Android)
   npm run dev:android
   ```

3. **Production builds:**
   ```bash
   # Web build
   npm run build

   # Mobile builds
   npm run build:ios
   npm run build:android
   ```

### Development URLs
- **Web**: http://localhost:3000
- **Mobile**: Launches in simulator/device with live reload

## 📱 Platform Architecture

### Single Bootstrap Entry Point
```
src/app/
├── layout.tsx          # Root layout with platform detection
├── page.tsx            # Main landing/onboarding flow
├── providers.tsx       # Cross-platform context providers
└── components/
    ├── onboarding/     # User journey components
    ├── layout/         # Header, navigation, layout
    ├── crisis/         # Crisis support components
    └── wellness/       # Core wellness features
```

### Capacitor Integration
- **iOS**: Native iOS app with web view
- **Android**: Native Android app with web view
- **Plugins**: Camera, push notifications, haptics, native UI
- **Performance**: Native-level performance with web flexibility

## 🎨 Design System

### Color Palette
```css
/* Primary Colors */
--primary-blue: #2563EB    /* Trust, stability, professional */
--secondary-teal: #0D9488  /* Calm, healing, growth */
--accent-green: #10B981    /* Success, positive progress */

/* Status Colors */
--success: #059669
--warning: #D97706
--danger: #DC2626
--info: #2563EB

/* Neutral Colors */
--text-primary: #111827
--text-secondary: #6B7280
--background: #F9FAFB
--border: #E5E7EB
```

### Typography
- **Font**: Inter (web-optimized, accessible)
- **Scales**: H1 (36px) → Caption (12px)
- **Line Heights**: Optimized for readability

### Components
- **Healing Buttons**: Rounded, soft shadows, therapeutic colors
- **Wellness Cards**: Gradient backgrounds, healing shadow effects
- **Crisis Support**: High-contrast, immediately accessible
- **Mobile-Safe**: Handles safe areas, touch targets

## 🔐 Privacy & Security

### Privacy-First Design
- **Local-First**: Data stored locally when possible
- **Encryption**: End-to-end encryption for sensitive data
- **User Control**: Complete data export/deletion capabilities
- **Transparent**: Clear privacy dashboard and controls

### Crisis Safety
- **AI Detection**: Real-time crisis language detection
- **Professional Oversight**: Human review of crisis interventions
- **Immediate Access**: Always-available crisis support resources
- **Emergency Integration**: Direct connection to crisis hotlines

### Compliance
- **GDPR**: European privacy regulation compliance
- **CCPA**: California privacy law compliance
- **HIPAA**: Healthcare data protection (when applicable)
- **WCAG 2.1**: Web accessibility standards

## 🚀 Deployment

### Web Deployment
```bash
# Build for production
npm run build

# Deploy to your hosting platform
# The dist/ folder contains the complete static site
```

### Mobile App Store Deployment
```bash
# iOS App Store
npm run build:ios
# Follow iOS deployment guide in docs/

# Google Play Store
npm run build:android
# Follow Android deployment guide in docs/
```

### PWA Installation
- Automatic PWA installation prompts on supported browsers
- Offline functionality with smart caching
- App-like experience on mobile devices

## 🧪 User Flow Implementation

### Onboarding Journey (0-5 Minutes)
1. **Welcome Screen**: Wellness focus selection
2. **Quick Assessment**: Mood tracking and challenge input
3. **Wellness Experience**: Immediate value through activities
4. **Registration Prompt**: Value-driven account creation

### Core Features
- **Breathing Exercises**: Guided meditation with visual feedback
- **Mood Tracking**: Interactive mood sliders and insights
- **Community Features**: Peer support and accountability
- **Crisis Support**: Always-accessible emergency resources

## 🔧 Development

### Technology Stack
- **Framework**: Next.js 13+ with App Router
- **Styling**: Tailwind CSS with custom design system
- **Animation**: Framer Motion for therapeutic animations
- **Mobile**: Capacitor for native app deployment
- **PWA**: Next-PWA for web app capabilities

### Code Organization
```
src/
├── app/                 # Next.js app router
├── components/          # Reusable UI components
├── styles/             # Global styles and design system
├── utils/              # Utility functions
└── types/              # TypeScript type definitions
```

### Best Practices
- **TypeScript**: Full type safety
- **Accessibility**: ARIA labels, keyboard navigation
- **Performance**: Optimized images, lazy loading
- **SEO**: Meta tags, structured data
- **Testing**: Component and integration tests

## 📊 Analytics & Monitoring

### User Wellness Metrics
- **Mood Improvement**: Track wellness score changes
- **Engagement**: Session length, feature usage
- **Crisis Prevention**: Early intervention success rates
- **Community Health**: Peer support effectiveness

### Technical Metrics
- **Performance**: Core Web Vitals, load times
- **Accessibility**: Screen reader compatibility
- **Cross-Platform**: Feature parity across platforms
- **Privacy**: Data encryption and protection metrics

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/wellness-feature`
3. Make changes with proper testing
4. Submit pull request with detailed description

### Guidelines
- Follow existing code style and conventions
- Maintain accessibility standards
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Crisis Resources

**Immediate Emergency**: Call 911 or your local emergency services

**24/7 Crisis Support**:
- **Suicide & Crisis Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Online Chat**: suicidepreventionlifeline.org/chat

## 📞 Support

For technical support or questions:
- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues
- **Community**: Join our support forums

---

*Building a healthier world, one user at a time. 🌱*
