#!/bin/zsh
#
# Setup Ruby for Jekyll website project.
#
# Usage: setup_rb <Ruby version>

ruby_version=$1

if [ -z "$ruby_version" ]; then
  echo "Usage: setup_rb <Ruby version>"
else
  rbenv local $ruby_version
  bundle install --path vendor/bundle
fi
