# Summary: Restore PostgreSQL database
#
# Usage: pg_restore <date>
#

if [ -z "$1" ]; then
    echo "Usage: pg_restore <date>"
else

    bk_dir="$HOME/Documents/Database/Backups"

    psql -f $bk_dir/pg_"$1".sql postgres
fi
