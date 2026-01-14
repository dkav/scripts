"""Add email headers to database for archived email"""
import mailbox
import sqlite3
import os
import argparse

DB_NAME = 'emails_archive.db'

def setup_database():
    """Initializes the SQLite database with the required schema."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_sent TEXT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            source_file TEXT
        )
    ''')
    conn.commit()
    return conn

def get_real_mbox_path(path):
    """
    If path is a directory (Apple Mail style), find the actual data file inside.
    If it's a standard file, return it as is.
    """
    if os.path.isdir(path):
        potential_file = os.path.join(path, 'mbox')
        if os.path.exists(potential_file):
            return potential_file
        # Using '_' to satisfy Pylint unused-variable check
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower() == 'mbox':
                    return os.path.join(root, f)
    return path

def process_single_mbox(user_path):
    """Parses an MBOX file or directory and inserts headers into the database."""
    if not os.path.exists(user_path):
        print(f"Error: Path '{user_path}' not found.")
        return

    # Handle directory-style MBOX archives
    mbox_file_path = get_real_mbox_path(user_path)

    if not os.path.isfile(mbox_file_path):
        print(f"Error: '{mbox_file_path}' is not a valid MBOX file.")
        return

    conn = setup_database()
    cursor = conn.cursor()
    display_name = os.path.basename(user_path)

    print(f"Processing {display_name}...")
    try:
        mbox = mailbox.mbox(mbox_file_path)
        for message in mbox:
            cursor.execute('''
                INSERT INTO emails (date_sent, sender, recipient, subject, source_file)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(message['Date']),
                str(message['From']),
                str(message['To']),
                str(message['Subject']),
                display_name
            ))
        conn.commit()
        print(f"Successfully archived messages from {display_name}.")
    except (mailbox.Error, sqlite3.Error) as err:
        print(f"Processing error: {err}")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract headers from an MBOX file to SQLite.")
    parser.add_argument("mbox_path", help="Path to the .mbox file or directory")

    args = parser.parse_args()
    process_single_mbox(args.mbox_path)
