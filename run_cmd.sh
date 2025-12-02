#!/usr/bin/env bash
# Simple script to execute a bash command passed as arguments.
# Usage: ./run_cmd.sh ls -la /tmp

if [ $# -eq 0 ]; then
  /home/nerses/git-practice/stockify/tractatus/bin/python3 main.py
  exit 0
fi

# Execute the command exactly as given (preserves args and quoting)

