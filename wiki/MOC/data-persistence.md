# Data & persistence

Hub for ORM patterns, migrations, lookup tables, audit logs, and content distribution.

## Principles

- [[principles/layered-io-boundaries-diplomat]] - Repository/entity ownership for TypeORM persistence boundaries.
- [[principles/content-distribution-by-channel]] - Lookup-backed channel targeting with content records separated from distribution criteria.
- [[principles/temporal-orchestration-of-content]] - Event windows, release calendars, regeneration guards, and schedule audit/version snapshots.
- [[principles/timed-session-resume]] - Session persistence fields and event rows for resumable timed work.
- [[principles/wallet-ledger-style-balances]] - Balance snapshots paired with transaction-ledger persistence.

## Case studies

- [[case-studies/tangram/diplomat-architecture]] - TypeORM repositories and entities as the standard persistence boundary.
- [[case-studies/tangram/catalog-and-learning]] - Tangram Catalog distribution, release schedules, lookups, and Learning session persistence.
- [[case-studies/tangram/rewards-ranking-cache]] - Wallet transactions, serialized balance mutations, ranking visibility cache fallback, and raw-query deviation.
- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] - Webhook event idempotency rows, payment transactions, and queue-backed state changes.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
