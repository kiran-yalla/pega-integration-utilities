# pega-integration-utilities

Sample Pega Platform integration utilities: REST API automation, BIX export processing, and case data extraction/reporting scripts.

## What this demonstrates

- 🔌 **REST API client** — `pega_case_client.py` wraps the Pega Constellation/DX REST API for creating cases, checking status, adding comments, and performing flow actions.
- 📦 **BIX export processing** — `bix_export_processor.py` parses Pega BIX (Business Intelligence Exchange) flat-file extracts and normalizes them into clean CSV output for downstream analytics.
- ⏱️ **SLA / goal reporting** — `sla_breach_report.py` scans a work-object extract and flags cases that are at risk of, or have already, breached their SLA deadlines — useful for daily operational stand-ups.

## Structure

```
.
├── pega_case_client.py       # REST API client for case management operations
├── bix_export_processor.py    # BIX flat-file extract parsing and normalization
└── sla_breach_report.py       # SLA/goal deadline breach and at-risk reporting
```

## Usage

```bash
python bix_export_processor.py --input extracts/WorkList_Extract.txt --delimiter "|" --output extracts/WorkList_normalized.csv
python sla_breach_report.py --input work_extract.csv --warning-hours 4
```

```python
from pega_case_client import PegaCaseClient

client = PegaCaseClient(base_url="https://mypegaenv.example.com/prweb/api/v1", access_token="<token>")
case = client.create_case("MyOrg-MyApp-Work-ServiceRequest")
```

> This is a portfolio/demonstration repository illustrating common Pega integration and platform-support automation patterns. Endpoint URLs, case types, and column names are illustrative — adapt them to your actual Pega environment before real-world use.

## Author

Kiran Yalla — Senior Platform Engineer with deep expertise in Pega Platform architecture, administration, and enterprise integrations (AES, PDC, BIX, SMA).
