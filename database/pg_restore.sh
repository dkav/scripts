#!/bin/zsh
# Summary: Restore PostgreSQL database
#
# Usage: pg_restore <file>
#
if [[ -z $1 ]]; then
    echo "Usage: pg_restore <file>"
else
    if [[ ! -f $1 ]]; then
      echo "Backup file $1 does not exist"
    else
      psql -f $1 postgres > /dev/null
      echo "PostgreSQL database restored from $1:a"
    fi
fi
