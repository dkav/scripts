#!/usr/bin/env python

"""Converts a directory full of .eml files to a single Unix "mbox" file.

Accepts as input either an individual .eml file or a directory containing one
or more .eml files.

The output mbox will be created if it doesn't already exist.  If it exists,
it will be appended to.  There is no checking for duplicates, so use caution.
If duplicate filtering is desired, it could be added to add_file_to_mbox().
Inspired by http://www.cosmicsoft.net/emlxconvert.html

Usage:
$ ./emlToMbox.py inputdir/ output.mbox
$ ./emlToMbox.py input.eml output.mbox

Requires Python 2.5 or later

STATUS:  Tested and appears to work.

Original source: https://gist.github.com/kadin2048/c332a572a388acc22d56
"""

import os
import sys
import mailbox


DEBUG = True


def main(arguments):
    """Convert eml message/s to single mbox file."""
    infile_name = arguments[1]
    dest_name = arguments[2]

    if DEBUG:
        print("Input is:  " + infile_name)
        print("Output is: " + dest_name)

    dest_mbox = mailbox.mbox(
        dest_name, create=True)  # if dest doesn't exist create it
    dest_mbox.lock()  # lock the mbox file

    if os.path.isdir(infile_name):
        if DEBUG:
            print("Detected directory as input, using directory mode")
        count = 0
        for filename in os.listdir(infile_name):
            if filename.startswith("m.") or filename.endswith(".eml"):
                try:
                    msg_file = open(os.path.join(infile_name, filename), 'r')
                except OSError:
                    sys.stderr.write("Error while opening " + filename + "\n")
                    dest_mbox.close()
                    raise
                add_file_to_mbox(msg_file, dest_mbox)
                count += 1
                msg_file.close()
        if DEBUG:
            print("Processed " + str(count) + " total files.")

    if infile_name.startswith("m.") or infile_name.endswith(".eml"):
        if DEBUG:
            print("Detected .eml file as input, using single file mode")
        try:
            msg_file = open(infile_name, 'r')
        except OSError:
            sys.stderr.write("Error while opening " + infile_name + "\n")
            dest_mbox.close()
            raise
        add_file_to_mbox(msg_file, dest_mbox)
        msg_file.close()

    dest_mbox.close()  # close/unlock the mbox file
    return 0


def add_file_to_mbox(msg_file, dest_mbox):
    """Add file to mbox.

    Any additional preprocessing logic goes here, e.g. duplicate filter.
    """
    try:
        dest_mbox.add(msg_file)
    except mailbox.Error:
        dest_mbox.close()
        raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./emlToMbox.py input outbox.mbox\n")
        sys.exit(1)
    sys.exit(main(sys.argv))
