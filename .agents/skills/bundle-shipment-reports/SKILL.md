---
name: bundle-shipment-reports
description: Generate shipment-related reports from the Bundle API: list shipments by status, track deliveries, view exceptions, and export shipment data. Use when a user asks for shipment reports, tracking, delivery status, or courier information through Bundle.
---

# Bundle Shipment Reports

Generate shipment-related reports from the Bundle API.

## Quick Reference

### List Shipments by Status

```python
from bundle_cli import api

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="ClientName")
shipments = bundle.get_shipment_list(status="in_transit")
for s in shipments:
    print(s["courier"], s["tracking_number"], s["status"])
```

**Status filter values**: `created`, `in_transit`, `delivered`, `exception`

### Export Shipments to Excel

```
GET .../clients/{client_uuid}/shipments/export
```

Returns a downloadable `.xlsx` file with all shipments (no pagination).

## Report Workflow

1. `Bundle()` → `.login()` → `.select_client(name)` → run report
2. Use `.get_shipment_list(status=...)` for lists (auto-paginating)
3. Use direct export endpoint for bulk data

## Key Data Points

- Courier name, tracking number
- Shipment status and timestamps
- Weight and dimensions
- Line items in shipment
- Origin/destination addresses

## Manual API (not wrapped in SDK)

- `GET .../shipments/export` — full Excel export
