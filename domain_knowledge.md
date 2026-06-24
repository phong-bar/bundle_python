# Domain Knowledge

This file captures domain knowledge learned from Phong Nguyen during conversations — things not found in the codebase, docs, or AGENTS.md.

## Currency in Bundle

- The JSON field name for currency on a Bundle order is `"currency"` (e.g. `"USD"`, `"EUR"`).
- Patching `currency` via the Bundle API (`PATCH /orders-api/clients/{uuid}/orders/{uuid}` with `{"currency": "USD"}`) **does not work** — the currency is ignored by the API.
- Currency is a **client-wide setting** only. It cannot be set per-order via UI or API.
- For manual orders that need a different currency, the workaround is to ask the warehouse (e.g. KEC) to set it manually.

## Warehouse Contacts

- **KEC** — can manually adjust currency on orders at the warehouse level when the Bundle API cannot.

## Jira BUN Project

- `customfield_10182` (Team) must always be set to `Customer support` when creating BUN tickets for Phong Nguyen.
