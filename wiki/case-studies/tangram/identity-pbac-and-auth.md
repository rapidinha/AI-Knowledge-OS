# Identity PBAC and Auth (Tangram)

**When to use:** Read this case study when you need the concrete Tangram implementation behind JWT auth, PBAC scopes, service accounts, and S2S API keys.

## Body

Tangram centralizes user authentication in `services/identity-service` and shares request authentication primitives through `libs/backend-common`. User login verifies credentials through Cognito, then `AuthController` issues a platform JWT with `sub`, `username`, `type`, `scopes`, and optional enrollment/trail context through `TokenLogic.buildJwtPayload`.

Application services use `JwtAuthGuard` from `libs/backend-common` as a dual-channel authentication boundary. The guard allows public routes and `/metrics`, accepts bearer JWTs through the Passport JWT strategy, or validates `X-API-Key` by calling the identity API-key validation endpoint. Successful API-key validation is cached locally with a configurable TTL and materialized as a `ServiceAccountPayload` on `request.user`.

PBAC is expressed as string scope codes. Identity seeds system scopes such as `admin`, `service`, `users:read`, `backoffice:*`, and service-specific scopes. `@Scopes()` stores required scope metadata, and `ScopesGuard` allows a request when at least one required scope is present in `request.user.scopes`.

Service-to-service identity uses `ServiceAccount`, `ServiceScope`, and `ApiKey` entities. Service accounts own scopes through `service_scopes`, API keys store hashes rather than raw keys, and the validation flow checks key format, hash lookup, revocation, expiry, and service-account activity before returning scopes. `docs/architecture/service-accounts.md` documents the intended operational flow, cache tiers, and configured service accounts.

Contextual permissions are partly modeled but not fully enforced by the shared guard. `UserScope` stores `contextType`, `contextId`, and `expiresAt`; `UserRepository.findUserScopes` filters expired assignments before token issuance, but returns only scope codes. The shared `ScopesGuard` therefore cannot enforce contextual fields unless an endpoint performs an additional resource-level authorization check.

`ADR-006-user-lifecycle-lazy-expiration.md` adds an identity lifecycle decision adjacent to auth: demo and admin-managed users can carry `statusExpiresAt`, and auth touchpoints perform lazy expiration side effects before new tokens are issued. The ADR explicitly accepts that already-issued JWTs remain valid until natural expiry instead of making every service revalidate identity status on each request.

## Trade-offs

- Tangram gets a single scope model for both user JWTs and service API keys.
- Shared guards reduce auth duplication across NestJS services.
- API-key validation has bounded local and Redis caching, which reduces auth-service load but delays revocation until cache expiry unless invalidated.
- Platform JWTs are fast for downstream services, but contextual authorization is not represented in the shared `scopes[]` check.

## Anti-patterns

- Tangram avoids placing raw API keys in the database by hashing keys and showing generated keys only once.
- Tangram avoids per-service ad hoc scope checks by centralizing `@Scopes()` and `ScopesGuard`.
- A current risk is treating contextual scope assignments as fully enforced by PBAC when only `expiresAt` is enforced before token issuance.
- A current risk is relying on `allowedIps` as an API-key security control without confirming enforcement in the validation flow.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Dual-channel shared guard | `libs/backend-common/src/guards/jwt.guard.ts` | Accepts bearer JWT first, then `X-API-Key`; calls identity `/api-keys/validate`; caches successful validations locally. |
| Scope metadata and guard | `libs/backend-common/src/decorators/scopes.decorator.ts` | Defines `@Scopes()` metadata. |
| Scope metadata and guard | `libs/backend-common/src/guards/scopes.guard.ts` | Reads required scopes and authorizes with OR semantics against `request.user.scopes`. |
| Shared auth models | `libs/backend-common/src/models/auth.model.ts` | Defines `JwtPayload`, `ServiceAccountPayload`, and API-key validation result shapes. |
| JWT validation | `libs/backend-common/src/strategies/jwt.strategy.ts` | Validates bearer JWTs with the configured shared JWT secret and requires `sub`. |
| Login and token issuance | `services/identity-service/src/controllers/auth.controller.ts` | Authenticates through Cognito, loads scopes, adds optional enrollment/trail context, signs access tokens, and refreshes scopes on refresh. |
| Token payload construction | `services/identity-service/src/logic/token.logic.ts` | Builds JWT payload with `sub`, `username`, `type`, `scopes`, and optional context. |
| Scope seed catalog | `services/identity-service/src/database/seeds/003-scopes.seed.ts` | Seeds user, admin, backoffice, service, and internal service scope codes. |
| Contextual user scopes | `services/identity-service/src/diplomat/db/entities/user-scope.entity.ts` | Stores `contextType`, `contextId`, `grantedAt`, and `expiresAt`. |
| Active scope lookup | `services/identity-service/src/diplomat/db/repositories/user.repository.ts` | Filters expired user scopes and returns only scope codes. |
| Service-account model | `services/identity-service/src/diplomat/db/entities/service-account.entity.ts` | Stores service account identity, active flag, optional allowed IPs, audit fields, API keys, and scopes. |
| API-key model | `services/identity-service/src/diplomat/db/entities/api-key.entity.ts` | Stores key hash, secret ARN, last-used metadata, expiry, and revocation timestamp. |
| API-key validation | `services/identity-service/src/controllers/api-key.controller.ts` | Validates format, cache, hash lookup, service-account activity, and returns service scopes. |
| API-key persistence | `services/identity-service/src/diplomat/db/repositories/api-key.repository.ts` | Checks revocation, expiry, account activity, and service scopes. |
| Service accounts seed | `services/identity-service/src/database/seeds/005-service-accounts.seed.ts` | Creates service accounts, assigns scopes, and seeds local development API-key hashes. |
| Identity-local hybrid guard | `services/identity-service/src/common/guards/identity-jwt-auth.guard.ts` | Lets identity validate API keys locally and convert service JWT subjects to service-account payloads. |
| S2S architecture doc | `docs/architecture/service-accounts.md` | Documents service accounts, API-key validation, cache strategy, and S2S usage. |
| User lifecycle ADR | `docs/architecture/ADR-006-user-lifecycle-lazy-expiration.md` | Accepts `statusExpiresAt`, lazy-only expiration at auth touchpoints, session revocation, Cognito disablement, and no per-request status revalidation. |

## Deviations

- `UserScope.contextType` and `UserScope.contextId` are persisted, but the shared `ScopesGuard` only evaluates scope codes in `scopes[]`. Contextual permissions are therefore partial unless individual endpoints add resource-level checks.
- `UserScope.expiresAt` is enforced before token issuance through `UserRepository.findUserScopes`, not by the shared guard after the token has been signed.
- `ServiceAccount.allowedIps` exists on the entity and is described in the architecture doc, but the researched validation path did not show `ApiKeyLogic.isIpAllowed` being called.
- `ADR-006` deliberately leaves already-issued JWTs valid until token expiry; downstream services rely on token expiry rather than per-request lifecycle revalidation.

## Principles

- [[principles/pbac-scopes-in-tokens]] — Generalizes Tangram's token-embedded PBAC scope model.
- [[principles/dual-channel-auth-jwt-and-service-credentials]] — Generalizes Tangram's bearer JWT plus API-key authentication boundary.
- [[principles/service-accounts-for-s2s]] — Generalizes Tangram's service-account and API-key S2S model.

## Related

- [[MOC/security-authz]]
- [[case-studies/tangram/index]]
