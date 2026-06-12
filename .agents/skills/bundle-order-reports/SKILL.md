---
name: bundle-order-reports
description: Generate order-related reports from the Bundle API: list orders by status, inspect order details, view order audit logs, and export order data. Use when a user asks for order reports, order lists, order status checks, or order details through Bundle.
---

# Bundle Order Reports

Generate order-related reports from the Bundle API.

## Quick Reference

### List Orders by Status

```python
from bundle_cli import api

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="ClientName")
orders = bundle.get_orders(status="created")
for o in orders:
    print(o["order_reference"], o["status"], o["created_at"])
```

**Status filter values**: `pending`, `created`, `in_progress`, `finalised`, `cancelled`

### Inspect Single Order

```python
bundle.select_order(order_reference="REF123")
details = bundle.get_order_details()
print(details["data"]["status"], details["data"]["total_price"])
```

### Order Audit Trail

```python
bundle.select_order(order_reference="REF123")
logs = bundle.get_order_api_logs()
for log in logs:
    print(log["timestamp"], log["method"], log["path"])
```

## Report Workflow

1. `Bundle()` → `.login()` → `.select_client(name)` → run report
2. Use `.get_orders(status=...)` for lists (auto-paginating, 100 per page)
3. Use `.get_order_details()` for single-order deep dive
4. Use `.get_order_api_logs()` for audit trail

## Key Data Points

- Order reference, status, timestamps (created, updated)
- Total price, shipping cost, tax breakdown
- Billing/shipping addresses
- Order lines (SKU, qty, price, weight)
- Shipments linked to order
- Discounts applied

## Manual API (not wrapped in SDK)

- `GET .../analytics` — aggregated order analytics per client
- `GET .../orders?search=...` — search orders by reference text
