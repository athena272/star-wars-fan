#!/usr/bin/env bash
# Deploy Star Wars Fan API: Cloud Function (2nd gen) + API Gateway
# Usage: ./scripts/deploy.sh [PROJECT_ID] [REGION]
# Requires: gcloud CLI, project with billing enabled

set -e

PROJECT_ID="${1:-$(gcloud config get-value project 2>/dev/null)}"
REGION="${2:-us-central1}"
FUNCTION_NAME="star-wars-fan"
RUNTIME="python311"

if [ -z "$PROJECT_ID" ]; then
  echo "Error: PROJECT_ID required. Usage: $0 PROJECT_ID [REGION]"
  exit 1
fi

echo "Deploying to project=$PROJECT_ID region=$REGION"

# Enable APIs
gcloud services enable cloudfunctions.googleapis.com run.googleapis.com apigateway.googleapis.com --project="$PROJECT_ID"

# Deploy Cloud Function (from repo root)
cd "$(dirname "$0")/.."
gcloud functions deploy "$FUNCTION_NAME" \
  --gen2 \
  --runtime="$RUNTIME" \
  --region="$REGION" \
  --source=. \
  --entry-point=cloud_function_handler \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars "SWAPI_BASE_URL=https://swapi.dev/api,CACHE_TTL_SECONDS=300" \
  --memory=256Mi \
  --timeout=60s

# Get function URL
FUNCTION_URL=$(gcloud functions describe "$FUNCTION_NAME" --region="$REGION" --gen2 --format='value(serviceConfig.uri)')
echo ""
echo "Cloud Function deployed: $FUNCTION_URL"
echo ""
echo "Next steps (API Gateway):"
echo "1. Replace CLOUD_FUNCTION_URL in openapi/api_config.yaml with: $FUNCTION_URL"
echo "2. Create API config:"
echo "   gcloud api-gateway api-configs create star-wars-config --api=star-wars-api --openapi-spec=openapi/api_config.yaml --project=$PROJECT_ID"
echo "3. Create gateway:"
echo "   gcloud api-gateway gateways create star-wars-gateway --api=star-wars-api --api-config=star-wars-config --location=$REGION --project=$PROJECT_ID"
echo "4. Create API and backend first if needed (see GCP API Gateway quickstart)."
