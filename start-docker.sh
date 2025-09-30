#!/bin/bash
# Grant Research Agent Docker Startup Script for Google Cloud

set -e

echo "🇨🇦 Starting Grant Research Agent for Google Cloud..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t grant-research-agent .

# Run the container
echo "🚀 Starting Grant Research Agent..."
docker run -d \
    --name grant-research-app \
    -p 8501:8501 \
    -e GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT:-your-project-id} \
    grant-research-agent

# Wait for the service to start
echo "⏳ Waiting for service to start..."
sleep 10

# Check if container is running
if docker ps | grep -q grant-research-app; then
    echo "✅ Grant Research Agent is running!"
    echo "🌐 Access the app at: http://localhost:8501"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs:       docker logs -f grant-research-app"
    echo "   Stop container:  docker stop grant-research-app"
    echo "   Remove container: docker rm grant-research-app"
else
    echo "❌ Failed to start Grant Research Agent"
    echo "📋 Check logs with: docker logs grant-research-app"
    exit 1
fi
