# Agents guide for bundle_python

## Run

```bash
python -m bundle_cli.main login
python -m bundle_cli.main search-client "Client Name"
python -m bundle_cli.main search-order "Client Name" "OrderRef"
```

## Setup

- Credentials in `.env` at repo root: `BUNDLE_USERNAME=...` / `BUNDLE_PASSWORD=...`
- Install: `pip install -r requirements.txt`
- No `pyproject.toml`, `setup.py`, or lockfile — pure `requirements.txt`
- No tests, no linter, no type checker, no CI
- **Gotcha**: `requirements.txt` lists `dotenv` but the real package is `python-dotenv` — the import is `from dotenv import load_dotenv`

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
