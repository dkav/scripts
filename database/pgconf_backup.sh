#!/bin/zsh
# Summary: Backup PostgreSQL config files
#
# Usage: pgconf_bakup {backup_dir}
#
db_dir="$HOME/Library/Application Support/Postgres/var-14"

if [[ -z $1 ]]; then
  bk_dir=$PWD
else
  bk_dir=$1
fi
mkdir -p $bk_dir
cp "$db_dir/pg_hba.conf" $bk_dir/
cp "$db_dir/postgresql.conf" $bk_dir/
echo "PostgreSQL config files backed up to $bk_dir:a folder"
