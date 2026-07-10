# Rewards Ranking Cache and Wallet Ledger (Tangram)

**When to use:** Read this case study when you need the concrete Tangram Rewards implementation behind Redis-backed olympiad ranking reads and wallet/prize balance mutations.

## Body

Tangram's Rewards service combines two product-domain patterns: a specialized read-model cache for olympiad rankings and a ledger-style wallet for Tangrans balances and prizes.

The ranking cache is intentionally narrow. `RankingCacheService` owns the full-population olympiad individual ranking recompute, builds two Redis payloads per `(editionId, periodId, levelId)` tuple, and exposes only `getLeaderboard`, `getPosition`, and `getMeta` reads. The leaderboard key stores top-N entries plus metadata such as `computedAt`, `nextRefreshAt`, `accrualKey`, period dates, and total population. The position key stores a hash from enrollment id to the student's exact position and score fields, so a user outside the top-N list can still see their own rank without scanning the leaderboard.

`RankingCacheRefresher` owns warming. On module init it registers an unref'ed interval from `ranking-cache.config.ts`, lists active olympiad ranking targets, acquires a tuple-scoped Redis lock, loads the active period, and calls `cache.refresh`. It catches per-tuple failures so one bad tuple does not stop the refresh loop, warns on overlapping ticks, logs slow tuple refreshes, and emits aggregate tick completion metrics. The cache service also has single-flight and refresh locks with TTLs, one-second Redis operation timeouts, parse-failure logging, and miss-style degradation when Redis is unavailable.

The request path uses this projection only for active olympiad period reads. `RankingController.getIndividualRanking` resolves the current olympiad edition and level, checks that the requested month overlaps the active period, reads the cached leaderboard, and optionally reads the current user's cached position when they are outside the top-N set. Cache misses call the service-unavailable path instead of recomputing the full population in the request. Historical and accumulated reads deliberately fall through to direct repository queries because they are not the active warmed projection.

Visibility controls use a separate Redis read model. `RankingVisibilityCacheService` materializes active hidden ranking scopes into a Redis set, keeps a short in-memory set for hot reads, falls back to `RankingVisibilityRepository.existsActiveScopeKey` when Redis reads fail, and periodically rebuilds from the database using a temporary key plus rename. Failed materialize/release operations are queued in memory and retried after a rebuild.

The wallet domain uses a denormalized `wallets.balance` for fast reads while recording every mutation in `transactions`. `WalletRepository.createTransactionWithBalanceUpdate` runs in a `SERIALIZABLE` transaction, pessimistically locks the wallet row, calculates `newBalance`, inserts a transaction with `balanceAfter`, and updates the wallet balance before commit. `createWithInitialBalance` follows the same rule by inserting an `init` transaction when the starting balance is non-zero.

Wallet and prize controllers orchestrate product rules around that repository boundary. `WalletController` validates enrollment ids, lazily creates the default Tangrans wallet on balance reads, returns statements from transactions by month, and exposes helpers for phase earnings. `PrizeController` manages giftcard preferences and award status transitions. `PrizeDistributionController` validates ranking-period/team inputs, prevents duplicate distributions, filters team members by ranking enrollment type, and credits team prizes by creating wallet transactions with `sourceType = "ranking_prize"` and `eligibleForRanking = false`.

## Trade-offs

- Tangram avoids repeated full-population olympiad ranking queries on active ranking screens.
- Redis leaderboard and position payloads are shaped around the exact frontend reads instead of generic cache entries.
- Guardrail tests make the cache isolation rule explicit: calculation and award paths must not depend on cache reads or hidden recomputation.
- Wallet balance reads are cheap while transactions preserve statement, audit, and ranking-eligibility context.
- Ranking reads are eventually consistent with the refresh interval and can return an updating response when the projection is cold.
- The cache adds operational tuning: refresh interval, Redis TTL, lock TTL, key versions, slow tuple logs, and rebuild health.
- Wallet correctness depends on all balance-changing paths using the centralized serializable mutation API.

## Anti-patterns

- Tangram avoids letting normal active olympiad read requests recompute `findOlympiadIndividualRankingByLevelWithZeroPoints`; the cache service is the only intended full-population recompute owner.
- Tangram avoids loading every student's position from the leaderboard document; the per-enrollment Redis hash is a separate access path.
- Tangram avoids using Redis as the source of truth for ranking visibility; Redis and memory speed reads, while the database remains the fallback and rebuild source.
- Tangram avoids direct wallet balance edits by route handlers; balance changes go through repository transactions that also write ledger rows.
- A current risk is log wording in prize distribution that includes enrollment and wallet identifiers; future audit/log policy should confirm whether those identifiers are acceptable operational metadata.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Cache config | `services/rewards-service/src/config/ranking-cache.config.ts` | Defines refresh interval, lock TTL, Redis TTL, top-N size, and cache key version from environment with defaults. |
| Ranking cache service | `services/rewards-service/src/services/ranking-cache.service.ts` | Builds `:lb` and `:pos` Redis read models, owns full-population recompute, chunks large HSET writes, wraps Redis reads with timeouts, and implements single-flight/refresh locks. |
| Cache refresher | `services/rewards-service/src/services/ranking-cache.refresher.ts` | Registers the interval worker, discovers active olympiad targets, serializes tuple refreshes through locks, catches tuple failures, and logs slow refreshes. |
| Ranking controller | `services/rewards-service/src/controllers/ranking.controller.ts` | Serves active olympiad individual ranking reads from cache, reads current-user position from the position hash, and falls through to direct DB reads for historical/accumulated paths. |
| Visibility cache | `services/rewards-service/src/services/ranking-visibility-cache.service.ts` | Maintains Redis and short-lived memory caches for hidden ranking scopes, falls back to DB reads, and rebuilds from database via temp-key rename. |
| Cache guardrail tests | `services/rewards-service/test/unit/guardrail/ranking-cache-isolation.spec.ts` | Static and runtime tests assert calculation paths do not import cache services or call heavy olympiad ranking reads on cache-backed reads. |
| Cache service tests | `services/rewards-service/test/unit/services/ranking-cache.service.spec.ts` | Verifies leaderboard/position payloads, TTLs, single-flight exclusivity, Redis-failure degradation, refresh locks, and large-population HSET chunking. |
| Visibility cache tests | `services/rewards-service/test/unit/services/ranking-visibility-cache.service.spec.ts` | Verifies Redis set reads/writes, DB fallback, memory cache behavior, temp-key rebuilds, and pending retry behavior. |
| Wallet entity | `services/rewards-service/src/diplomat/db/entities/wallet.entity.ts` | Stores enrollment, wallet type, balance, audit columns, soft delete, and the unique active wallet per enrollment/type. |
| Transaction entity | `services/rewards-service/src/diplomat/db/entities/transaction.entity.ts` | Records wallet mutations with type, amount, `balanceAfter`, source fields, ranking eligibility, period id, release/answer dates, and metadata. |
| Wallet repository | `services/rewards-service/src/diplomat/db/repositories/wallet.repository.ts` | Creates wallets, inserts initialization transactions, and centralizes serializable balance mutation with pessimistic wallet locking. |
| Transaction repository | `services/rewards-service/src/diplomat/db/repositories/transaction.repository.ts` | Provides bounded statement reads and period/phase/ranking aggregation queries from transaction rows. |
| Wallet controller | `services/rewards-service/src/controllers/wallet.controller.ts` | Validates ids, lazily creates default Tangrans wallets, reads balances/statements, and delegates balance mutations to repositories. |
| Wallet mutation tests | `services/rewards-service/test/unit/diplomat/db/repositories/wallet.repository.transaction.spec.ts` | Verifies a wallet mutation locks the row, inserts a transaction, updates balance, uses `SERIALIZABLE`, and throws when the wallet is missing. |
| Prize entity | `services/rewards-service/src/diplomat/db/entities/prize.entity.ts` | Models active prizes, giftcard/physical/virtual categories, stock/value fields, awards, preferences, and audit/soft-delete fields. |
| Prize controller | `services/rewards-service/src/controllers/prize.controller.ts` | Manages giftcard lookup, preferences, suggested awards, and award status transitions. |
| Prize distribution controller | `services/rewards-service/src/controllers/prize-distribution.controller.ts` | Distributes team and individual prizes, prevents duplicate distributions, filters team members by enrollment type, and credits team prizes through wallet transactions. |
| Prize repository | `services/rewards-service/src/diplomat/db/repositories/prize.repository.ts` | Stores prizes, awards, preferences, status updates, soft deletion, and giftcard lookups. |

## Deviations

- The ranking cache lives under `src/services/`, not `src/diplomat/cache/`. This is an intentional service-level deviation from the generic Diplomat cache boundary documented elsewhere in the wiki.
- `RankingController` still imports `RankingCacheService` directly for active olympiad reads. This keeps the read path explicit, but it means controller-level guardrail tests are important to prevent accidental recomputation behavior from creeping into calculation or award paths.
- `PrizeDistributionController.getTeamMembers` uses a raw SQL query with positional parameters. It is parameterized and tied to enrollment schema joins, but it sits in the controller rather than a repository adapter.

## Principles

- [[principles/specialized-read-model-cache]] - Generalizes Tangram's active olympiad ranking projection, refresh locks, cold-miss behavior, and guardrail tests.
- [[principles/wallet-ledger-style-balances]] - Generalizes Tangram's current-balance plus transaction-ledger wallet model.

## Related

- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]]
- [[case-studies/tangram/diplomat-architecture]]
- [[case-studies/tangram/index]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
