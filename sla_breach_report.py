#!/usr/bin/env python3
"""
sla_breach_report.py

Generates an SLA (goal/deadline) breach report from a Pega work-object
extract, highlighting cases that are approaching or have exceeded their
configured SLA thresholds. Useful for daily operational stand-ups and
platform-owner reporting on production stability.

Usage:
    python sla_breach_report.py --input work_extract.csv --warning-hours 4
"""

import argparse
import csv
import datetime
import sys


def parse_datetime(value):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y %H:%M"):
        try:
            return datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {value}")


def load_cases(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def evaluate_sla(cases, warning_hours):
    now = datetime.datetime.now()
    breached, at_risk = [], []

    for case in cases:
        deadline_raw = case.get("GoalDeadline") or case.get("goal_deadline")
        if not deadline_raw:
            continue
        try:
            deadline = parse_datetime(deadline_raw)
        except ValueError:
            continue

        remaining = (deadline - now).total_seconds() / 3600
        case_id = case.get("pxInsName") or case.get("case_id", "UNKNOWN")

        if remaining < 0:
            breached.append((case_id, remaining))
        elif remaining <= warning_hours:
            at_risk.append((case_id, remaining))

    return breached, at_risk


def print_report(breached, at_risk):
    print("=== SLA Breach Report ===")
    print(f"\nBreached ({len(breached)}):")
    for case_id, hrs in breached:
        print(f"  - {case_id}: {abs(hrs):.1f} hours overdue")

    print(f"\nAt risk ({len(at_risk)}):")
    for case_id, hrs in at_risk:
        print(f"  - {case_id}: {hrs:.1f} hours remaining")


def main():
    parser = argparse.ArgumentParser(description="Report on Pega case SLA breaches and at-risk cases")
    parser.add_argument("--input", required=True, help="CSV export of work objects with a GoalDeadline column")
    parser.add_argument("--warning-hours", type=float, default=4.0, help="Hours-remaining threshold for 'at risk'")
    args = parser.parse_args()

    try:
        cases = load_cases(args.input)
    except FileNotFoundError:
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    breached, at_risk = evaluate_sla(cases, args.warning_hours)
    print_report(breached, at_risk)


if __name__ == "__main__":
    main()
