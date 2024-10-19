#!/bin/bash
set -e


# Set the image registry
IMAGE_REGISTRY="gemgt4gtii"
# Set the image name
IMAGE_NAME="doris"
FULL_IMAGE_NAME="${IMAGE_REGISTRY}/${IMAGE_NAME}"

# Generate the tag based on the current date and time
TAG='latest'

# Build the Docker image
docker build -t ${FULL_IMAGE_NAME}:${TAG} .
# 限制架構
# docker build --platform linux/amd64 -t ${FULL_IMAGE_NAME}:${TAG} .
# Optionally, you can also tag this build as the latest

echo '------------------------------------------------------------------------------------------------'
docker images | head -n 2
echo '------------------------------------------------------------------------------------------------'
#  push Azure Container Registry
docker push ${FULL_IMAGE_NAME}:${TAG}

