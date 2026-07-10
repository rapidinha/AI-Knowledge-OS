# PBAC Scopes in Tokens

**When to use:** Use this pattern when services need fast authorization decisions based on centrally managed permission codes.

## Body

Represent permissions as stable scope codes and issue them as claims in a signed access token. The auth service remains the source of truth for scope assignment; application services receive a compact `scopes[]` claim and do not query permission tables on every request.

Resolve active scopes at token issuance and refresh time. If assignments can expire, filter expired assignments before signing the token. If assignments have contextual dimensions, such as organization, resource, or enrollment, either encode those dimensions into explicit claims or require a second authorization check at the resource boundary.

Route handlers declare required scopes with metadata. A scope guard compares the required list with the token's `scopes[]` and allows the request when the configured rule is satisfied. The simplest useful rule is OR semantics: any one required scope grants access. Use a separate all-scopes rule only where the business rule truly needs conjunction.

## Trade-offs

- Authorization checks are cheap and consistent across services.
- Permission changes may lag until token refresh or cache invalidation.
- Scope codes are easy to audit, but contextual authorization needs additional design.

## Anti-patterns

- Treating possession of a broad scope as proof of ownership over a specific resource.
- Hiding AND semantics behind a decorator that most engineers expect to be OR semantics.
- Adding contextual fields to assignments without enforcing those fields in token claims or downstream guards.

## Checklist for a new project

- [ ] Define scope codes as stable, documented API contracts.
- [ ] Filter expired scope assignments before issuing or refreshing tokens.
- [ ] Make OR versus AND semantics explicit in guard names and tests.
- [ ] Decide how contextual permissions are represented and enforced before shipping them.
- [ ] Add cache invalidation or short token lifetimes for high-risk permission changes.

## Case studies

- [[MOC/security-authz]] — Evidence and implementation examples for this pattern.

## Related

- [[principles/dual-channel-auth-jwt-and-service-credentials]]
- [[principles/service-accounts-for-s2s]]
- [[MOC/security-authz]]
