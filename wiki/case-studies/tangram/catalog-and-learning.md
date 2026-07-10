# Catalog And Learning Sessions (Tangram)

**When to use:** Read this case study when you need the concrete Tangram implementation behind catalog distribution, release calendars, resumable challenge sessions, and Learning XLSX evaluation imports.

## Body

Tangram's Catalog and Learning services split product ownership along a clear boundary. Catalog owns content availability: lookup tables, trail distribution, challenge seasonal windows, release schedules, schedule audit/version history, and eligibility discovery. Learning owns learner interaction state: session lifecycle, answer rows, session events, timed resume, and imported evaluations for user-generated submissions.

Catalog models multi-channel distribution with a base distribution row plus channel-specific tables. `ChallengeSeasonalDistributionRepository.replaceForEvent` writes a base `challenge_seasonal_distributions` row keyed by enrollment type, then writes the criteria row for B2C, school, olympiad, or corporate contexts. The trail distribution tables use the same base-plus-criteria shape for curriculum trail access. This keeps channel targeting separate from the content and time-window records.

Temporal orchestration appears in two Catalog shapes. `ChallengeSeasonal` stores reveal/open/close/finish timestamps, active flag, participation policy, preconditions, and theme options. `ChallengeSeasonalRepository.getEventState` derives `UPCOMING`, `ACTIVE`, `CLOSED`, or `FINISHED` from those timestamps, while discovery orders eligible events by state and open date. Release schedules handle longer curriculum calendars: `ScheduleLogic` generates daily, weekly, biweekly, all-at-once, and manual schedules; `ScheduleController` can regenerate, preview, bulk shift, detect drift, suspend conflicting additions when students already have progress, and write audit/version snapshots.

Lookups are intentionally simple and cached. `LookupsHttp` exposes public read endpoints for phase types, challenge types, question types, difficulty levels, blank types, investment view types, and lesson-plan visibility. Each endpoint reads a short key from `CacheService`, falls back to TypeORM repositories, stores the result, and returns stable lookup data to clients and generated contracts.

Learning's session engine makes `POST /sessions/start` idempotent. `ChallengeSessionController.startSession` first fetches challenge metadata, validates seasonal state when needed, resolves a `challengeDate` for daily participation, and looks up an existing session by enrollment, challenge order, and optional policy date. Completed sessions conflict. In-progress or abandoned sessions with remaining time are returned instead of recreated, and abandoned sessions can be moved back to in-progress.

Timed resume uses persisted active-time fields, not only `startedAt`. `ChallengeSession` stores `elapsedTimeSeconds`, `lastResumedAt`, `pausedAt`, `pausedTimeSeconds`, `timeLimitSeconds`, `isPaused`, and `isStoppable`. `SessionLogic.calculateTimeRemaining` derives remaining time from elapsed time plus the current active run. Pause adds active seconds and clears `lastResumedAt`; resume adds paused duration and sets `lastResumedAt`; abandon flushes active seconds before marking the session abandoned. `SessionEvent` records start, pause, resume, complete, abandon, answer-submitted, and auto-complete events.

Learning imports VC evaluation spreadsheets with a streaming chunk contract. `VcImportHttp` enforces multipart upload and file-size limits; `VcImportController` validates MIME type; `VcImportSyncService` streams rows from the uploaded buffer, maintains cumulative counts, and calls `VcImportChunkPersistService` per chunk. The XLSX reader validates headers and row structure, detects duplicate submission ids, yields chunk indexes and checkpoint row numbers, and falls back to a buffered workbook read only under a hard in-memory ceiling. Chunk persistence runs in a transaction, resolves submissions and challenge types, rejects out-of-scope or non-BeCreator rows, creates missing submission versions, upserts draft evaluations, upserts selection rows, and returns row-level errors.

Submission evaluation stores imports as drafts before release. `SubmissionEvaluationRepository.upsertDraftBySubmissionId` calculates media percent and Tangrans from the four rubric scores, updates an active draft if it exists, or creates one with an idempotency key and `source = "bulk"`. Release methods switch matching drafts to `released`, set release/publish timestamps, and mark evaluations as counting for ranking.

## Trade-offs

- Tangram keeps Catalog time/distribution ownership separate from Learning session state, reducing pressure to overload trail or session tables with every product rule.
- Lookup-backed distribution and release schedules are operationally inspectable and cacheable.
- Learning start/resume avoids duplicate sessions and preserves answers after reloads or abandon/reentry.
- XLSX imports can process many rows and return row-level errors without one giant transaction.
- Catalog and Learning still have synchronous coupling for seasonal eligibility, participation policy, challenge metadata, and precondition checks.
- Release schedule regeneration and drift handling add significant controller complexity and cross-schema progress queries.
- The synchronous VC import path is chunked but still request-bound; very large imports may need promotion to a background job.

## Anti-patterns

- Tangram avoids binding seasonal challenge windows directly into trail progression; ADR-001 explicitly separates temporal event orchestration from trail content.
- Tangram avoids treating `ABANDONED` as a terminal lock for timed sessions when remaining time exists; ADR-003 and ADR-004 make resume part of the unified session engine.
- Tangram avoids passing full spreadsheet state into a single database transaction; the import path parses and persists bounded chunks.
- Current risk: several Catalog scheduling methods query Learning and Enrollment schemas directly from `ScheduleController`; those reads are parameterized, but they blur Diplomat repository boundaries and should be watched if schedule logic grows.
- Current risk: VC import names and logs can include filenames and submission identifiers; operational log policy should confirm whether those identifiers are acceptable.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Seasonal ADR | `docs/architecture/ADR-001-challenge-seasonal-temporal-orchestration.md` | Documents Catalog ownership of temporal orchestration, distribution by enrollment type, eligibility, and Learning participation enforcement. |
| Session resume ADR | `docs/architecture/ADR-003-session-resume-time-is-money.md` | Documents idempotent start, backend remaining time, abandoned-session resume, and active-time fields. |
| Unified challenge engine ADR | `docs/architecture/ADR-004-challenge-engine.md` | Documents the single session model, pause/resume/abandon transitions, session events, backend timing, and scalability notes. |
| Catalog audit ADR | `docs/architecture/ADR-005-catalog-audit-system-evolution.md` | Documents Catalog audit evolution, schedule audit legacy, and future event-driven audit direction. |
| Seasonal entity | `services/catalog-service/src/diplomat/db/entities/challenge-seasonal.entity.ts` | Stores reveal/open/close/finish windows, theme options, preconditions, participation policy, and active flag. |
| Seasonal repository | `services/catalog-service/src/diplomat/db/repositories/challenge-seasonal.repository.ts` | Computes event state, discovers events by distributed ids, and keeps hot challenge-order lookup join-free. |
| Seasonal logic | `services/catalog-service/src/logic/challenge-seasonal.logic.ts` | Validates ordered windows, distribution criteria, participation policy integration, and completion preconditions. |
| Seasonal controller | `services/catalog-service/src/controllers/challenge-seasonal.controller.ts` | Creates, lists, updates, deletes, and evaluates eligibility for seasonal events. |
| Seasonal distribution repository | `services/catalog-service/src/diplomat/db/repositories/challenge-seasonal-distribution.repository.ts` | Replaces event distributions transactionally and discovers event ids by channel criteria. |
| Seasonal distribution entities | `services/catalog-service/src/diplomat/db/entities/challenge-seasonal-distribution.entity.ts` | Base distribution row keyed by event and enrollment type. |
| Trail distribution entities | `services/catalog-service/src/diplomat/db/entities/trail-distribution.entity.ts` | Base trail distribution row keyed by trail and enrollment type. |
| Release schedule entities | `services/catalog-service/src/diplomat/db/entities/release-schedule.entity.ts` | Stores distribution, organization/edition context, start date, frequency, version, and audit columns. |
| Release item entities | `services/catalog-service/src/diplomat/db/entities/release-schedule-item.entity.ts` | Stores phase/challenge release dates and manual override flags. |
| Schedule logic | `services/catalog-service/src/logic/schedule.logic.ts` | Generates daily, weekly, biweekly, all-at-once, manual, and override-preserving schedules. |
| Schedule controller | `services/catalog-service/src/controllers/schedule.controller.ts` | Creates, updates, regenerates, bulk-shifts, audits, versions, detects drift, and syncs schedules. |
| Lookup endpoints | `services/catalog-service/src/diplomat/http-in/lookups.http.ts` | Public cached lookup endpoints for stable catalog reference data. |
| Session entity | `services/learning-service/src/diplomat/db/entities/challenge-session.entity.ts` | Stores session key fields, challenge date, status, elapsed time, pause state, and time limit. |
| Session events | `services/learning-service/src/diplomat/db/entities/session-event.entity.ts` | Stores lifecycle events and metadata by session. |
| Session logic | `services/learning-service/src/logic/session.logic.ts` | Validates state transitions and computes active duration, remaining time, pause duration, and timeout buffers. |
| Session repository | `services/learning-service/src/diplomat/db/repositories/challenge-session.repository.ts` | Creates sessions with `lastResumedAt`, finds sessions by policy date, and updates pause/resume/status fields. |
| Session controller | `services/learning-service/src/controllers/challenge-session.controller.ts` | Implements idempotent start, seasonal validation, resume, pause, complete, abandon, and event writes. |
| XLSX reader | `services/learning-service/src/worker/xlsx/vc-xlsx-stream-reader.ts` | Streams workbook rows into validated chunks and falls back to buffered reads under a memory cap. |
| VC import logic | `services/learning-service/src/logic/vc-import.logic.ts` | Validates MIME types, UUIDs, duplicate submissions, rubric score ranges, elimination values, and required feedback. |
| VC import HTTP | `services/learning-service/src/diplomat/http-in/vc-import.http.ts` | Defines the sync spreadsheet upload endpoint and file-size validator. |
| VC import controller | `services/learning-service/src/controllers/vc-import.controller.ts` | Validates file size/content type and delegates to the sync import service. |
| VC import sync service | `services/learning-service/src/controllers/vc-import-sync.service.ts` | Streams chunks, accumulates counts/errors, and logs completion. |
| VC chunk persistence | `services/learning-service/src/controllers/vc-import-chunk-persist.service.ts` | Validates database scope and persists draft evaluations plus selection rows in chunk transactions. |
| Evaluation entity | `services/learning-service/src/diplomat/db/entities/submission-evaluation.entity.ts` | Stores rubric scores, draft/released status, source, ranking flag, timestamps, and idempotency keys. |
| Evaluation repository | `services/learning-service/src/diplomat/db/repositories/submission-evaluation.repository.ts` | Upserts drafts, resolves latest evaluations, and releases drafts by submission or scope. |
| Import config | `services/learning-service/src/config/vc-import-worker.config.ts` | Defines sync max file size and bounded chunk-size parsing. |
| Import tests | `services/learning-service/test/unit/controllers/vc-import-sync.service.spec.ts` | Verifies chunk aggregation, full error reporting beyond the former cap, parse errors, and actor propagation. |
| Session tests | `services/learning-service/test/integration/challenge-session.integration-spec.ts` | Verifies start, existing-session return, and completed-session conflicts. |

## Deviations

- `ChallengeSeasonalLogic` performs I/O and external Learning calls despite living under `src/logic`; it behaves more like an orchestration service than pure domain logic.
- `ScheduleController` contains substantial regeneration, drift, conflict, and cross-schema SQL behavior; this is pragmatic but heavier than the usual controller orchestration layer.
- `VcImportChunkPersistService` lives under `src/controllers/` even though it is a worker-like persistence service.
- `ADR-005` is still proposed, so the current Catalog audit implementation and the future event-driven audit direction are not the same thing.

## Principles

- [[principles/content-distribution-by-channel]] - Generalizes Tangram's base-plus-channel criteria tables for seasonal and trail distribution.
- [[principles/temporal-orchestration-of-content]] - Generalizes Tangram's event windows, release schedules, regeneration previews, and schedule audit/version snapshots.
- [[principles/timed-session-resume]] - Generalizes Tangram's idempotent start, active-time persistence, abandoned-session resume, and session event trail.
- [[principles/streaming-bulk-file-import-workers]] - Generalizes Tangram's VC XLSX chunk reader, chunk transaction persistence, draft evaluation upserts, and row-level errors.

## Related

- [[case-studies/tangram/diplomat-architecture]]
- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]]
- [[case-studies/tangram/rewards-ranking-cache]]
- [[case-studies/tangram/index]]
- [[MOC/data-persistence]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
