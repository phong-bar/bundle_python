---
name: bundle-inventory-reports
description: Generate inventory and product reports from the Bundle API: list products, check stock levels, view SKU details, and export inventory data. Use when a user asks for inventory reports, product lists, stock checks, or SKU information through Bundle.
---

# Bundle Inventory Reports

Generate inventory and product reports from the Bundle API.

## Quick Reference

### List Products (via direct API)

```python
import requests
from bundle_cli import api

bundle = api.Bundle()
bundle.login()
# The SDK does not wrap product listing — use requests directly
headers = {"Authorization": f"Bearer {bundle.session.headers['Authorization']}"}
resp = requests.get(
    f"https://api.bundle.wayfindr.io/orders-api/clients/{bundle.client_uuid}/products",
    headers=headers
)
products = resp.json()
for p in products:
    print(p["sku"], p["title"], p["quantity"], p["status"])
```

### Export Products to Excel

```
GET .../clients/{client_uuid}/products/export
```

Returns a downloadable `.xlsx` file with all products.

### Update SKU Quantity

```python
bundle.update_sku_qty(sku="SKU123", qty=50)
```

## Report Workflow

1. `Bundle()` → `.login()` → `.select_client(name)` → run report
2. Product listing not wrapped in SDK — use HTTP GET directly
3. Excel export available for bulk data

## Key Data Points

- SKU, title, description
- Quantity on hand, allocated quantity
- Status: `in_stock`, `out_of_stock`, `sold_out`
- Weight, dimensions
- Price, supplier tag
- Warehouse assignment

## SDK Methods

| Method | Description |
|--------|-------------|
| `.select_inventory_item(supplier_tag=...)` | Find inventory by supplier tag |
| `.create_inventory_item(**data)` | Create new product |
| `.update_inventory_item_data(**data)` | Update product fields |
| `.update_sku_qty(sku, qty)` | Update stock quantity |
