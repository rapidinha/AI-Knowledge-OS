# Data & persistence

Hub for ORM patterns, migrations, lookup tables, audit logs, and content distribution.

## Principles

- [[principles/layered-io-boundaries-diplomat]] - Repository/entity ownership for TypeORM persistence boundaries.
- [[principles/content-distribution-by-channel]] - Lookup-backed channel targeting with content records separated from distribution criteria.
- [[principles/temporal-orchestration-of-content]] - Event windows, release calendars, regeneration guards, and schedule audit/version snapshots.
- [[principles/timed-session-resume]] - Session persistence fields and event rows for resumable timed work.
- [[principles/wallet-ledger-style-balances]] - Balance snapshots paired with transaction-ledger persistence.
- [[principles/soft-delete-with-actor-audit]] - Soft delete with deletion timestamp and actor attribution.
- [[principles/typed-domain-cache-with-ttl-tiers]] - Domain snapshot caching with TTL tiers (complements specialized read models).

## Related

- [[index]]
- [[_meta/coverage-matrix]]
