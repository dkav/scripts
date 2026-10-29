#!/usr/bin/env python3
"""Combine OverDrive/Libby History CSV files into a unified CSV file.

Input format:
  history-export-<library>-<Date>.csv

Output format:
  overdrive-history-<YYYYMMDD>.csv (where YYYYMMDD is execution date)

Features:
- Automatically detects input files matching history-export-*.csv.
- Ignores existing output/combined files.
- Unifies and sorts records reverse-chronologically (newest loan first).
- Caches parsed dates for optimized parsing performance.
- Uses indexed streaming csv.reader for minimal memory footprint.
- Preserves UTF-8 BOM encoding for seamless viewing in Excel/Numbers.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

DATE_COLUMN_NAME = "date added to history"
MIN_DATETIME = datetime.min.replace(tzinfo=UTC)


@lru_cache(maxsize=1024)
def parse_loan_date(date_str: str) -> datetime:
    """Parse 'Loan Month Day, Year' into a timezone-aware datetime object.

    Args:
        date_str: Raw loan date string from history export.

    Returns:
        Timezone-aware datetime or MIN_DATETIME on failure.

    """
    if not date_str:
        return MIN_DATETIME
    clean_date = date_str.replace("Loan", "").strip()
    try:
        dt = datetime.strptime(clean_date, "%B %d, %Y")  # noqa: DTZ007
        return dt.replace(tzinfo=UTC)
    except ValueError:
        return MIN_DATETIME


def find_input_files(
    input_dir: Path,
    pattern: str | None = None,
) -> list[Path]:
    """Find CSV files matching the specified pattern or default export pattern.

    Args:
        input_dir: Directory containing CSV exports.
        pattern: Optional custom glob pattern.

    Returns:
        List of matching Path objects excluding generated output files.

    """
    target_pattern = pattern or "history-export-*.csv"
    candidates = sorted(input_dir.glob(target_pattern))

    return [
        f
        for f in candidates
        if "combined" not in f.name.lower()
        and not f.name.startswith("overdrive-history-")
    ]


def determine_output_filename(input_dir: Path) -> Path:
    """Generate output path in format 'overdrive-history-YYYYMMDD.csv'.

    Args:
        input_dir: Directory where the output CSV should be written.

    Returns:
        Path object pointing to the output CSV destination.

    """
    run_date = datetime.now(tz=UTC).strftime("%Y%m%d")
    return input_dir / f"overdrive-history-{run_date}.csv"


def read_history_files(
    files: list[Path],
) -> tuple[list[str] | None, list[tuple[datetime, list[str]]], dict[str, int]]:
    """Read and parse rows from given history export files.

    Args:
        files: List of input CSV files to read.

    Returns:
        Tuple containing header list, parsed row records, and file row counts.

    """
    all_rows: list[tuple[datetime, list[str]]] = []
    header: list[str] | None = None
    date_col_idx = -1
    file_counts: dict[str, int] = {}

    for file_path in files:
        with file_path.open(encoding="utf-8-sig", newline="") as fp:
            reader = csv.reader(fp)
            try:
                file_header = next(reader)
            except StopIteration:
                continue

            if header is None:
                header = file_header
                if DATE_COLUMN_NAME in header:
                    date_col_idx = header.index(DATE_COLUMN_NAME)

            count = 0
            for row in reader:
                dt = MIN_DATETIME
                if 0 <= date_col_idx < len(row):
                    dt = parse_loan_date(row[date_col_idx])
                all_rows.append((dt, row))
                count += 1
            file_counts[file_path.name] = count

    return header, all_rows, file_counts


def write_combined_csv(
    output_path: Path,
    header: list[str] | None,
    rows: list[tuple[datetime, list[str]]],
) -> None:
    """Write merged rows to the target CSV file.

    Args:
        output_path: Target destination Path.
        header: Optional header row.
        rows: List of sorted (datetime, row) tuples.

    """
    with output_path.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.writer(fp)
        if header is not None:
            writer.writerow(header)
        for _, row in rows:
            writer.writerow(row)


def print_summary(
    file_counts: dict[str, int],
    total_records: int,
    output_path: Path,
) -> None:
    """Print formatted execution summary.

    Args:
        file_counts: Mapping of filename to count of records merged.
        total_records: Total record count across all files.
        output_path: Destination path of written output file.

    """
    print("=" * 68)
    print("History Export Combine Summary")
    print("=" * 68)
    for fname, count in file_counts.items():
        print(f"  • {fname:<48} : {count:>4} records")
    print("-" * 68)
    print(f"  Total records merged : {total_records:>4}")
    print(f"  Output saved to      : {output_path}")
    print("=" * 68)


def combine_history_csvs(
    input_dir: Path,
    pattern: str | None = None,
    output_path: Path | None = None,
    *,
    sort_by_date: bool = True,
) -> Path:
    """Combine multiple history-export CSVs into a single output file.

    Args:
        input_dir: Path directory containing input CSVs.
        pattern: Optional glob pattern override.
        output_path: Optional explicit output destination.
        sort_by_date: Whether to sort descending by loan date.

    Returns:
        Path to the generated output file.

    """
    files = find_input_files(input_dir, pattern)

    if not files:
        search_target = pattern or "history-export-*.csv"
        print(
            f"Error: No CSV files found matching '{search_target}' "
            f"in '{input_dir}'",
            file=sys.stderr,
        )
        sys.exit(1)

    target_output = output_path or determine_output_filename(input_dir)
    header, all_rows, file_counts = read_history_files(files)

    if sort_by_date:
        all_rows.sort(key=lambda item: item[0], reverse=True)

    write_combined_csv(target_output, header, all_rows)
    print_summary(file_counts, len(all_rows), target_output)

    return target_output


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser.

    Returns:
        Configured ArgumentParser instance.

    """
    parser = argparse.ArgumentParser(
        description=(
            "Combine history-export CSV files into one unified "
            "overdrive-history-<run_date>.csv file."
        ),
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=Path,
        default=Path(),
        help="Directory containing CSV files (default: current directory).",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default=None,
        help=(
            "Glob pattern to identify source files (default: "
            "'history-export-*.csv')."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help=(
            "Output CSV destination (default: "
            "'overdrive-history-<YYYYMMDD>.csv' with current date)."
        ),
    )
    parser.add_argument(
        "--no-sort",
        action="store_true",
        help="Do not sort rows by date; preserve input concatenation order.",
    )
    return parser


def main() -> None:
    """Execute main entry point for history combiner CLI."""
    parser = build_parser()
    args = parser.parse_args()
    combine_history_csvs(
        input_dir=args.dir,
        pattern=args.pattern,
        output_path=args.output,
        sort_by_date=not args.no_sort,
    )


if __name__ == "__main__":
    main()
