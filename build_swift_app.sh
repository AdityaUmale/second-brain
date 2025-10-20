#!/bin/bash

# Second Brain - Build Swift App
# This script builds the Swift menubar application

echo "=========================================="
echo "🧠 Second Brain Swift App Builder"
echo "=========================================="

cd SecondBrainApp

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode not found! Please install Xcode from the App Store."
    exit 1
fi

echo "🔨 Building SecondBrainApp..."
xcodebuild -project SecondBrainApp.xcodeproj \
    -scheme SecondBrainApp \
    -configuration Release \
    -derivedDataPath build \
    build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📦 App location: SecondBrainApp/build/Build/Products/Release/SecondBrainApp.app"
    echo ""
    echo "To run the app:"
    echo "  open SecondBrainApp/build/Build/Products/Release/SecondBrainApp.app"
else
    echo "❌ Build failed!"
    exit 1
fi

