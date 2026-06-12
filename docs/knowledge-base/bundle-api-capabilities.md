# Bundle API Capabilities for Reporting

## Service Overview

| Service | Base Path | Endpoint Count | Status |
|---------|-----------|----------------|--------|
| Auth | `/auth-api` | 1 | Operational |
| Clients | `/clients-api` | 2 | Operational |
| Users | `/users-api` | 3 | Operational |
| Orders | `/orders-api` | 14 | Operational (some 500s) |
| Warehouse | `/warehouse-api` | 1 | Operational |
| Payments | `/payments-api` | 1 | Operational |
| Passports | `/passports-api` | 0 | Not accessible |
| Notifications | `/notifications-api` | 0 | Not accessible |

## Report-Relevant Endpoints

### Orders — Core Reporting Resource

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/orders-api/clients/{uuid}/orders` | GET | Paginated order list with full details (status, prices, addresses, order_lines, shipments). Filter by `status`, `search`. Auto-paginated in SDK. |
| `/orders-api/clients/{uuid}/orders/{uuid}` | GET | Single order with cost breakdown, addresses, line items, tax, discounts |
| `/orders-api/clients/{uuid}/orders/{uuid}/open-api-logs` | GET | Order API audit trail (timestamps, request/response) |
| `/orders-api/clients/{uuid}/products` | GET | Paginated product/inventory list (SKU, title, qty, weight, dimensions, price, supplier) |
| `/orders-api/clients/{uuid}/products/export` | GET | Excel (.xlsx) product export |
| `/orders-api/clients/{uuid}/shipments` | GET | Paginated shipment list (courier, tracking, status, weight, line items). Filter by `status`. |
| `/orders-api/clients/{uuid}/shipments/export` | GET | Excel (.xlsx) shipment export |
| `/orders-api/clients/{uuid}/analytics` | GET | Aggregated analytics: stockAccuracy, deliveryMetrics, geographicAnalysis, fulfillment |

### Clients

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/clients-api/admin/clients` | GET | List all clients (UUID, name, region, currency) — ~31 clients |
| `/clients-api/admin/clients/{uuid}` | GET | Single client details |

### Payments

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/payments-api/admin/payments` | GET | Paginated payments (transaction_id, amount, currency, status, method) — ~44K records |

### Users

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/users-api/admins` | GET | List all users (UUID, name, role, email, active) |
| `/users-api/admins/{uuid}` | GET | Single user details |

### Warehouse

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/warehouse-api/admin/warehouses` | GET | List all warehouses (UUID, tag, address, status) — ~10 warehouses |

## Analytics Endpoint

`GET .../clients/{uuid}/analytics` returns:

| Section | Content |
|---------|---------|
| `stockAccuracy` | Monthly accuracy percentages |
| `deliveryMetrics` | Avg transit days, fulfillment days, failure rate, top failure reasons |
| `geographicAnalysis` | Top destinations, regional performance, delivery time by country |
| `fulfillment` | Chart data, replenishment time, shipping time |

## SDK Wrappers (from `bundle_cli/api.py`)

| Method | API Call | Description |
|--------|----------|-------------|
| `.login()` | `POST /auth-api/auth/admin/login` | Authenticate (reads `.env`) |
| `.get_clients()` | `GET /clients-api/admin/clients` | List all clients |
| `.get_client_info(uuid)` | `GET /clients-api/admin/clients/{uuid}` | Client details |
| `.select_client(search_for_client_name=...)` | — | Search clients by name, set `client_uuid` |
| `.get_orders(status=None, search=None)` | `GET .../orders` | Auto-paginating order list |
| `.get_order_details()` | `GET .../orders/{uuid}` | Single order details |
| `.select_order(order_reference=...)` | — | Find order by reference, set `order_uuid` |
| `.update_order_status(status=...)` | `PATCH .../orders/{uuid}/status` | Change order status |
| `.update_order_details(**data)` | `PATCH .../orders/{uuid}` | Update order fields |
| `.get_shipment_list(status=None)` | `GET .../shipments` | Auto-paginating shipment list |
| `.select_inventory_item(supplier_tag=...)` | — | Find inventory by supplier tag |
| `.create_inventory_item(**data)` | `POST .../products` | Create product/inventory |
| `.update_inventory_item_data(**data)` | `PATCH .../products/{uuid}` | Update inventory fields |
| `.update_sku_qty(sku, qty)` | `PATCH .../products/{uuid}/quantity` | Update SKU quantity |
| `.reset_shipment()` | `POST .../shipments/{uuid}/reset` | Reset a shipment |
| `.manage_user(...)` | `PATCH .../users-api/admins/{uuid}` | Update user (super-admin only) |
| `.get_order_api_logs()` | `GET .../orders/{uuid}/open-api-logs` | Order audit trail |

## Notes

- Some `/orders/` endpoints return HTTP 500 (`/orders/history`, `/orders/stats`, `/orders/count`, `/orders/export`, `/shipments/stats`, etc.)
- No health check endpoint exists at `/health`, `/health-check`, `/api`, etc.
- No OpenAPI/Swagger docs exposed
