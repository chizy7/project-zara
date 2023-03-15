#!/bin/bash
# MLH SRE work

# Kill all existing tmux sessions
tmux kill-server

cd /root/project-zara

# Fetch the latest changes from the main branch and reset the local repository
git fetch && git reset origin/main --hard

# Stop and remove any existing containers
docker-compose -f docker-compose.prod.yml down

# Build and start the new containers in detached mode
docker-compose -f docker-compose.prod.yml up -d --build

echo "Docker Build Complete."