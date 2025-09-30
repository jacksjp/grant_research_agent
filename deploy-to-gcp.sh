#!/bin/bash
# Deploy Grant Research Agent to Google Cloud Run

set -e

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="grant-research-agent"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🇨🇦 Deploying Grant Research Agent to Google Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Set the project
echo "🔧 Setting Google Cloud project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push the Docker image
echo "🔨 Building and pushing Docker image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 100 \
    --min-instances 0 \
    --timeout 300 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
    --set-env-vars="STREAMLIT_SERVER_PORT=8501" \
    --set-env-vars="STREAMLIT_SERVER_ADDRESS=0.0.0.0"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your Grant Research Agent is available at:"
echo "   ${SERVICE_URL}"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}' --limit 50 --format='table(timestamp,textPayload)'"
echo "   Update:       gcloud run deploy ${SERVICE_NAME} --image ${IMAGE_NAME} --region ${REGION}"
echo "   Delete:       gcloud run services delete ${SERVICE_NAME} --region ${REGION}"
