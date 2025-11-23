#!/usr/bin/env bash
# Simple script to execute a bash command passed as arguments.
# Usage: ./run_cmd.sh ls -la /tmp

if [ $# -eq 0 ]; then
  echo "I'm trying to learn how to script with bash!"
  exit 1
fi

# Execute the command exactly as given (preserves args and quoting)

