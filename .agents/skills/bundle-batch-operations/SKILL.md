---
name: bundle-batch-operations
description: Perform batch order operations on the Bundle API: cancel orders in bulk, reset orders to created status, and update multiple order statuses. Use when a user asks to cancel orders, reset orders, batch update order statuses, or process multiple order references through Bundle. This is the most common SUPP support ticket pattern.
---

# Bundle Batch Operations

Perform batch order status changes via the Bundle API.

This is the **most common SUPP ticket pattern** — ~80% of all SUPP scripts involve batch operations (cancelling or resetting orders).

## Quick Reference

### Batch Cancel Orders (most common)

```python
from bundle_cli import api

orders = """
REF1
REF2
REF3
"""

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="ClientName")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        result = bundle.update_order_status(status="cancelled")
        print(f"{order} - {result['data']['status']}")
```

### Batch Reset Orders to Created

Replace `status="cancelled"` with `status="created"`:

```python
result = bundle.update_order_status(status="created")
```

### Single Order Operation

```python
bundle.select_order(order_reference="REF123")
bundle.update_order_status("cancelled")
```

## Workflow

1. `Bundle()` → `.login()` → `.select_client(search_for_client_name="ClientName")`
2. Define order reference list (multiline string or Python list)
3. Loop: `.select_order(ref)` → `.update_order_status(status)`
4. Optionally print results

## Clients & Scale

| Client | Typical Batch Size |
|--------|-------------------|
| Takomo | 1–20 orders |
| Blueprint | 20–45 orders |
| Diggers | 12 orders |
| Auteur B2B | Single orders |

## Import Styles

Both are valid — prefer `from bundle_cli import api`:

```python
from bundle_cli import api  # preferred
api.Bundle()
```

```python
from bundle_cli.api import Bundle  # also valid
Bundle()
```

## Order List Styles

Both are valid — multiline string is preferred for larger lists:

```python
# Style A: multiline string (preferred for 5+ orders)
orders = """
REF1
REF2
REF3
"""
order_list = [line.strip() for line in orders.split(sep="\n")]

# Style B: inline list (preferred for 1-4 orders)
orders = ["REF1", "REF2", "REF3"]
```

## Valid Status Values

- `"cancelled"` — most common (~80% of scripts)
- `"created"` — for resetting orders (~20% of scripts)
- `"pending"`, `"in_progress"`, `"finalised"` — available but not used in existing scripts
