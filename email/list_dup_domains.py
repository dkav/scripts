"""Script to list domains that are present more than once in an email list."""
import sys

import pandas as pd


def main(argv=None):
    """Run script."""
    if argv is None:
        argv = sys.argv
    list_dup_domains(argv[1])


def list_dup_domains(csv_file):
    """List domains that are present more than once."""
    sender_df = pd.read_csv(csv_file, header=0, comment='#')
    sender_df['domain'] = ['.'.join((x.split('@')[-1]).rsplit('.', 2)[-2:])
                           for x in sender_df['sender']]
    dup_domains = sender_df['domain'].value_counts()[
        sender_df['domain'].value_counts() > 2]
    dup_domains.index.name = 'Domain'
    dup_domains_df = dup_domains.reset_index(name='Count')
    print(dup_domains_df.to_string(index=False))


if __name__ == "__main__":
    main()
