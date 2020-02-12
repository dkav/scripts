#!/bin/zsh

git filter-branch --env-filter '

old_email="your-old-email@example.com"
correct_name="Your Correct Name"
correct_email="your-correct-email@example.com"

if [ "$GIT_COMMITTER_EMAIL" = "$old_email" ]
then
    export GIT_COMMITTER_NAME="$correct_name"
    export GIT_COMMITTER_EMAIL="$correct_email"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$old_email" ]
then
    export GIT_AUTHOR_NAME="$correct_name"
    export GIT_AUTHOR_EMAIL="$correct_email"
fi
' --tag-name-filter cat -- --branches --tags
