#!/bin/bash

# Set proper paths for cron environment
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"

# Project directory
PROJECT_DIR="$HOME/Documents/university/Term 7/test project"
cd "$PROJECT_DIR" || exit 1

# Activate virtual environment directly
source "$PROJECT_DIR/.venv/bin/activate"

# Run the auto-close script with Python directly
python -m todolist.cli.autoclose_task

# Exit with the python command's exit code
exit $?
