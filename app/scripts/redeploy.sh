#!/bin/bash

cd ~/repos/project-zara;

# cd /root/project-zara

# Fetch the latest changes from the main branch and reset the local repository
# git fetch && git reset origin/main --hard;
git stash && git switch main && git fetch --all && git reset --hard origin/main;

# Activate the Python virtual environment and install dependensies
source venv/bin/activate;
# source python3-virtualenv/bin/activate

pip install -q -r requirements.txt;
# pip install -r requirements.txt


systemctl daemon-reload;
systemctl restart myportfolio.service;

echo "Complete."