---
name: bundle-mcp
description: Use the deployed Bundle MCP bridge to call Bundle APIs by capability, search text, or route path. Use when a user asks to inspect, call, test, or automate Bundle through MCP, xmcp, Bundle tools, or the Bundle MCP bridge.
---

# Bundle MCP

Call Bundle through the MCP bridge. Prefer one tool call when the target is clear.

## Defaults

- Production MCP: `https://bundle-mcp.nibras.co/mcp`
- Testing MCP: `https://bundle-testing-mcp.nibras.co/mcp`
- Local MCP: `http://localhost:3001/mcp`
- Use production unless the user explicitly says testing, staging, sandbox, or local.
- Auth may arrive as MCP `Authorization`, `?bearer=`, `?basic=`, or a tool `bearerToken`.
- Never print credentials, JWTs, reset links, API keys, or sensitive customer payloads.

## Fast Workflow

1. If the route, capability, or intent is clear, call `bundle_api_request` directly.
2. Pass one target form: `capability`, `search`, or `service` + `method` + `path`.
3. Use `pathParams` for `:params`, `query` for URL params, and `body` for JSON payloads.
4. Use `dryRun: true` when you only need the resolved method/service/path.
5. If the tool returns `ambiguous_endpoint`, retry with one returned `capability` id or add `method`/`service`.
6. Use `bundle_find_capabilities` only when you need broader discovery; include `search` and keep the default `limit`.
7. Use `bundle_auth_login` only with caller-supplied credentials. Use `bundle_get_me` only when identity matters.

## Tool Hints

- `bundle_api_request`: main tool. Resolves full ingress URLs, prefixed paths, catalog paths, capability ids, or search text.
- `bundle_find_capabilities`: compact local catalog search; returns `id`, `method`, `service`, `path`, `pathParams`, and auth metadata.
- `bundle_list_endpoints`: compatibility alias for `bundle_find_capabilities`.
- `bundle_health_check`: smoke-test the configured Bundle API origin.

## Prefixes

- `auth` -> `/auth-api`
- `users` -> `/users-api`
- `orders` -> `/orders-api`
- `warehouse` -> `/warehouse-api`
- `clients` -> `/clients-api`
- `passports` -> `/passports-api`
- `payments` -> `/payments-api`
- `root` -> `/api`

Do not add another `/api` after service prefixes. Admin login is `/auth-api/auth/admin/login`.

## Examples

```json
{ "path": "/api/healthcheck" }
```

```json
{
  "search": "orders by order uuid",
  "method": "GET",
  "pathParams": { "clientIndexUuid": "<client>", "orderUuid": "<order>" }
}
```

```json
{
  "capability": "orders.post.clients-by-id-orders",
  "pathParams": { "clientIndexUuid": "<client>" },
  "body": { "...": "..." }
}
```
