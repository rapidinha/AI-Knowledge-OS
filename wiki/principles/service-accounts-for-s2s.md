# Service Accounts for S2S

**When to use:** Use this pattern when backend services need durable identities and scoped access to other services.

## Body

Model each service as a first-class account with its own active flag, optional network constraints, and assigned scopes. Do not reuse human user accounts for automated service traffic; service identities need separate lifecycle, audit, and revocation controls.

Issue API keys or equivalent service credentials as secrets tied to a service account. Store only a hash in the database, show the raw credential once, and keep any recoverable copy in a dedicated secret store if recovery is required. Validation should check format, hash match, revocation, expiry, and account activity before returning the service account's scopes.

Scope assignments should live outside the credential itself. That lets operators rotate keys without changing permissions and update scopes without reissuing every credential. Cache successful validation with a short TTL, and invalidate cache entries when keys are revoked or service-account scopes change.

## Trade-offs

- Services get least-privilege identities instead of shared platform secrets.
- Key rotation and permission changes can be managed independently.
- Validation adds operational dependencies on the auth service, cache, and secret storage.
- Short cache TTLs improve revocation speed but increase validation load.

## Anti-patterns

- Sharing one API key across multiple services.
- Storing raw service credentials in the primary database.
- Granting a generic admin scope to every service caller.
- Updating service-account scopes without invalidating credential-validation caches.
- Relying on optional network constraints without enforcing them in the validation path.

## Checklist for a new project

- [ ] Create one service account per service or automated actor.
- [ ] Assign only the scopes required by that actor's current integrations.
- [ ] Hash credentials before storage and show raw credentials only once.
- [ ] Enforce expiry, revocation, account activity, and any network constraints during validation.
- [ ] Audit create, revoke, delete, and scope-assignment operations.
- [ ] Invalidate caches when credentials or service-account scopes change.

## Case studies

- [identity-pbac-and-auth](../case-studies/t%61ngram/identity-pbac-and-auth.md) — Shows service accounts, service scopes, API keys, and validation caches.

## Related

- [[principles/dual-channel-auth-jwt-and-service-credentials]]
- [[principles/pbac-scopes-in-tokens]]
- [[MOC/security-authz]]
