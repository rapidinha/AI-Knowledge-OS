# Async & scale

Hub for queues, webhooks, imports, caching, read models, and background workers.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Durable webhook ingestion with queue-backed processing, idempotency, leases, and stale-event guards.
- [[principles/bulk-import-via-command-queues]] - Long-running imports split into bootstrap, orchestration, and chunk commands.
- [[principles/specialized-read-model-cache]] - Expensive user-facing reads served from bounded, periodically rebuilt projections.
- [[principles/typed-domain-cache-with-ttl-tiers]] - Typed get/set/invalidate caches with per-type TTLs and optional L1 memory for domain snapshots.
- [[principles/streaming-bulk-file-import-workers]] - Spreadsheet/file imports processed as bounded validated chunks with row-level errors.
- [[principles/pluggable-notification-providers]] - Scheduled campaigns that wake up through a scheduler provider and return to the normal send path.
- [[principles/event-capacity-overlay-on-baseline-autoscaling]] - Known-peak capacity overlays on baseline autoscaling (infra companion to async load).

## Related

- [[index]]
- [[MOC/product-domain]]
- [[_meta/coverage-matrix]]
