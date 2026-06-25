# Agents guide for bundle_python

## Domain Knowledge

- Record any new domain knowledge from Phong in `domain_knowledge.md` (repo root).
- This includes: Bundle API quirks, warehouse contacts, workarounds, Jira field conventions, or any non-obvious info not in the codebase.

## Run

```bash
python -m bundle_cli.main login
python -m bundle_cli.main search-client "Client Name"
python -m bundle_cli.main search-order "Client Name" "OrderRef"
```

## Atlassian

- Jira/Confluence cloud ID: `19df032c-98d3-40a7-a2c9-c86982f6f341`
- When the user mentions "SUPP-XXX", it refers to a Jira ticket in the SUPP project.
- When creating BUN tickets for Phong Nguyen, always set `customfield_10182` (Team) to `Customer support`
- When replying to SUPP tickets, keep it professional but use simple words — write as if the requester is 15 years old. Avoid technical jargon or deep system explanations.
- Always set the ticket status to "Investigating" before interacting with a ticket. Halt and wait for user input if it's not feasible.
- When a SUPP ticket needs escalation to the engineering team, write a BUN ticket with detailed explanation of what needs to be done on the backend/database. Provide as much context as you can from the SUPP ticket and prompt the user if necessary. After creating the BUN ticket, mark the SUPP ticket as In Backlog with the flow: To Do → Investigating → In Backlog.
- When marking a SUPP ticket as Done, always try to fill `customfield_10002` (Request participant organization) with the client organization if it's empty. Prompt the user if it's unclear.

## Setup

- **Activate venv first**: `source .venv/bin/activate`
- Credentials in `.env` at repo root: `BUNDLE_USERNAME=...` / `BUNDLE_PASSWORD=...`
- Install: `pip install -r requirements.txt`
- No `pyproject.toml`, `setup.py`, or lockfile — pure `requirements.txt`
- No tests, no linter, no type checker, no CI
- **Gotcha**: `requirements.txt` lists `dotenv` but the real package is `python-dotenv` — the import is `from dotenv import load_dotenv`

## Bundle

- URLs matching `https://admin.bundle.wayfindr.io/*` are Bundle admin pages — use the `bundle-mcp` skill to interact with them, not a browser or web fetch.

## Bundle MCP Capabilities (cached 2026-06-24)

### auth (24)
| ID | Method | Path | Audience |
|---|---|---|---|
| `auth.get.auth-admin-change-logs` | GET | /auth/admin/change-logs | user |
| `auth.post.auth-admin-change-password` | POST | /auth/admin/change-password | user |
| `auth.post.auth-admin-forgot-password` | POST | /auth/admin/forgot-password | public |
| `auth.post.auth-admin-login` | POST | /auth/admin/login | public |
| `auth.post.auth-admin-logout` | POST | /auth/admin/logout | user |
| `auth.get.auth-admin-me` | GET | /auth/admin/me | user |
| `auth.patch.auth-admin-me` | PATCH | /auth/admin/me | user |
| `auth.post.auth-admin-reset-password` | POST | /auth/admin/reset-password | public |
| `auth.post.auth-admin-update-version` | POST | /auth/admin/update-version | user |
| `auth.get.auth-change-logs` | GET | /auth/change-logs | user |
| `auth.post.auth-change-password` | POST | /auth/change-password | user |
| `auth.post.auth-forgot-password` | POST | /auth/forgot-password | public |
| `auth.post.auth-login` | POST | /auth/login | public |
| `auth.post.auth-logout` | POST | /auth/logout | user |
| `auth.get.auth-me` | GET | /auth/me | user |
| `auth.patch.auth-me` | PATCH | /auth/me | user |
| `auth.post.auth-refresh` | POST | /auth/refresh | public |
| `auth.post.auth-reset-password` | POST | /auth/reset-password | public |
| `auth.get.auth-shopify-callback` | GET | /auth/shopify/callback | public |
| `auth.get.auth-shopify-start` | GET | /auth/shopify/start | public |
| `auth.post.auth-shopify-webhooks-compliance` | POST | /auth/shopify/webhooks/compliance | unknown |
| `auth.post.auth-update-version` | POST | /auth/update-version | user |
| `auth.get.invitations-validate` | GET | /invitations/validate | public |
| `auth.post.registrations` | POST | /registrations | public |

### clients (13)
| ID | Method | Path | Audience |
|---|---|---|---|
| `clients.get.admin-clients-by-id-statistics-order-trend` | GET | /admin/clients/:clientUuid/statistics/order-trend | user |
| `clients.get.admin-clients-by-id-statistics` | GET | /admin/clients/:clientUuid/statistics | user |
| `clients.patch.admin-clients-by-id-status` | PATCH | /admin/clients/:clientUuid/status | admin |
| `clients.get.admin-clients-by-id-storefront-configuration` | GET | /admin/clients/:clientUuid/storefront-configuration | admin-or-user |
| `clients.patch.admin-clients-by-id-storefront-configuration` | PATCH | /admin/clients/:clientUuid/storefront-configuration | admin-or-user |
| `clients.get.admin-clients-by-id-storefront-integrations` | GET | /admin/clients/:clientUuid/storefront-integrations | admin-or-user |
| `clients.patch.admin-clients-by-id-storefronts` | PATCH | /admin/clients/:clientUuid/storefronts | admin-or-user |
| `clients.get.admin-clients-by-id` | GET | /admin/clients/:clientUuid | admin-or-user |
| `clients.patch.admin-clients-by-id` | PATCH | /admin/clients/:clientUuid | admin |
| `clients.get.admin-clients-all` | GET | /admin/clients/all | admin |
| `clients.get.admin-clients-filters` | GET | /admin/clients/filters | admin |
| `clients.get.admin-clients` | GET | /admin/clients | admin |
| `clients.post.admin-clients` | POST | /admin/clients | admin |

### orders (67)
| ID | Method | Path | Audience |
|---|---|---|---|
| `orders.post.admin-storefront-sync-clients-by-id-orders-brilliant` | POST | /admin/storefront-sync/clients/:clientUuid/orders/brilliant | admin-or-user |
| `orders.post.admin-storefront-sync-clients-by-id-orders-bydesign` | POST | /admin/storefront-sync/clients/:clientUuid/orders/bydesign | admin-or-user |
| `orders.post.admin-storefront-sync-clients-by-id-orders-odoo` | POST | /admin/storefront-sync/clients/:clientUuid/orders/odoo | admin-or-user |
| `orders.post.admin-storefront-sync-clients-by-id-orders-shopee` | POST | /admin/storefront-sync/clients/:clientUuid/orders/shopee | admin-or-user |
| `orders.post.admin-storefront-sync-clients-by-id-orders-shopify` | POST | /admin/storefront-sync/clients/:clientUuid/orders/shopify | admin-or-user |
| `orders.post.admin-storefront-sync-clients-by-id-orders-woocommerce` | POST | /admin/storefront-sync/clients/:clientUuid/orders/woocommerce | admin-or-user |
| `orders.post.admin-storefronts-woocommerce-check` | POST | /admin/storefronts/woocommerce/check | admin |
| `orders.post.clients-by-id-createcommercialinvoice` | POST | /clients/:clientIndexUuid/CreateCommercialInvoice | admin-or-user |
| `orders.get.clients-by-id-order-returns-by-id` | GET | /clients/:clientIndexUuid/order-returns/:returnUuid | admin-or-user |
| `orders.get.clients-by-id-order-returns` | GET | /clients/:clientIndexUuid/order-returns | admin-or-user |
| `orders.post.clients-by-id-orders-by-id-duplicate` | POST | /clients/:clientIndexUuid/orders/:orderUuid/duplicate | admin-or-user |
| `orders.get.clients-by-id-orders-by-id-logs` | GET | /clients/:clientIndexUuid/orders/:orderUuid/logs | admin-or-user |
| `orders.get.clients-by-id-orders-by-id-open-api-logs` | GET | /clients/:clientIndexUuid/orders/:orderUuid/open-api-logs | admin-or-user |
| `orders.patch.clients-by-id-orders-by-id-status` | PATCH | /clients/:clientIndexUuid/orders/:orderUuid/status | admin-or-user |
| `orders.patch.clients-by-id-orders-by-id-warehouse-reference` | PATCH | /clients/:clientIndexUuid/orders/:orderUuid/warehouse-reference | admin-or-user |
| `orders.delete.clients-by-id-orders-by-id` | DELETE | /clients/:clientIndexUuid/orders/:orderUuid | admin-or-user |
| `orders.get.clients-by-id-orders-by-id` | GET | /clients/:clientIndexUuid/orders/:orderUuid | admin-or-user |
| `orders.patch.clients-by-id-orders-by-id` | PATCH | /clients/:clientIndexUuid/orders/:orderUuid | admin-or-user |
| `orders.get.clients-by-id-orders-export-easyship` | GET | /clients/:clientIndexUuid/orders/export/easyship | admin-or-user |
| `orders.get.clients-by-id-orders-export` | GET | /clients/:clientIndexUuid/orders/export | admin-or-user |
| `orders.get.clients-by-id-orders-filters` | GET | /clients/:clientIndexUuid/orders/filters | admin-or-user |
| `orders.get.clients-by-id-orders` | GET | /clients/:clientIndexUuid/orders | admin-or-user |
| `orders.post.clients-by-id-orders` | POST | /clients/:clientIndexUuid/orders | admin-or-user |
| `orders.get.clients-by-id-products-by-id-graph` | GET | /clients/:clientIndexUuid/products/:productUuid/graph | admin-or-user |
| `orders.get.clients-by-id-products-by-id-orders` | GET | /clients/:clientIndexUuid/products/:productUuid/orders | admin-or-user |
| `orders.patch.clients-by-id-products-by-id-quantity` | PATCH | /clients/:clientIndexUuid/products/:productUuid/quantity | admin-or-user |
| `orders.delete.clients-by-id-products-by-id` | DELETE | /clients/:clientIndexUuid/products/:productUuid | admin-or-user |
| `orders.get.clients-by-id-products-by-id` | GET | /clients/:clientIndexUuid/products/:productUuid | admin-or-user |
| `orders.patch.clients-by-id-products-by-id` | PATCH | /clients/:clientIndexUuid/products/:productUuid | admin-or-user |
| `orders.get.clients-by-id-products-all` | GET | /clients/:clientIndexUuid/products/all | admin-or-user |
| `orders.get.clients-by-id-products-export` | GET | /clients/:clientIndexUuid/products/export | admin-or-user |
| `orders.get.clients-by-id-products-filters` | GET | /clients/:clientIndexUuid/products/filters | admin-or-user |
| `orders.get.clients-by-id-products` | GET | /clients/:clientIndexUuid/products | admin-or-user |
| `orders.post.clients-by-id-products` | POST | /clients/:clientIndexUuid/products | admin-or-user |
| `orders.get.clients-by-id-shipments-by-id-logs` | GET | /clients/:clientIndexUuid/shipments/:shipmentUuid/logs | admin-or-user |
| `orders.get.clients-by-id-shipments-by-id-open-api-logs` | GET | /clients/:clientIndexUuid/shipments/:shipmentUuid/open-api-logs | admin-or-user |
| `orders.post.clients-by-id-shipments-by-id-reset` | POST | /clients/:clientIndexUuid/shipments/:shipmentUuid/reset | admin-or-user |
| `orders.get.clients-by-id-shipments-by-id` | GET | /clients/:clientIndexUuid/shipments/:shipmentUuid | admin-or-user |
| `orders.get.clients-by-id-shipments-export` | GET | /clients/:clientIndexUuid/shipments/export | admin-or-user |
| `orders.get.clients-by-id-shipments-filters` | GET | /clients/:clientIndexUuid/shipments/filters | admin-or-user |
| `orders.get.clients-by-id-shipments` | GET | /clients/:clientIndexUuid/shipments | admin-or-user |
| `orders.get.clients-by-id-warehouses` | GET | /clients/:clientIndexUuid/warehouses | admin-or-user |
| `orders.get.open-order-returns-by-id` | GET | /open/order-returns/:returnUuid | open-api |
| `orders.get.open-order-returns` | GET | /open/order-returns | open-api |
| `orders.post.open-order-returns` | POST | /open/order-returns | open-api |
| `orders.get.open-order-sync-logs-by-id-by-id` | GET | /open/order-sync-logs/:clientUuid/:sourceName | open-api |
| `orders.patch.open-orders-by-id-shipment-by-id-status` | PATCH | /open/orders/:orderUuid/shipment/:shipmentUuid/status | open-api |
| `orders.patch.open-orders-by-id-shipment-by-id` | PATCH | /open/orders/:orderUuid/shipment/:shipmentUuid | open-api |
| `orders.post.open-orders-by-id-shipment` | POST | /open/orders/:orderUuid/shipment | open-api |
| `orders.patch.open-orders-by-id-status` | PATCH | /open/orders/:orderUuid/status | open-api |
| `orders.delete.open-orders-by-id` | DELETE | /open/orders/:orderUuid | open-api |
| `orders.get.open-orders-by-id` | GET | /open/orders/:orderUuid | open-api |
| `orders.patch.open-orders-by-id` | PATCH | /open/orders/:orderUuid | open-api |
| `orders.get.open-orders` | GET | /open/orders | open-api |
| `orders.post.open-orders` | POST | /open/orders | open-api |
| `orders.get.shopee-authorize-shop` | GET | /shopee/authorize-shop | public |
| `orders.get.shopee-callback` | GET | /shopee/callback | public |
| `orders.post.shopee-trigger-sync-inventory` | POST | /shopee/trigger-sync-inventory | admin-or-user |
| `orders.post.shopee-trigger-sync-order` | POST | /shopee/trigger-sync-order | admin-or-user |
| `orders.post.shopee-webhook` | POST | /shopee/webhook | webhook |
| `orders.get.shopee` | GET | /shopee | public |
| `orders.get.storefronts-configuration` | GET | /storefronts/configuration | admin-or-user |
| `orders.patch.storefronts-configuration` | PATCH | /storefronts/configuration | admin-or-user |
| `orders.post.storefronts-shopify` | POST | /storefronts/shopify | admin-or-user |
| `orders.post.storefronts-woocommerce-check` | POST | /storefronts/woocommerce/check | admin-or-user |
| `orders.post.storefronts-woocommerce` | POST | /storefronts/woocommerce | admin-or-user |
| `orders.post.woocommerce-webhook` | POST | /woocommerce/webhook | webhook |

### warehouse (34)
| ID | Method | Path | Audience |
|---|---|---|---|
| `warehouse.get.admin-warehouses-by-id-configuration` | GET | /admin/warehouses/:warehouseUuid/configuration | admin |
| `warehouse.patch.admin-warehouses-by-id-configuration` | PATCH | /admin/warehouses/:warehouseUuid/configuration | admin |
| `warehouse.get.admin-warehouses-by-id-connections` | GET | /admin/warehouses/:warehouseUuid/connections | admin |
| `warehouse.get.admin-warehouses-by-id-openapilogs` | GET | /admin/warehouses/:warehouseUuid/openapilogs | admin |
| `warehouse.get.admin-warehouses-by-id` | GET | /admin/warehouses/:warehouseUuid | admin |
| `warehouse.get.admin-warehouses` | GET | /admin/warehouses | admin |
| `warehouse.post.clients-by-id-inbound-shipments-by-id-grn` | POST | /clients/:clientIndexUuid/inbound-shipments/:asnUuid/grn | user |
| `warehouse.get.clients-by-id-inbound-shipments-by-id-logs` | GET | /clients/:clientIndexUuid/inbound-shipments/:asnUuid/logs | user |
| `warehouse.get.clients-by-id-inbound-shipments-by-id-open-api-logs` | GET | /clients/:clientIndexUuid/inbound-shipments/:asnUuid/open-api-logs | user |
| `warehouse.post.clients-by-id-inbound-shipments-by-id-push` | POST | /clients/:clientIndexUuid/inbound-shipments/:asnUuid/push | user |
| `warehouse.delete.clients-by-id-inbound-shipments-by-id` | DELETE | /clients/:clientIndexUuid/inbound-shipments/:asnUuid | user |
| `warehouse.get.clients-by-id-inbound-shipments-by-id` | GET | /clients/:clientIndexUuid/inbound-shipments/:asnUuid | user |
| `warehouse.post.clients-by-id-inbound-shipments-create` | POST | /clients/:clientIndexUuid/inbound-shipments/create | user |
| `warehouse.get.clients-by-id-inbound-shipments` | GET | /clients/:clientIndexUuid/inbound-shipments | user |
| `warehouse.get.clients-by-id-warehouses` | GET | /clients/:clientIndexUuid/warehouses | user |
| `warehouse.get.open-warehouses-by-id-inventory` | GET | /open/warehouses/:warehouseUuid/inventory | open-api |
| `warehouse.get.open-warehouses` | GET | /open/warehouses | open-api |
| `warehouse.post.orderstatusupdate` | POST | /orderStatusUpdate | admin |
| `warehouse.post.pushorder` | POST | /pushOrder | admin-or-user |
| `warehouse.post.syncinventory` | POST | /syncInventory | admin |
| `warehouse.get.test` | GET | /test | public |
| `warehouse.post.webhook-anchanto-event` | POST | /webhook/anchanto/event | public |
| `warehouse.get.webhook-evri-health` | GET | /webhook/evri/health | public |
| `warehouse.post.webhook-evri-order-despatch` | POST | /webhook/evri/order-despatch | webhook |
| `warehouse.post.webhook-evri-order-status` | POST | /webhook/evri/order-status | webhook |
| `warehouse.post.webhook-evri-sku-stock-level` | POST | /webhook/evri/sku-stock-level | webhook |
| `warehouse.post.webhook-logiwa-event` | POST | /webhook/logiwa/event | webhook |
| `warehouse.get.webhook-shipmonk-health` | GET | /webhook/shipmonk/health | public |
| `warehouse.post.webhook-shipmonk-shipment` | POST | /webhook/shipmonk/shipment | webhook |
| `warehouse.post.webhook-vietful-event` | POST | /webhook/vietful/event | webhook |
| `warehouse.post.webhook-wave-event` | POST | /webhook/wave/event | webhook |
| `warehouse.post.webhook-wave-inventory` | POST | /webhook/wave/inventory | webhook |
| `warehouse.post.webhook-wave-orders` | POST | /webhook/wave/orders | webhook |
| `warehouse.post.webhook-wave-receipt` | POST | /webhook/wave/receipt | webhook |

### passports (16)
| ID | Method | Path | Audience |
|---|---|---|---|
| `passports.get.admin-passports-by-id-logs` | GET | /admin/passports/:passportUuid/logs | admin |
| `passports.get.admin-passports-by-id` | GET | /admin/passports/:passportUuid | admin |
| `passports.post.admin-passports-acs-export` | POST | /admin/passports/acs/export | admin |
| `passports.post.admin-passports-export` | POST | /admin/passports/export | admin |
| `passports.get.admin-passports-filters` | GET | /admin/passports/filters | admin |
| `passports.get.admin-passports-inbound-export` | GET | /admin/passports/inbound/export | admin |
| `passports.get.admin-passports-inbound` | GET | /admin/passports/inbound | admin |
| `passports.get.admin-passports-outbound-export` | GET | /admin/passports/outbound/export | admin |
| `passports.get.admin-passports-outbound` | GET | /admin/passports/outbound | admin |
| `passports.get.admin-passports-statistics` | GET | /admin/passports/statistics | admin |
| `passports.get.open-acs-address` | GET | /open/acs/address | open-api |
| `passports.post.open-acs-address` | POST | /open/acs/address | open-api |
| `passports.get.open-address` | GET | /open/address | open-api |
| `passports.post.open-address` | POST | /open/address | open-api |
| `passports.post.open-shipment` | POST | /open/shipment | open-api |
| `passports.get.test` | GET | /test | public |

### payments (15)
| ID | Method | Path | Audience |
|---|---|---|---|
| `payments.get.cgi-api-domain-prefixes-admin-filters` | GET | /CGI_API_DOMAIN_PREFIXES/admin/filters | admin |
| `payments.get.cgi-api-domain-prefixes-admin-payments-by-id` | GET | /CGI_API_DOMAIN_PREFIXES/admin/payments/:paymentUuid | admin |
| `payments.get.cgi-api-domain-prefixes-admin-payments-export` | GET | /CGI_API_DOMAIN_PREFIXES/admin/payments/export | public |
| `payments.get.cgi-api-domain-prefixes-admin-payments` | GET | /CGI_API_DOMAIN_PREFIXES/admin/payments | admin |
| `payments.get.cgi-api-domain-prefixes-admin-statistics` | GET | /CGI_API_DOMAIN_PREFIXES/admin/statistics | admin |
| `payments.get.cgi-api-domain-prefixes-countries-by-id-locations` | GET | /CGI_API_DOMAIN_PREFIXES/countries/:countryId/locations | public |
| `payments.get.cgi-api-domain-prefixes-countries` | GET | /CGI_API_DOMAIN_PREFIXES/countries | public |
| `payments.post.cgi-api-domain-prefixes-payment-by-id-3ds` | POST | /CGI_API_DOMAIN_PREFIXES/payment/:paymentUuid/3ds | public |
| `payments.get.cgi-api-domain-prefixes-payment-by-id-status` | GET | /CGI_API_DOMAIN_PREFIXES/payment/:paymentUuid/status | public |
| `payments.post.cgi-api-domain-prefixes-payment-callback` | POST | /CGI_API_DOMAIN_PREFIXES/payment/callback | public |
| `payments.get.cgi-api-domain-prefixes-payment-redirect` | GET | /CGI_API_DOMAIN_PREFIXES/payment/redirect | public |
| `payments.post.cgi-api-domain-prefixes-payment` | POST | /CGI_API_DOMAIN_PREFIXES/payment | public |
| `payments.post.cgi-api-domain-prefixes-support` | POST | /CGI_API_DOMAIN_PREFIXES/support | public |
| `payments.get.cgi-api-domain-prefixes-test` | GET | /CGI_API_DOMAIN_PREFIXES/test | public |
| `payments.post.cgi-api-domain-prefixes-verify-uid` | POST | /CGI_API_DOMAIN_PREFIXES/verify-uid | public |

### users (11)
| ID | Method | Path | Audience |
|---|---|---|---|
| `users.patch.admin-clients-by-id-users-by-id` | PATCH | /admin/clients/:clientIndexUuid/users/:userUuid | admin |
| `users.patch.admins-by-id-toggle` | PATCH | /admins/:adminUuid/toggle | admin |
| `users.get.admins-by-id` | GET | /admins/:adminUuid | admin |
| `users.patch.admins-by-id` | PATCH | /admins/:adminUuid | admin |
| `users.get.admins` | GET | /admins | admin |
| `users.post.admins` | POST | /admins | admin |
| `users.patch.clients-by-id-users-by-id-toggle` | PATCH | /clients/:clientIndexUuid/users/:userUuid/toggle | admin-or-user |
| `users.get.clients-by-id-users-by-id` | GET | /clients/:clientIndexUuid/users/:userUuid | user |
| `users.patch.clients-by-id-users-by-id` | PATCH | /clients/:clientIndexUuid/users/:userUuid | user |
| `users.get.clients-by-id-users` | GET | /clients/:clientIndexUuid/users | user |
| `users.post.clients-by-id-users` | POST | /clients/:clientIndexUuid/users | user |

### root (15)
| ID | Method | Path | Audience |
|---|---|---|---|
| `root.get.admin-dashboard-daily-performance` | GET | /admin/dashboard/daily-performance | admin |
| `root.get.admin-dashboard-monthly-performance` | GET | /admin/dashboard/monthly-performance | admin |
| `root.get.admin-dashboard-top-clients` | GET | /admin/dashboard/top-clients | admin |
| `root.get.admin-statistics` | GET | /admin/statistics | admin |
| `root.patch.admins-by-id-notifications-read` | PATCH | /admins/:adminUuid/notifications/read | admin |
| `root.get.admins-by-id-notifications` | GET | /admins/:adminUuid/notifications | admin |
| `root.get.clients-by-id-analytics` | GET | /clients/:clientIndexUuid/analytics | user |
| `root.get.clients-by-id-dashboard-monthly-performance` | GET | /clients/:clientIndexUuid/dashboard/monthly-performance | user |
| `root.get.clients-by-id-dashboard-top-weekly-skus` | GET | /clients/:clientIndexUuid/dashboard/top-weekly-skus | user |
| `root.get.clients-by-id-statistics` | GET | /clients/:clientIndexUuid/statistics | user |
| `root.get.healthcheck` | GET | /healthcheck | public |
| `root.get.notifications-admin-types` | GET | /notifications/admin/types | admin |
| `root.get.notifications-client-types` | GET | /notifications/client/types | user |
| `root.patch.users-by-id-notifications-read` | PATCH | /users/:userUuid/notifications/read | user |
| `root.get.users-by-id-notifications` | GET | /users/:userUuid/notifications | user |

## Architecture

- `bundle_cli/api.py` — stateful `Bundle` class wrapping `requests.Session`. Hardcoded base URL `https://api.bundle.wayfindr.io`
- `bundle_cli/main.py` — `click` CLI that re-logs-in per command
- `bundle_cli/helper_functions.py` — one utility: `get_latest_file_in_folder()`
- `docs/knowledge-base/` — report patterns, API capabilities, script conventions
- `~/.config/opencode/skills/bundle-*/` — agent skills for order/shipment/inventory reports and batch operations

## Workflow

- Call order: `Bundle()` → `.login()` → `.select_client(name)` → `.select_order(ref)` → action method
- `Bundle` is stateful — `client_uuid`, `order_uuid`, `inventory_item_uuid` are set on the instance
- All SUPP-* scripts at repo root are one-off per-ticket scripts. Underscore-separated filenames (supp-903, SUPP-907) — both conventions exist
- Two import styles in use (both valid): `from bundle_cli.api import Bundle` and `from bundle_cli import api`
- `.login()` without args reads `.env`. The `.env` file is gitignored

## Gotchas

- `update_order_details()` strips order lines without `inventory_uuid` before PATCH — removed lines are returned but not re-added
- `get_orders()` has **broken pagination** — it does NOT accumulate across pages, only returns the last page. Default `per_page=1000` (not 100). Use it only when results fit in one page.
- `get_shipment_list()` properly auto-paginates and accumulates all pages (default 100 per page)
- `manage_user()` requires `super-admin` or `admin` role (raises `PermissionError` otherwise)
- `requirements.txt` lists `dotenv` but real package is `python-dotenv` — `pip install dotenv` installs a different, unrelated package
