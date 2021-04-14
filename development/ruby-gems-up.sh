#!/bin/zsh
#
# Update Ruby gems.

bundle outdated

read -p "Continue with update? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  bundle update
  bundle clean
fi
