# Diplomat Architecture (Tangram)

**When to use:** Read this case study when you need the concrete Tangram implementation behind layered service boundaries, pure logic, and the known async/cache deviations.

## Body

Tangram documents "Diplomat" as its service architecture pattern: HTTP handlers live under `diplomat/http-in`, controllers orchestrate use cases, logic files hold pure business rules, repositories and entities own TypeORM persistence, cache adapters live under `diplomat/cache`, adapters transform shapes, and `wire/in` plus `wire/out` define request and response contracts.

The standard service flow is explicit in `docs/SERVICE_STANDARDS.md` and `.cursor/rules/nestjs-architecture.mdc`: request input moves from HTTP into a controller, the controller gathers state, calls logic, then performs effects through repositories or external clients, and the HTTP boundary returns a response contract. The same docs call this controller shape the "logic sandwich."

The Catalog schedule flow is a representative aligned implementation. `ScheduleHttp` handles NestJS routing, auth decorators, DTO input, and response shaping. `ScheduleController` validates IDs, loads distribution and schedule records, invokes `ScheduleLogic.generateScheduleItems`, persists schedule rows, and records audit/version effects. `ScheduleLogic` calculates release items from plain phase data and dates. `ScheduleRepository` owns TypeORM queries, joins, updates, optimistic version checks, and mapping from entities to schedule result objects. `schedule.dto.ts` and `schedule.response.ts` define the wire contracts at the boundary.

Tangram also extends the pattern for workloads that do not fit a simple HTTP-to-repository path. Enrollment adds `diplomat/queue` producers and consumers for SQS-backed olympiad import commands. Learning has a `worker/xlsx` area for streaming VC import spreadsheets into validated chunks while still calling `VcImportLogic` for row rules. Rewards keeps a specialized olympiad ranking read-model cache under `src/services/ranking-cache*`, where refresh timers, Redis keys, locks, and full-population reads are specific enough that they sit outside the generic `diplomat/cache` boundary.

## Trade-offs

- Tangram gets a common mental model across services: HTTP is thin, controllers orchestrate, logic stays easy to unit test, and repositories hide persistence details.
- The structure makes security and validation review easier because inbound DTOs, guards, repositories, and response contracts have predictable homes.
- Async imports and ranking caches need exceptions because queue consumers, streaming workers, and precomputed read models do not map cleanly to the base HTTP/db/cache table.
- Some features trade strict adapter separation for local response mapping when the transformation is mechanical.

## Anti-patterns

- Tangram avoids letting most HTTP handlers become business services; the Catalog schedule handler routes to `ScheduleController` and returns response shapes.
- Tangram avoids putting heavy release-date generation in persistence code; `ScheduleLogic` owns schedule item calculation.
- A current risk is treating every background worker as an ordinary controller path, because queue visibility, retries, shutdown, and idempotency need explicit worker behavior.
- A current risk is creating one-off `src/services/*` helpers without documenting why they are not `diplomat/cache`, `diplomat/db`, or a controller dependency.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Service standard | `docs/SERVICE_STANDARDS.md` | Defines Diplomat architecture, data flow, layer responsibilities, folder structure, pure logic, controller logic sandwich, repositories, cache, and testing expectations. |
| Cursor architecture rule | `.cursor/rules/nestjs-architecture.mdc` | Encodes layer access rules: `diplomat/http-in`, repositories, entities, cache, controllers, logic, adapters, wire contracts, and models. |
| HTTP boundary | `services/catalog-service/src/diplomat/http-in/schedule.http.ts` | `ScheduleHttp` handles route decorators, DTO input, authorization scopes, and response shaping before/after controller calls. |
| Controller orchestration | `services/catalog-service/src/controllers/schedule.controller.ts` | `ScheduleController` gathers distribution and schedule state, calls `ScheduleLogic`, persists rows, and records audit/version effects. |
| Pure schedule rules | `services/catalog-service/src/logic/schedule.logic.ts` | `ScheduleLogic` derives release schedule items from phases, dates, and frequency without repository or transport dependencies. |
| Persistence boundary | `services/catalog-service/src/diplomat/db/repositories/schedule.repository.ts` | `ScheduleRepository` owns TypeORM reads, writes, relations, optimistic locking, and entity-to-result mapping. |
| Wire contracts | `services/catalog-service/src/wire/in/schedule.dto.ts` and `services/catalog-service/src/wire/out/schedule.response.ts` | Input DTOs and output response classes define the boundary shapes used by `ScheduleHttp`. |
| Queue deviation | `services/enrollment-service/src/diplomat/queue/producers/olympiad-import.producer.ts` and `services/enrollment-service/src/diplomat/queue/consumers/olympiad-import.consumer.ts` | Enrollment adds a Diplomat queue boundary for SQS producers/consumers and worker loops. |
| Worker deviation | `services/learning-service/src/worker/xlsx/vc-xlsx-stream-reader.ts` | Learning streams VC import spreadsheets from `worker/xlsx`, chunks rows, and delegates row validation to `VcImportLogic`. |
| Cache deviation | `services/rewards-service/src/services/ranking-cache.service.ts` and `services/rewards-service/src/services/ranking-cache.refresher.ts` | Rewards keeps specialized ranking read-model cache refresh, locks, Redis keys, and timers outside `diplomat/cache`. |

## Deviations

- Enrollment extends the Diplomat boundary with `diplomat/queue` for SQS producers and long-running consumers. This is still an I/O boundary, but it is not part of the base `http-in`, `db`, and `cache` table in the standards docs.
- Learning places VC spreadsheet streaming code under `src/worker/xlsx` rather than `diplomat/*`. The worker is not an HTTP or database adapter; it reads workbook streams, builds chunks, and calls `VcImportLogic` for row validation.
- Rewards keeps olympiad ranking cache behavior in `src/services/ranking-cache*` rather than `diplomat/cache`. The code is a specialized read-model warmer with Redis locks, periodic refresh, and full-population repository reads, not a generic cache adapter.

## Principles

- [[principles/layered-io-boundaries-diplomat]] - Generalizes Tangram's Diplomat layer boundaries into a generic layered I/O boundary pattern.
- [[principles/pure-domain-logic-no-io]] - Generalizes Tangram's logic layer rule that business decisions should not perform I/O.

## Related

- [[case-studies/tangram/identity-pbac-and-auth]]
- [[case-studies/tangram/index]]
- [[MOC/architecture]]
