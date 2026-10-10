"""Script to list domain-only entries (no user part) in an email list."""
import sys

import pandas as pd


def main(argv=None):
    """Run script."""
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        sys.exit(f"Usage: {argv[0]} <csv_file>")
    list_domain_entries(argv[1])


def list_domain_entries(csv_file):
    """List entries that are domains only, e.g. 'example.com' or '@example.com'."""
    sender_df = pd.read_csv(csv_file, header=0, comment="#")
    senders = sender_df["sender"].dropna().astype(str).str.strip()
    # A domain-only entry has no "@", or only a leading "@" (Outlook accepts both).
    domain_only = senders[~senders.str.lstrip("@").str.contains("@")]
    domains = sorted(set(domain_only.str.lstrip("@").str.lower()))
    print("\n".join(domains))
    print(f"\n{len(domains)} domain-only entries", file=sys.stderr)


if __name__ == "__main__":
    main()
