#!/bin/bash

IMAGE_NAME="uptimetracker"
CONTAINER_NAME="uptimetracker-container"
DOCKERFILE_PATH="docker/Dockerfile"

if [ "$1" == "build" ]; then
    echo "🔧 Building Docker image: $IMAGE_NAME"
    docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .
elif [ "$1" == "run" ]; then
    echo "🚀 Running container: $CONTAINER_NAME"
    docker run --rm --name $CONTAINER_NAME $IMAGE_NAME
else
    echo "❓ Usage: $0 [build|run]"
fi



#./uptimechecker.sh build
#./uptimechecker.sh run

