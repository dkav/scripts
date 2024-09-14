"""Exporting Apple Screen Time to CSV.

Modified from:
https://github.com/FelixKohlhas/ScreenTime2CSV

"""

import argparse
import csv
import os
import sqlite3
import sys
from io import StringIO
from pathlib import Path


HEADER = ["app", "start_time", "end_time", "duration_seconds",
         "created_time_coca", "device_model"]


def query_database(last_created_at):
    """Query knowledgeC database."""
    knowledge_db = Path(
        "~/Library/Application Support/Knowledge/knowledgeC.db").expanduser()

    # Check if knowledgeC.db exists
    if not knowledge_db.exists():
        print(f"Could not find knowledgeC.db at {knowledge_db}.")
        sys.exit(1)

    # Check if knowledgeC.db is readable
    if not os.access(knowledge_db, os.R_OK):
        print(f"The knowledgeC.db at {knowledge_db} is not readable.\n"
              "Please grant full  disk access to the application running the "
              "script (e.g. Terminal, iTerm, VSCode etc.).")
        sys.exit(1)

    # Connect to the SQLite database
    with sqlite3.connect(knowledge_db) as con:
        cur = con.cursor()

        # Execute the SQL query to fetch data
        # Modified from:
        # https://rud.is/b/2019/10/28/spelunking-macos-screentime-app-usage-with-r/
        query = """
        SELECT
            ZOBJECT.ZVALUESTRING AS "app",
            DATETIME(ZOBJECT.ZSTARTDATE + 978307200 +
                ZOBJECT.ZSECONDSFROMGMT,'unixepoch') AS "start",
            DATETIME(ZOBJECT.ZENDDATE + 978307200 +
                ZOBJECT.ZSECONDSFROMGMT,'unixepoch') AS "end",
            ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE AS "duration",
            ZOBJECT.ZCREATIONDATE as "creation",
            ZSYNCPEER.ZMODEL AS "device_model"
        FROM
            ZOBJECT
        LEFT JOIN
            ZSOURCE ON ZOBJECT.ZSOURCE = ZSOURCE.Z_PK
        LEFT JOIN
            ZSYNCPEER ON ZSOURCE.ZDEVICEID = ZSYNCPEER.ZDEVICEID
        WHERE
            ZOBJECT.ZSTREAMNAME = "/app/usage" AND
            ZOBJECT.ZCREATIONDATE > ?
        ORDER BY
            ZOBJECT.ZCREATIONDATE DESC
        """
        cur.execute(query, (last_created_at,))

        # Fetch all rows from the result set
        return cur.fetchall()


def write_to_csv(output, delimiter):
    """Write Screen Time date to csv file."""
    if not Path(output).exists():
        st_data = query_database(0.0)
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
            writer.writerows(st_data)
    else:
        with open(output, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            old_st_data = list(reader)
        st_data = query_database(old_st_data[0][4])
        with open(output, "w", newline="", encoding="utf-8") as f_new:
            writer = csv.writer(f_new, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
            writer.writerows(st_data)
            writer.writerows(old_st_data)


def csv_to_stringio(delimiter):
    """Create StringIO csv object."""
    st_data = query_database(0.0)
    stringio_obj = StringIO()
    writer = csv.writer(stringio_obj, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADER)
    writer.writerows(st_data)
    return stringio_obj


def main():
    """Main function for screentime2csv."""
    parser = argparse.ArgumentParser(description="Query knowledge database")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument("-d", "--delimiter", default=",",
                        help="Delimiter for output file (default: comma)")
    args = parser.parse_args()

    # Prepare output format
    delimiter = args.delimiter.replace("\\t", "\t")

    if args.output:
        write_to_csv(args.output, delimiter)
    else:
        csv_output = csv_to_stringio(delimiter)
        print(csv_output.getvalue())


if __name__ == "__main__":
    main()
