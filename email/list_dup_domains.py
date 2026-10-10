"""Script to list domains present a minimum number of times."""

import sys

import pandas as pd

DEFAULT_MIN_COUNT = 2
MIN_ARGS_FOR_COUNT = 3
COUNT_ARG_INDEX = 2


def main(argv: list[str] | None = None) -> None:
    """Run script."""
    if argv is None:
        argv = sys.argv

    csv_file = argv[1]
    if len(argv) >= MIN_ARGS_FOR_COUNT:
        min_count = int(argv[COUNT_ARG_INDEX])
    else:
        min_count = DEFAULT_MIN_COUNT

    list_dup_domains(csv_file, min_count)


def list_dup_domains(
    csv_file: str,
    min_count: int = DEFAULT_MIN_COUNT,
) -> None:
    """List domains meeting or exceeding the specified count."""
    sender_df = pd.read_csv(csv_file, header=0, comment="#")
    sender_df["domain"] = [
        ".".join((x.split("@")[-1]).rsplit(".", 2)[-2:])
        for x in sender_df["sender"]
    ]

    counts = sender_df["domain"].value_counts()
    dup_domains = counts[counts >= min_count]

    dup_domains.index.name = "Domain"
    dup_domains_df = dup_domains.reset_index(name="Count")
    dup_domains_df = dup_domains_df.sort_values(
        by=["Count", "Domain"],
        ascending=[False, True],
    )

    print(dup_domains_df.to_string(index=False))
    print(f"\nShowing domains with a count >= {min_count}:")


if __name__ == "__main__":
    main()
