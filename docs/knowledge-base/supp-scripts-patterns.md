# SUPP Scripts — Patterns & Conventions

## All Scripts (15 total)

| Script | Client | Action | Orders |
|--------|--------|--------|--------|
| `SUPP-887.py` | Auteur B2B | Inspect order details | 1 |
| `SUPP-903.py` | Blueprint | Cancel orders | 1 |
| `supp-903.py` | Blueprint | Cancel orders | 1 |
| `supp-906.py` | Takomo | Cancel orders | 1 |
| `SUPP-907.py` | Takomo | Cancel orders | 2 |
| `SUPP-911.py` | Takomo | Cancel orders | 16 |
| `SUPP-918.py` | Takomo | Cancel orders | 15 |
| `SUPP-987.py` | Takomo | Cancel orders | 7 |
| `SUPP-994.py` | Takomo | Cancel orders | 8 |
| `SUPP-1014.py` | Blueprint | Set status to "created" | ~45 |
| `SUPP-1034.py` | Takomo | Cancel orders | 5 |
| `SUPP-1035.py` | Blueprint | Set status to "created" | ~20 |
| `SUPP-1053.py` | Takomo | Cancel orders | 20 |
| `SUPP-1063.py` | Diggers | Cancel orders | 12 |
| `SUPP-1066.py` | Takomo | Cancel orders | 5 |
| `SUPP-1071.py` | Blueprint | Set status to "created" | ~25 |

## Script Categories

| Category | Scripts | Description |
|----------|---------|-------------|
| **Batch Order Cancellation** | 903, supp-903, supp-906, 907, 911, 918, 987, 994, 1034, 1053, 1063, 1066 | Loop through order refs, set status to `"cancelled"` |
| **Batch Order Reset to Created** | 1014, 1035, 1071 | Loop through order refs, set status to `"created"` |
| **Order Detail Inspection** | 887 | Fetch and print order details |

## Clients & Frequency

| Client | Scripts |
|--------|---------|
| **Takomo** | 9 scripts |
| **Blueprint** | 4 scripts |
| **Auteur B2B** | 1 script |
| **Diggers** | 1 script |

## Status Values Used

| Status | Scripts |
|--------|---------|
| `"cancelled"` | 12 scripts |
| `"created"` | 3 scripts |

## Canonical Script Template

```python
from bundle_cli import api

orders = """
REF1
REF2
REF3
"""
status = "cancelled"  # or "created"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="ClientName")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        result = bundle.update_order_status(status=status)
        print(f"{order} - {result['data']['status']}")
```

## Conventions

- **No** functions, `if __name__ == "__main__"`, error handling, or argument parsing
- **Two import styles**: `from bundle_cli import api` (majority) vs `from bundle_cli.api import Bundle`
- **Two order-list styles**: multiline string (newer) vs inline Python list (older)
- All scripts are top-level imperative with hardcoded values
- Two filename conventions: `SUPP-XXX.py` and `supp-xxx.py`
