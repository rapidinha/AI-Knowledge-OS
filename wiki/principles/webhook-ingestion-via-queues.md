# Webhook Ingestion Via Queues

**When to use:** Use this pattern when external webhook delivery must be acknowledged quickly while processing remains durable, retryable, and idempotent.

## Body

Treat the webhook endpoint as an ingestion boundary, not as the place where business state is finalized. The endpoint should authenticate the provider request, validate that the payload has the minimum shape needed for routing, attach a correlation identifier, and publish a command to a managed queue service.

The worker owns the slower and riskier work: claiming the event, applying domain transitions, recording audit state, and deciding whether the message can be deleted. A persisted event ledger should make duplicates harmless. The claim should distinguish already-processed events, events currently leased by another worker, and events eligible for retry after a failed or expired attempt.

Where the datastore supports it, commit domain effects and the event-ledger processed update in the same transaction. If effects cross systems and cannot be atomic with the ledger, every effect needs its own idempotency key or conditional write based on the provider event id. The retry path must assume a previous worker may have crashed after applying an effect but before marking the event processed.

Long-running handlers need two leases: the queue visibility timeout and the persisted processing claim. Renew them together while work continues. Delete the queue message only after the domain effects and event ledger update succeed. If processing fails, record enough error state to support operations and let the queue retry policy redeliver the command.

Provider events can arrive out of order. Domain aggregates should keep the last applied provider event timestamp or sequence, and handlers should ignore stale transitions instead of moving state backward.

## Trade-offs

- The HTTP path stays fast and resilient to downstream slowness.
- Queue retry and persisted claims protect against transient worker failures and provider redelivery.
- Operators gain an audit trail for stuck, duplicate, failed, and completed events.
- Atomic ledger/effect commits reduce crash-retry ambiguity when the effects share a datastore.
- The system gains operational moving parts: queue configuration, worker health, visibility timeout tuning, and dead-letter monitoring.
- Cross-system effects require extra idempotency work because no queue can make those effects atomic.
- Eventual consistency becomes visible because the webhook request can succeed before business state changes.

## Anti-patterns

- Performing subscription, fulfillment, notification, or ledger mutations directly inside the webhook request handler.
- Relying on provider delivery to be exactly-once instead of storing an idempotency key.
- Deleting queue messages before durable processing state has been committed.
- Marking an event processed separately from domain effects without transactionality, idempotency keys, or conditional writes.
- Treating a queue visibility timeout as the only processing lease when multiple workers can observe the same provider event.
- Applying every received event in arrival order without checking provider event time or aggregate state transitions.

## Checklist for a new project

- [ ] Authenticate the webhook request before enqueueing it.
- [ ] Include a provider event id, event type, received timestamp, source, and correlation id in the queued command.
- [ ] Store a unique idempotency key and processing status before applying business effects.
- [ ] Commit domain effects and event-ledger updates atomically where possible.
- [ ] Add idempotency keys or conditional writes to every cross-system effect that cannot share the event-ledger transaction.
- [ ] Renew queue visibility and persisted processing leases for long-running handlers.
- [ ] Delete messages only after business effects and processed status are durable.
- [ ] Ignore stale or invalid state transitions at the aggregate boundary.
- [ ] Monitor failed, leased, retried, and dead-lettered events.

## Case studies

- [[MOC/async-scale]] - Evidence and implementation examples for queue-backed webhook ingestion.

## Related

- [[principles/bulk-import-via-command-queues]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/async-scale]]
