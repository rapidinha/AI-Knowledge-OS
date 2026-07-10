# Async & scale

Hub for queues, webhooks, imports, caching, read models, and background workers.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Durable webhook ingestion with queue-backed processing, idempotency, leases, and stale-event guards.
- [[principles/bulk-import-via-command-queues]] - Long-running imports split into bootstrap, orchestration, and chunk commands.
- [[principles/specialized-read-model-cache]] - Expensive user-facing reads served from bounded, periodically rebuilt projections.
- [[principles/streaming-bulk-file-import-workers]] - Spreadsheet/file imports processed as bounded validated chunks with row-level errors.
- [[principles/pluggable-notification-providers]] - Scheduled campaigns that wake up through a scheduler provider and return to the normal send path.

## Case studies

- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] - Enrollment SQS workers for Asaas webhooks and olympiad imports.
- [[case-studies/tangram/rewards-ranking-cache]] - Rewards ranking cache, visibility cache, and cache-isolation guardrails.
- [[case-studies/tangram/catalog-and-learning]] - Learning VC import chunking, synchronous streaming limits, and draft evaluation persistence.
- [[case-studies/tangram/clients-dx-and-meta]] - Notification campaign scheduling and provider-triggered delivery.

## Related

- [[index]]
- [[MOC/product-domain]]
- [[_meta/coverage-matrix]]
