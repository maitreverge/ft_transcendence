#!/bin/bash

# Function to recursively search and delete "migrations" directories
delete_migrations() {
	for dir in "$1"/*; do
		if [ -d "$dir" ]; then
			if [ "$(basename "$dir")" == "migrations" ]; then
				echo "Deleting $dir"
				sudo rm -rf "$dir"
			else
				delete_migrations "$dir"
			fi
		fi
	done
}

# Start the deletion process from the current directory
delete_migrations "$(pwd)"