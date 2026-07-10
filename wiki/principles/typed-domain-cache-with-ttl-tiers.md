# Typed Domain Cache with TTL Tiers

**When to use:** Cache frequently read domain objects (catalogs, lookups, eligibility) with per-type TTLs, optional process-local memory, and explicit invalidation—not only specialized ranking read models.

## Body

Expose a cache service with **typed getters/setters** for each cached shape (trail, question, lookup set, daily quote, and so on). Configure a **TTL per type** from configuration defaults, not a single global expiry.

Use a key prefix per bounded context. Prefer Redis (or equivalent) as the shared store. Optionally keep a small in-process memory map for ultra-hot keys, always bounded and short-lived.

Provide **invalidate** methods for write paths so editors do not wait for TTL alone. On cache errors, fail soft: log and fall through to the database rather than failing the request.

This pattern differs from a typed domain object cache (per-type TTL get/set/invalidate for authoritative snapshots such as catalog trails and lookups). A specialized read-model cache rebuilds an expensive projection on a cadence; a typed domain cache amplifies ordinary repository reads. Use both when the product has both ranking-style projections and hot reference graphs.

## Trade-offs

- Large reduction in repetitive DB reads for stable reference and content graphs.
- Stale reads until TTL or explicit invalidation; writers must remember to invalidate.
- Dual Redis + memory layers add complexity and consistency subtleties across instances.

## Anti-patterns

- One undifferentiated `cache.set(key, value)` bag with no typed API or TTL policy.
- Treating cache miss or Redis outage as a hard 500.
- Caching user-specific secrets or authorization decisions without careful key design.
- Assuming a ranking/read-model refresher is the only legitimate Redis use.

## Checklist for a new project

- [ ] List cacheable domain types and assign TTLs.
- [ ] Implement typed get/set/invalidate with a context key prefix.
- [ ] Decide whether an L1 memory cache is justified.
- [ ] Wire invalidation into create/update/delete paths.
- [ ] Define fail-open behavior when the cache store is down.

## Case studies

- [[MOC/async-scale]] — Domain object caching alongside specialized read models.
- [[MOC/data-persistence]] — Lookup and content caching.

## Related

- [[principles/specialized-read-model-cache]]
- [[principles/content-distribution-by-channel]]
- [[MOC/async-scale]]
- [[MOC/data-persistence]]
