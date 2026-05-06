"""Backup macOS Messages converstations.

Based off https://github.com/yortos/imessage-analysis

N.B. Full Disk Access required for Terminal to execute this script.
"""

from datetime import datetime
import os
from pathlib import Path
import shutil

import sqlite3
import pandas as pd


def main():
    """Backup and Export macOS Messages."""
    msgdir = os.path.join(Path.home(), 'Library', 'Messages')
    wkdir = os.path.join(Path.home(), 'Downloads')
    chatdb = os.path.join(msgdir, 'chat.db')
    fname = ''.join([wkdir, '/Messages ',
                     datetime.now().strftime('%Y.%m.%d')])
    ofile = ''.join([fname, '.csv'])

    # Backup folder first
    shutil.make_archive(fname, 'zip', msgdir)

    # Establish a connection
    conn = sqlite3.connect(chatdb)
    cur = conn.cursor()

    # Create pandas dataframe
    messages = pd.read_sql_query(
        '''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,
        "unixepoch","localtime") as date_utc from message''', conn)

    handles = pd.read_sql_query("select * from handle", conn)
    chat_message_joins = pd.read_sql_query("select * from chat_message_join",
                                           conn)

    # These fields are only for ease of datetime analysis (e.g., number of
    # messages per month or year)
    messages['message_date'] = messages['date']
    messages['timestamp'] = messages['date_utc'].apply(lambda x:
                                                       pd.Timestamp(x))
    messages['date'] = messages['timestamp'].apply(lambda x: x.date())
    messages['month'] = messages['timestamp'].apply(lambda x: int(x.month))
    messages['year'] = messages['timestamp'].apply(lambda x: int(x.year))

    # Rename the ROWID into message_id, because that's what it is
    messages.rename(columns={'ROWID': 'message_id'}, inplace=True)

    # Rename appropriately the handle and apple_id/phone_number as well
    handles.rename(columns={'id': 'phone_number', 'ROWID': 'handle_id'},
                   inplace=True)

    # Merge the messages with the handles
    merge_level_1 = pd.merge(
        messages[['text', 'handle_id', 'date', 'message_date', 'timestamp',
                  'month', 'year', 'is_sent', 'message_id']],
        handles[['handle_id', 'phone_number']],
        on='handle_id', how='left')

    # and then that table with the chats
    df_messages = pd.merge(merge_level_1,
                           chat_message_joins[['chat_id', 'message_id']],
                           on='message_id', how='left')

    # Save the combined table
    df_messages.to_csv(ofile, index=False, encoding='utf-8')

    # Close connections
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
