#!/usr/bin/env python3
"""
bix_export_processor.py

Processes Pega BIX (Business Intelligence Exchange) extract files —
typically pipe- or comma-delimited flat files exported from Pega work
tables — and loads them into a staging table or converts them into a
normalized CSV for downstream reporting/analytics.

Usage:
    python bix_export_processor.py --input extracts/WorkList_Extract.txt \
        --delimiter "|" --output extracts/WorkList_normalized.csv
"""

import argparse
import csv
import sys


def read_bix_extract(path, delimiter):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    return header, rows


def normalize_rows(header, rows):
    """Trim whitespace and normalize common Pega BIX column naming."""
    normalized_header = [h.strip().lower().replace(" ", "_") for h in header]
    normalized_rows = [[cell.strip() for cell in row] for row in rows]
    return normalized_header, normalized_rows


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Process a Pega BIX extract file")
    parser.add_argument("--input", required=True, help="Path to the raw BIX extract file")
    parser.add_argument("--delimiter", default="|", help="Field delimiter used in the extract (default '|')")
    parser.add_argument("--output", required=True, help="Path to write the normalized CSV output")
    args = parser.parse_args()

    try:
        header, rows = read_bix_extract(args.input, args.delimiter)
    except FileNotFoundError:
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    norm_header, norm_rows = normalize_rows(header, rows)
    write_csv(args.output, norm_header, norm_rows)

    print(f"Processed {len(norm_rows)} rows from {args.input}")
    print(f"Normalized output written to {args.output}")


if __name__ == "__main__":
    main()
