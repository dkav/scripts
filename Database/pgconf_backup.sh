# Summary: Backup PostgreSQL config files
#
# Usage: pgconf_bakup
#

db_dir="$HOME/Library/Application Support/Postgres/var-13"
bk_dir="$HOME/Documents/Database/Backups"
mkdir -p $bk_dir


cp "$db_dir/pg_hba.conf" $bk_dir/
cp "$db_dir/postgresql.conf" $bk_dir/
