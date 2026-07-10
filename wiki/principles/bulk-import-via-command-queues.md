# Bulk Import Via Command Queues

**When to use:** Use this pattern when a user-initiated import can exceed request time limits, message size limits, or single-worker throughput.

## Body

Represent the import as a job, then move work through explicit commands instead of one long synchronous request. The request path should validate intent, create the job, persist or cache large request context, and enqueue a small bootstrap command that references the job id.

Separate command roles make the workflow easier to operate. A bootstrap command prepares the job and splits source data into bounded chunks. An orchestrator command can fan out work for each source group, tenant, file section, or external partition. Chunk commands process one bounded slice and update item-level status.

Queue messages should stay small and reconstructable. Put large non-secret payloads, uploaded files, or import context in a durable store, then pass stable identifiers in each command. A bounded cache is acceptable only when its TTL is longer than the queue retry and dead-letter replay window, and the worker has documented recovery behavior for a missing context lookup. Required inputs must remain available for delayed retries and manual replay.

Do not put credentials in queue messages, ordinary job context, generic durable stores, or unbounded caches. If a worker needs temporary credentials, pass a reference to a restricted, encrypted secret store with controlled access and explicit expiration.

Workers should prefer retryable item states over hidden in-memory progress. A failed chunk should be safe to retry, skip already-completed items, and mark permanently invalid items with reasoned failure state. The finalizer should derive completion from stored job and item status rather than from how many worker processes happened to run.

## Trade-offs

- Large imports no longer depend on a single HTTP request staying open.
- Chunking lets workers scale horizontally and retry partial failures.
- Stored job and item status gives support teams progress and failure visibility.
- The workflow adds more states and commands than a direct import function.
- Small-message discipline often requires a separate payload store or cache with its own TTL and cleanup rules.
- Required context retention must be sized against retry and dead-letter replay windows, not just normal processing time.

## Anti-patterns

- Sending the full import file or large request body through the queue.
- Storing secrets in queue messages, generic job payloads, or caches that are not encrypted, access-controlled, and expiring.
- Using one command that both orchestrates the whole job and processes every item.
- Tracking progress only in worker memory or logs.
- Treating chunk retries as fresh work without checking item status.
- Letting cached context expire before queue retries or dead-letter replay can finish.
- Finalizing the import because the last observed worker finished, rather than because stored state says all required work is terminal.

## Checklist for a new project

- [ ] Create an import job before enqueueing the first command.
- [ ] Store large request context outside queue messages and pass stable references.
- [ ] Keep required context available for the full retry and dead-letter replay window, or document recovery when a context reference is missing.
- [ ] Store secrets only in restricted encrypted secret storage with access controls and explicit expiration.
- [ ] Define separate command types for bootstrap, orchestration, and chunk processing when the import has multiple phases.
- [ ] Bound chunk size by queue visibility timeout, downstream rate limits, and item-level transaction cost.
- [ ] Persist item status so retries can skip completed work and expose failures.
- [ ] Make finalization derive from durable job state.
- [ ] Add runtime guards so production workers cannot accidentally target local queue endpoints.

## Case studies

- [[MOC/async-scale]] - Evidence and implementation examples for command-queue imports.
- [[MOC/product-domain]] - Product-domain examples where imports provision enrollment or access state.

## Related

- [[principles/webhook-ingestion-via-queues]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
