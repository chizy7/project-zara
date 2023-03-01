#!/bin/bash

# Kill all existing tmux sessions
tmux kill-server

cd ~/repos/project-zara;

# Fetch the latest changes from the main branch and reset the local repository
git fetch && git reset origin/main --hard

# Activate the Python virtual environment and install dependensies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

systemctl daemon-reload;
systemctl restart project-zara.service;

echo "Complete."