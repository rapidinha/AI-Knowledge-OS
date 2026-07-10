# Named Rate Limit Profiles

**When to use:** Apply different request-rate limits to login, public reads, writes, and internal traffic without scattering raw TTL/limit numbers on every handler.

## Body

Wrap the platform rate limiter in **named profiles** (for example login, refresh, create, public, send). Each profile encodes TTL window and max requests. Handlers declare the profile via a decorator; internal or metrics routes can skip throttling explicitly.

Store limiter state in a shared store (often Redis) when multiple instances must share budgets. Keep defaults in configuration so operations can tighten limits without code changes.

Separate “public generous” profiles from “auth sensitive” profiles so bots hitting login do not share the same bucket as authenticated catalog browsing.

## Trade-offs

- Consistent abuse protection with readable intent at the handler.
- Mis-assigned profiles can lock out legitimate traffic or leave holes.
- Redis-backed limiters add a dependency on cache availability for correct limiting.

## Anti-patterns

- Copy-pasting `{ ttl: 60000, limit: 100 }` literals on dozens of routes.
- One global limit for all traffic classes.
- Forgetting to skip health/metrics endpoints.

## Checklist for a new project

- [ ] Inventory traffic classes and assign profiles.
- [ ] Implement named decorators over the limiter.
- [ ] Decide shared vs in-memory storage for multi-instance deploys.
- [ ] Skip throttle on health/metrics/internal scrapers as appropriate.
- [ ] Document how to tune limits via config/env.

## Case studies

- [[MOC/engineering-practice]] — Named throttle profiles across services.
- [[MOC/security-authz]] — Auth endpoint rate limits.

## Related

- [[principles/dual-channel-auth-jwt-and-service-credentials]]
- [[principles/shared-kernel-library-extraction]]
- [[MOC/engineering-practice]]
- [[MOC/security-authz]]
