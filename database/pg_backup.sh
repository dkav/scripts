#!/bin/zsh
# Summary: Backup PostgreSQL database
#
# Usage: pg_backup {backup_dir}
#
date=$(date +%Y%m%d)
if [[ -z $1 ]]; then
  bk_dir=$PWD
else
  bk_dir=$1
fi
mkdir -p $bk_dir
bk_file=$bk_dir/pg_$date.sql

pg_dumpall -U $USER -h localhost --clean --file=$bk_file
echo "PosgreSQL database backed up to $bk_file:a"
