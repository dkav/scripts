#!/bin/zsh

# Set the target extension (e.g., "mov", "png", "pdf").
# Run the script without an argument to get all attachments.
EXTENSION="$1"

# Create target directory if it doesn't exist
mkdir -p ~/Documents/Msgs

# Copy database to prevent locking issues
cp ~/Library/Messages/chat.db ~/Documents/Msgs/chat_backup.db

# Build the dynamic WHERE clause and Output File Name
if [ -n "$EXTENSION" ]; then
    WHERE_SQL="WHERE (a.filename LIKE '%.${EXTENSION}' OR a.transfer_name LIKE '%.${EXTENSION}' OR a.filename LIKE '%.${EXTENSION:u}' OR a.transfer_name LIKE '%.${EXTENSION:u}')"
    OUTPUT_FILE=~/Documents/Msgs/attachments_summary_${EXTENSION}.csv
else
    WHERE_SQL=""
    OUTPUT_FILE=~/Documents/Msgs/attachments_summary_all.csv
fi

sqlite3 -csv -header ~/Documents/Msgs/chat_backup.db "
SELECT
    (
        SELECT GROUP_CONCAT(h_part.id, ', ')
        FROM chat_handle_join c_hj
        JOIN handle h_part ON c_hj.handle_id = h_part.ROWID
        WHERE c_hj.chat_id = c.ROWID
    ) AS all_participants,
    CASE
        WHEN m.is_from_me = 1 THEN 'Me'
        ELSE COALESCE(h_sender.id, 'Unknown Sender')
    END AS sender,
    datetime(m.date / 1000000000 + 978307200, 'unixepoch', 'localtime') AS message_date,
    COALESCE(a.filename, a.transfer_name) AS file_name,
    CASE
        WHEN a.total_bytes IS NOT NULL THEN ROUND(CAST(a.total_bytes AS REAL) / (1024 * 1024), 2)
        ELSE 'Unknown'
    END AS file_size_mb,
    CASE
        WHEN maj.message_id IS NULL THEN 'Hanging / Orphaned'
        WHEN a.filename IS NULL THEN 'Not Downloaded'
        ELSE 'Downloaded'
    END AS attachment_status
FROM attachment a
LEFT JOIN message_attachment_join maj ON a.ROWID = maj.attachment_id
LEFT JOIN message m ON maj.message_id = m.ROWID
LEFT JOIN chat_message_join cj ON m.ROWID = cj.message_id
LEFT JOIN chat c ON cj.chat_id = c.ROWID
LEFT JOIN handle h_sender ON m.handle_id = h_sender.ROWID
${WHERE_SQL}
ORDER BY file_size_mb DESC;
" > "${OUTPUT_FILE}"

open "${OUTPUT_FILE}"
