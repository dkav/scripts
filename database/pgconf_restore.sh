#!/bin/zsh
# Summary: Restore PostgreSQL database
#
# Usage: Usage: pgconf_restore {backup_dir}
#
db_dir="$HOME/Library/Application Support/Postgres/var-14"

if [[ -z $1 ]]; then
  bk_dir=$PWD
else
  bk_dir=$1
fi
if [[ ! -d $bk_dir ]]; then
  echo "Folder $bk_dir:a does not exist"
else
  cp $bk_dir/pg_hba.conf "$db_dir/"
  cp $bk_dir/postgresql.conf "$db_dir/"
  echo "pg_hba.conf and postgresql.conf restored to $db_dir"
fi
