# Summary: Backup PostgreSQL database
#
# Usage: pg_backup
#

d=$(date +%Y%m%d)
bk_dir="$HOME/Documents/Database/Backups"
bk_file=$bk_dir/pg_$d.sql
mkdir -p $bk_dir

pg_dumpall -U $USER -h localhost --clean --file=$bk_file
