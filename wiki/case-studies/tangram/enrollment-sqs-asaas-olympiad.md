# Enrollment SQS, Asaas, and Olympiad Imports (Tangram)

**When to use:** Read this case study when you need the concrete Tangram implementation behind SQS-backed payment webhooks and olympiad import workers in Enrollment.

## Body

Tangram's Enrollment service uses `diplomat/queue` as an async I/O boundary for two related workloads: Asaas payment webhooks and olympiad enrollment imports. Both avoid doing all work in the original HTTP request. The payment path turns provider webhooks into SQS commands, while the import path turns user-initiated work into bootstrap, orchestration, and chunk-processing commands.

The Asaas webhook flow starts in `AsaasWebhookIngestService`. It accepts unknown request bodies, verifies the configured webhook token from provider headers, checks that the body is object-shaped, adds a correlation id and received timestamp, then publishes an `AsaasWebhookCommand` through `AsaasWebhookQueueService`. The producer serializes the command body and attaches event type, correlation id, and provider event id as SQS message attributes.

`AsaasWebhookConsumerService` owns the worker loop. It long-polls SQS, parses each message, claims or inserts a `webhook_events` row by `asaas_event_id`, treats already processed events as duplicates to delete, leaves currently leased events in the queue, and starts a processing lease for claimed work. While the processor runs, the consumer renews both the database lease and the SQS visibility timeout. It marks the event processed and deletes the queue message only after `AsaasWebhookProcessorService` succeeds; failures are marked in the event row and left for retry behavior.

The processor applies payment and subscription state changes through TypeORM transactions. It maps payment statuses, updates access states, handles membership and B2C provisioning side effects, and guards against out-of-order provider events by comparing `lastAsaasEventCreatedAt` before applying transitions. The ADR documents the intent: immediate webhook acknowledgement, idempotency via `asaas_event_id`, auditability in `WebhookEvent`, async reliability through SQS and retry/DLQ behavior, and local parity through Localstack.

The olympiad import flow uses the same queue boundary for bulk work. `OlympiadController` creates an import job, saves large request context in `OlympiadImportPayloadCacheService` with Redis TTL, then enqueues a bootstrap command. Bootstrap prepares the job and enqueues chunk commands for plan-annual imports. External-school imports add an orchestrator queue: the orchestrator groups school items, chunks each group, then enqueues external-student chunk commands. `OlympiadImportConsumer` runs separate worker loops for the plan-annual, external-orchestrator, and external-student queues, parses command types, validates required fields, dispatches to controller command handlers, deletes messages after success, and leaves failed messages for visibility-timeout retry.

`SqsConfigService` centralizes queue URL, endpoint, credential, and local endpoint normalization. `assertOlympiadSqsRuntimeSafe` adds a production guard: olympiad producers and consumers must not run against missing or Localstack queue URLs unless local defaults are explicitly allowed. Demo provisioning is a useful contrast: `DemoProvisioningService` orchestrates identity, organization, enrollment, and notification adapters synchronously around a demo lead status, so it reinforces the "orchestrator coordinates effects" shape without being the queue-backed async path.

## Trade-offs

- Tangram gets fast webhook acknowledgement while preserving idempotent, retryable payment state updates.
- SQS workers make high-volume imports chunkable and horizontally scalable without holding HTTP requests open.
- Redis payload caching keeps olympiad import queue messages below SQS payload limits.
- The design adds several operational surfaces: queue URLs, worker enablement, lease timing, Redis TTL, stuck job detection, and dead-letter handling.
- Import command routing remains controller-heavy because `OlympiadController` owns both HTTP use cases and command use cases.

## Anti-patterns

- Tangram avoids mutating payment/subscription state directly in the webhook ingestion service; ingestion only authenticates, shapes, and enqueues.
- Tangram avoids assuming Asaas redelivers exactly once; `webhook_events` and aggregate timestamps make duplicate and stale events harmless.
- Tangram avoids putting full olympiad import payloads in SQS messages; the queue carries import ids, chunk indexes, and command metadata.
- A current risk is reading queue behavior from the ADR alone, because the service code contains later details such as lease renewal, Redis payload caching, and production Localstack guards.
- A current risk is treating the requested terraform-v2 queue modules as source evidence from this monorepo branch; those paths were not available in `tangram-platform` `origin/main` during this extraction.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Payment ADR | `docs/architecture/ADR-002-asaas-b2c-payment-integration.md` | Documents webhook goals, idempotency, SQS decoupling, retry/DLQ intent, audit trail, Localstack parity, and the HTTP-to-SQS-to-worker shape. |
| Webhook setup | `scripts/setup-asaas-webhooks.sh` | Documents sandbox webhook setup, target endpoint, selected payment/subscription events, and token alignment with service configuration. |
| Webhook ingestion | `services/enrollment-service/src/diplomat/queue/asaas-webhook-ingest.service.ts` | Verifies Asaas webhook token headers, validates body shape, creates correlation metadata, and enqueues the webhook command. |
| Webhook producer | `services/enrollment-service/src/diplomat/queue/producers/asaas-webhook-queue.service.ts` | Sends SQS messages with serialized command bodies and event/correlation/id attributes. |
| Webhook consumer | `services/enrollment-service/src/diplomat/queue/consumers/asaas-webhook-consumer.service.ts` | Long-polls SQS, handles malformed messages, claims events, renews leases, dispatches processing, marks processed/failed, and deletes messages after success. |
| Webhook event idempotency | `services/enrollment-service/src/diplomat/db/repositories/webhook-event.repository.ts` | Implements `claimProcessingOrInsert`, processed duplicate detection, failed/processing retry eligibility, and processing lease renewal. |
| Webhook processor | `services/enrollment-service/src/diplomat/queue/processor/asaas-webhook-processor.service.ts` | Applies payment/subscription transitions in transactions and ignores stale provider events through aggregate timestamps. |
| SQS config | `services/enrollment-service/src/config/sqs.config.ts` | Centralizes queue URLs, endpoint normalization, local credentials, consumer enablement, visibility timeout, batch size, and wait time. |
| Olympiad producer | `services/enrollment-service/src/diplomat/queue/producers/olympiad-import.producer.ts` | Sends bootstrap, plan-annual, external-orchestrator, and external-student commands while enforcing the SQS payload size limit. |
| Olympiad consumer | `services/enrollment-service/src/diplomat/queue/consumers/olympiad-import.consumer.ts` | Runs three queue worker loops, validates command fields, dispatches controller command handlers, deletes successful messages, and leaves failures for retry. |
| Import payload cache | `services/enrollment-service/src/diplomat/queue/olympiad-import-payload-cache.service.ts` | Stores large import request context in Redis by import id with a six-hour TTL. |
| Import orchestration | `services/enrollment-service/src/controllers/olympiad.controller.ts` | Creates jobs, saves payload context, enqueues bootstrap commands, chunks plan-annual and external-school work, and finalizes from stored status. |
| Runtime guard | `services/enrollment-service/src/config/olympiad-sqs.runtime.ts` | Blocks missing or Localstack olympiad queue URLs outside explicitly allowed local defaults. |
| Demo orchestration contrast | `services/enrollment-service/src/demo-provisioning/demo-provisioning.service.ts` | Synchronously coordinates identity, organization, enrollment, and notification adapters for demo leads, useful as a non-queue orchestration comparison. |

## Deviations

- The queue boundary extends Tangram's base Diplomat table with `diplomat/queue` producers, consumers, and worker loops. This aligns with the I/O boundary principle but is not an HTTP handler.
- `OlympiadController` contains both request-facing and command-facing orchestration. The queue consumer stays thin, but the controller is large because it owns job creation, bootstrap, chunk processing, external orchestration, and finalization.
- Requested `terraform-v2/modules/sqs` and `terraform-v2/modules/asaas-events` evidence was not available under `tangram-platform` `origin/main` or the source checkout during this task, so this case study cites service, ADR, and script evidence only.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Generalizes Tangram's Asaas webhook ingestion, idempotency, lease, and stale-event handling.
- [[principles/bulk-import-via-command-queues]] - Generalizes Tangram's olympiad import bootstrap, orchestration, chunking, and payload-cache pattern.

## Related

- [[case-studies/tangram/diplomat-architecture]]
- [[case-studies/tangram/terraform-v2-platform]]
- [[case-studies/tangram/index]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
