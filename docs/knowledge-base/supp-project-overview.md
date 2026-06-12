# SUPP Project Overview

## Atlassian Instance

| Field | Value |
|-------|-------|
| **Cloud ID** | `19df032c-98d3-40a7-a2c9-c86982f6f341` |
| **Jira URL** | `https://wayfindr.atlassian.net` |
| **Confluence URL** | `https://wayfindr.atlassian.net/wiki` |
| **Site Name** | wayfindr |
| **Instance Type** | Jira Cloud (1001.0.0-SNAPSHOT) |

## SUPP Jira Project

The SUPP project tracks support tickets. Each SUPP issue involves running a Bundle API script to resolve a client request (order cancellation, status update, etc.).

### Known Issue Range

| Lowest | Highest | Approximate Total |
|--------|---------|-------------------|
| SUPP-887 | SUPP-1071 | ~184 issues |

### Observed Workflow

1. Support ticket filed in SUPP project
2. Script created at repo root (`SUPP-{issue}.py`)
3. Script connects to Bundle API, performs action for client
4. Result reported back

## Confluence Space

Only the **KB** (Knowledge Base) space is publicly visible — **"Bundle Help Page"** with support documentation:

- Store Configuration Page
- Connect Shopify Store to Bundle
- Connect WooCommerce Store to Bundle

No report-specific Confluence pages found.

## Authentication

- Atlassian APIs require authenticated access for Jira data
- Bundle API uses username/password auth via `.env` (`BUNDLE_USERNAME` / `BUNDLE_PASSWORD`)
- `.env` is gitignored
