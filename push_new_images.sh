#!/bin/bash

# Pull values from environment variables or set defaults
AWS_ACCOUNT_NUMBER=${SOTW_AWS_ACCOUNT_NUMBER:-"123456789012"}
CONTAINERS=(${SOTW_CONTAINERS:-"app1 app2 app3"})
REMOTE_REPOS=(${SOTW_REMOTE_REPOS:-"repo1 repo2 repo3"})

# Check if at least one container name was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <container-name1> [<container-name2> ...]"
    echo "Available containers:"
    for i in "${!CONTAINERS[@]}"; do
        echo "${CONTAINERS[i]} -> ${REMOTE_REPOS[i]}"
    done
    exit 1
fi

echo "Logging into AWS ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "${AWS_ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com"

# Deploy each specified container
for CONTAINER_NAME in "$@"; do
    CONTAINER_INDEX=-1

    # Find the index of the selected container
    for i in "${!CONTAINERS[@]}"; do
        if [ "${CONTAINERS[i]}" == "$CONTAINER_NAME" ]; then
            CONTAINER_INDEX=$i
            break
        fi
    done

    if [ $CONTAINER_INDEX -lt 0 ]; then
        echo "Error: Container '$CONTAINER_NAME' not found. Skipping..."
        continue
    fi

    REMOTE_REPO=${REMOTE_REPOS[$CONTAINER_INDEX]}

    # Deploy process for the current container
    echo "Pushing ${CONTAINER_NAME} to ${REMOTE_REPO}..."
    docker tag "${CONTAINER_NAME}" "${REMOTE_REPO}"
    docker push "${REMOTE_REPO}"

    echo "Upload of ${CONTAINER_NAME} to ${REMOTE_REPO} complete!"
done

echo "All specified images were pushed!"
