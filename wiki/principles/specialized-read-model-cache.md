# Specialized Read-Model Cache

**When to use:** Use this pattern when an expensive, high-traffic read can be served from a bounded, periodically rebuilt projection instead of recomputing from write tables on every request.

## Body

A specialized read-model cache is a projection, not a transparent key-value shortcut. Design it around one expensive read shape: the scope keys, payload schema, refresh cadence, and fallback behavior should all be explicit.

Give one background owner responsibility for rebuilding the projection. Request handlers should read the projection and return a predictable "not ready" or "updating" response when it is missing, rather than running the heavy source query themselves. If a request path is allowed to recompute the full population, the cache stops protecting the database during cold starts and traffic spikes.

Split payloads by access pattern. A list view can use a compact summary or top-N document, while a "my position" view can use a direct lookup keyed by subject id. Store projection metadata with the read model: computed time, next expected refresh time, source period or window, total population, and a cache key version.

Use short operation timeouts, bounded TTLs, and expiring locks. A refresh lock prevents multiple workers from rebuilding the same scope at the same time. A separate single-flight lock can let one caller trigger a recovery path while other callers fail fast. Locks must self-expire; release failure should be tolerable.

Add guardrail tests that assert write paths, scoring paths, and normal read handlers do not import the cache service as a recomputation dependency or call the heavy source queries. The read model should have one rebuild entry point that is easy to find and easy to review.

## Trade-offs

- Expensive reads become predictable and cheap during normal traffic.
- A projection schema can be shaped exactly for user-facing read paths.
- Refresh ownership and guardrails reduce accidental database stampedes.
- Results are eventually consistent within the refresh cadence and TTL.
- Operators now own cache warmup, lock tuning, stale-response behavior, and projection observability.
- Cold or missing projections require a product decision: fail fast, show "updating", or allow a controlled recovery path.

## Anti-patterns

- Letting every request recompute the projection on a miss.
- Treating the cache as generic infrastructure without documenting the read-model schema and source query.
- Using one payload shape for list views and per-user position lookups when their access patterns differ.
- Allowing scoring, award, or write paths to depend on cache reads.
- Using locks without expirations or refresh loops that can overlap indefinitely.
- Hiding stale or missing projection behavior behind silent fallbacks to slow source queries.

## Checklist for a new project

- [ ] Name the exact read shape and source query the projection replaces.
- [ ] Define scope keys, key versioning, payload schema, metadata fields, TTL, and refresh cadence.
- [ ] Make one background owner responsible for full-population rebuilds.
- [ ] Split list and direct-lookup payloads when they have different access patterns.
- [ ] Add expiring refresh locks and short cache-operation timeouts.
- [ ] Define the cold-miss response contract before launch.
- [ ] Add guardrail tests that keep write/calculation paths away from projection recomputation.
- [ ] Monitor refresh duration, empty target sets, stale projections, lock contention, and parse/read failures.

## Case studies

- [[MOC/async-scale]] - Evidence and implementation examples for specialized read-model caches.
- [[MOC/product-domain]] - Product-domain examples where user-facing ranking or progress views need bounded read latency.

## Related

- [[principles/bulk-import-via-command-queues]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
