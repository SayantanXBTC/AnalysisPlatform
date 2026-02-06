#!/bin/bash

# Techathon Frontend Deployment Script for Netlify

echo "🚀 Deploying Techathon Frontend to Netlify"
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the Techathon root directory"
    exit 1
fi

# Navigate to frontend
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the project
echo "🔨 Building frontend..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📥 Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
netlify deploy --prod --dir=dist

echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Copy your Netlify URL"
echo "2. Update backend CORS_ORIGINS with this URL"
echo "3. Test your application"