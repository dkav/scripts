# Summary: Restore PostgreSQL database
#
# Usage: Usage: pgconf_restore
#

bk_dir="$HOME/Documents/Database/Backups"
db_dir="$HOME/Library/Application Support/Postgres/var-13"

cp $bk_dir/pg_hba.conf "$db_dir/"
cp $bk_dir/postgresql.conf "$db_dir/"
