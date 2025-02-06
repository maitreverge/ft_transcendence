#!/bin/bash



read -p "Enter commit message: " commit_message
command="git add . && git commit -m \"$commit_message\" && git push && git status"
echo "Command to execute: $command"
read -p "Execute this command? (y/n): " execute
if [[ $execute == "y" ]]; then 
    eval "$command"
else
    echo "Command execution aborted."
fi
