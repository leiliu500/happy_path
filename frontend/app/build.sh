#!/bin/bash

# Happy Path Frontend Build & Deploy Script
# Cross-platform mental wellness application

set -e

echo "🌱 Happy Path - Build & Deploy Script"
echo "======================================"

# Check if we're in the correct directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run from the app directory."
    exit 1
fi

# Function to display help
show_help() {
    echo "Usage: ./build.sh [OPTION]"
    echo ""
    echo "Options:"
    echo "  dev         Start development server"
    echo "  build       Build for production (web)"
    echo "  mobile      Setup mobile development"
    echo "  ios         Build for iOS"
    echo "  android     Build for Android"
    echo "  deploy      Deploy web app"
    echo "  clean       Clean build artifacts"
    echo "  install     Install all dependencies"
    echo "  help        Show this help message"
    echo ""
}

# Function to install dependencies
install_deps() {
    echo "📦 Installing dependencies..."
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 18+ first."
        echo "   Visit: https://nodejs.org/"
        exit 1
    fi
    
    # Check Node.js version
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
        exit 1
    fi
    
    echo "✅ Node.js version: $(node -v)"
    
    # Install dependencies
    npm install
    
    echo "✅ Dependencies installed successfully!"
}

# Function to start development server
start_dev() {
    echo "🚀 Starting development server..."
    echo "   Web: http://localhost:3000"
    echo "   Press Ctrl+C to stop"
    echo ""
    npm run dev
}

# Function to build for production
build_web() {
    echo "🏗️  Building for production..."
    
    # Clean previous build
    rm -rf dist/
    
    # Build the application
    npm run build
    
    echo "✅ Production build completed!"
    echo "   Output directory: ./dist/"
    echo "   Ready for deployment!"
}

# Function to setup mobile development
setup_mobile() {
    echo "📱 Setting up mobile development..."
    
    # Check if Capacitor CLI is available
    if ! npm list -g @capacitor/cli &> /dev/null; then
        echo "📦 Installing Capacitor CLI globally..."
        npm install -g @capacitor/cli
    fi
    
    # Initialize Capacitor (if not already done)
    if [ ! -f "capacitor.config.json" ]; then
        echo "🔧 Initializing Capacitor..."
        npx cap init
    fi
    
    # Add platforms
    echo "📱 Adding mobile platforms..."
    npx cap add ios || echo "ℹ️  iOS platform already exists"
    npx cap add android || echo "ℹ️  Android platform already exists"
    
    # Sync the project
    echo "🔄 Syncing project..."
    npm run build
    npx cap sync
    
    echo "✅ Mobile setup completed!"
    echo ""
    echo "Next steps:"
    echo "  - For iOS: npm run dev:mobile"
    echo "  - For Android: npm run dev:android"
    echo "  - Make sure you have Xcode (iOS) or Android Studio installed"
}

# Function to build for iOS
build_ios() {
    echo "🍎 Building for iOS..."
    
    # Check if on macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        echo "❌ iOS builds require macOS"
        exit 1
    fi
    
    # Check if Xcode is installed
    if ! command -v xcodebuild &> /dev/null; then
        echo "❌ Xcode is not installed. Please install Xcode from the App Store."
        exit 1
    fi
    
    # Build and sync
    npm run build:ios
    
    echo "✅ iOS build completed!"
    echo "   Open ios/App/App.xcworkspace in Xcode to test or deploy"
}

# Function to build for Android
build_android() {
    echo "🤖 Building for Android..."
    
    # Check if Android Studio is available
    if [ ! -d "$HOME/Library/Android/sdk" ] && [ ! -d "$ANDROID_HOME" ]; then
        echo "❌ Android SDK not found. Please install Android Studio."
        echo "   Visit: https://developer.android.com/studio"
        exit 1
    fi
    
    # Build and sync
    npm run build:android
    
    echo "✅ Android build completed!"
    echo "   Open android/ folder in Android Studio to test or deploy"
}

# Function to deploy web app
deploy_web() {
    echo "🚀 Deploying web application..."
    
    # Build first
    build_web
    
    echo ""
    echo "📋 Deployment Options:"
    echo "   1. Vercel: vercel --prod"
    echo "   2. Netlify: netlify deploy --prod --dir=dist"
    echo "   3. GitHub Pages: Upload dist/ folder"
    echo "   4. Custom server: Copy dist/ to your web server"
    echo ""
    echo "🔗 The dist/ folder contains your complete static site"
}

# Function to clean build artifacts
clean_build() {
    echo "🧹 Cleaning build artifacts..."
    
    rm -rf dist/
    rm -rf .next/
    rm -rf node_modules/.cache/
    rm -rf ios/App/App/public/
    rm -rf android/app/src/main/assets/public/
    
    echo "✅ Build artifacts cleaned!"
}

# Function to show project status
show_status() {
    echo "📊 Project Status:"
    echo "=================="
    echo ""
    
    # Check if dependencies are installed
    if [ -d "node_modules" ]; then
        echo "✅ Dependencies: Installed"
    else
        echo "❌ Dependencies: Not installed (run: ./build.sh install)"
    fi
    
    # Check if built
    if [ -d "dist" ]; then
        echo "✅ Web build: Available"
    else
        echo "ℹ️  Web build: Not built"
    fi
    
    # Check mobile setup
    if [ -d "ios" ] && [ -d "android" ]; then
        echo "✅ Mobile platforms: Configured"
    else
        echo "ℹ️  Mobile platforms: Not configured (run: ./build.sh mobile)"
    fi
    
    echo ""
    echo "🌐 URLs:"
    echo "   Development: http://localhost:3000"
    echo "   PWA Manifest: http://localhost:3000/manifest.json"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "install")
        install_deps
        ;;
    "dev")
        install_deps
        start_dev
        ;;
    "build")
        install_deps
        build_web
        ;;
    "mobile")
        install_deps
        setup_mobile
        ;;
    "ios")
        install_deps
        build_ios
        ;;
    "android")
        install_deps
        build_android
        ;;
    "deploy")
        install_deps
        deploy_web
        ;;
    "clean")
        clean_build
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        show_help
        ;;
esac
