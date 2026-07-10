# Dual-Channel Auth with JWT and Service Credentials

**When to use:** Use this pattern when the same HTTP surface must support both human users and service-to-service callers.

## Body

Use one authentication boundary that accepts two credential channels: bearer JWTs for user sessions and a dedicated service credential header for service callers. The guard should prefer the bearer token when present, then fall back to the service credential, and reject requests that provide neither.

User login can delegate password verification to a managed IdP, then issue a platform JWT that contains application-specific claims such as subject, username, user type, and scopes. Service credentials should be validated against an auth service, then normalized into the same request identity shape used by user tokens: an authenticated principal with scopes.

Keep public-route bypasses explicit. Metrics or health endpoints can be exempt, but exemptions should be small, named, and easy to audit. Downstream authorization should not care which channel authenticated the request; it should read the normalized principal and apply scopes consistently.

## Trade-offs

- Shared guards reduce duplicated auth logic across services.
- Service callers can reuse the same scope-based authorization model as users.
- The auth boundary becomes more critical because a bug affects both user and service traffic.
- Service credential validation usually needs caching to avoid turning every request into a remote auth call.

## Anti-patterns

- Letting every service invent a different service credential header or payload shape.
- Mixing authentication and business authorization in the same guard.
- Treating public-route metadata as compatible with service-credential-only endpoints without testing the exact guard order.
- Logging raw service credentials, bearer tokens, or full authorization headers.

## Checklist for a new project

- [ ] Define a single normalized authenticated-principal model for users and services.
- [ ] Validate service credentials through an auth service or equivalent trusted authority.
- [ ] Cache successful service-credential validation with a bounded TTL.
- [ ] Ensure route-level authorization reads scopes from the normalized principal.
- [ ] Test bearer-only, service-credential-only, missing-auth, and public-route cases.

## Case studies

- [identity-pbac-and-auth](../case-studies/t%61ngram/identity-pbac-and-auth.md) — Shows bearer JWT and service credential authentication feeding the same scope guard.

## Related

- [[principles/pbac-scopes-in-tokens]]
- [[principles/service-accounts-for-s2s]]
- [[MOC/security-authz]]
