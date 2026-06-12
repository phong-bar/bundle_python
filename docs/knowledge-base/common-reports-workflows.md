# Common Reports & Workflows

## Report Categories

### 1. Order Status Reports

**Purpose**: List orders by status for a client.

```
bundle.select_client(search_for_client_name="ClientName")
orders = bundle.get_orders(status="created")  # or "pending", "in_progress", "finalised", "cancelled"
for order in orders:
    print(order["order_reference"], order["status"], order["created_at"])
```

**Filterable by**: `status`, `search` (order reference text)

**Returns**: order_reference, status, prices, addresses, order_lines, shipments, timestamps

### 2. Batch Order Status Change

**Purpose**: Update many orders to a target status (most common SUPP pattern).

```
orders = ["REF1", "REF2"]
for ref in orders:
    bundle.select_order(order_reference=ref)
    result = bundle.update_order_status(status="cancelled")  # or "created"
```

**Common targets**: `cancelled`, `created`

### 3. Order Detail Inspection

**Purpose**: View full details of a single order.

```
bundle.select_order(order_reference="REF123")
details = bundle.get_order_details()
```

**Returns**: cost breakdown, billing/shipping addresses, line items, tax, discounts, shipments

### 4. Order Audit Trail

**Purpose**: View API logs for an order.

```
bundle.select_order(order_reference="REF123")
logs = bundle.get_order_api_logs()
```

**Returns**: Timestamps, request/response data for each API call

### 5. Shipment Tracking Report

**Purpose**: List shipments by status.

```
bundle.select_client(search_for_client_name="ClientName")
shipments = bundle.get_shipment_list(status="in_transit")  # or "created", "delivered", "exception"
```

**Also**: Excel export via `GET .../shipments/export`

### 6. Inventory Report

**Purpose**: List all products/inventory for a client.

```
# Via SDK (not yet wrapped — use bundle_api_request directly)
# GET .../clients/{uuid}/products
```

**Also**: Excel export via `GET .../products/export`

**Fields**: SKU, title, quantity, allocated qty, status (in_stock/out_of_stock/sold_out), weight, dimensions, price, supplier

### 7. Analytics Dashboard

**Purpose**: Get aggregated metrics for a client.

```
# GET .../clients/{uuid}/analytics
```

**Sections**: stockAccuracy, deliveryMetrics, geographicAnalysis, fulfillment

### 8. Client List Report

**Purpose**: List all clients.

```
clients = bundle.get_clients()
```

**Fields**: UUID, name, region, currency, API key, timestamps

### 9. Payment Report

**Purpose**: List all payment records.

```
# GET /payments-api/admin/payments
```

**Fields**: transaction_id, customer, amount, currency, status, payment method

### 10. User Audit Report

**Purpose**: List all admin users.

```
# GET /users-api/admins
```

**Fields**: UUID, name, role (super-admin/admin/cgi-viewer/cgi-admin), email, active status

## Quick Reference — SDK Methods vs Manual API

| Task | SDK Method | Manual API Call |
|------|------------|-----------------|
| List clients | `bundle.get_clients()` | `GET /clients-api/admin/clients` |
| Search client | `bundle.select_client(search_for_client_name=...)` | `GET /clients-api/admin/clients?search=...` |
| List orders | `bundle.get_orders(status=..., search=...)` | `GET .../clients/{uuid}/orders` |
| Get order details | `bundle.get_order_details()` | `GET .../clients/{uuid}/orders/{uuid}` |
| Update order status | `bundle.update_order_status(status=...)` | `PATCH .../orders/{uuid}/status` |
| List shipments | `bundle.get_shipment_list(status=...)` | `GET .../clients/{uuid}/shipments` |
| List products | *(not wrapped)* | `GET .../clients/{uuid}/products` |
| Analytics | *(not wrapped)* | `GET .../clients/{uuid}/analytics` |
| List payments | *(not wrapped)* | `GET /payments-api/admin/payments` |
| List users | *(not wrapped)* | `GET /users-api/admins` |
| List warehouses | *(not wrapped)* | `GET /warehouse-api/admin/warehouses` |
