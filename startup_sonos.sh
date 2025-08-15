#!/bin/bash

# Ensure script is running from its own directory
cd "$(dirname "$0")"

SESSION="sonos"

# Start a tmux session and run the Sonos API
tmux new-session -d -s $SESSION "cd node-sonos-http-api && npm start"

# Wait for the API to initialize
sleep 10

# Start the rotary encoder script in a new tmux window
tmux new-window -t $SESSION -n rotary "bash -c 'source .venv/bin/activate && python sonosController.py'"
