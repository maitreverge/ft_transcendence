#!/bin/bash

# Ths script is used to delete all "migrations" directories in the project.

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

delete_migrations "$(pwd)"