#!/bin/zsh

# Directory containing your repos
REPO_DIR="$HOME/Repositories"

# Exit if the directory doesn't exist
[[ ! -d "$REPO_DIR" ]] && echo "Error: $REPO_DIR not found." && exit 1

echo "Checking for Git stashes in all repositories..."

# Iterate through directories only using the (/) glob qualifier
for dir in "$REPO_DIR"/*(/); do
    # Run in a subshell to keep the script's working directory stable
    (
        cd "$dir" || exit

        # Check if it's a git repo and has stashes
        if git rev-parse --is-inside-work-tree &>/dev/null; then
            stashes=$(git stash list)

            if [[ -n "$stashes" ]]; then
                # Print folder name in bold cyan, then the list
                print -P "\n%F{cyan}%B--- ${dir:t} ---%b%f"
                echo "$stashes"
            fi
        fi
    )
done
