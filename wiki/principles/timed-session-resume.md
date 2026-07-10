# Timed Session Resume

**When to use:** Use this pattern when a user can leave and later resume a time-limited session without losing progress or creating duplicate attempts.

## Body

Make the backend the source of truth for session state and elapsed time. The client may render a live countdown, but it should start from server-provided remaining time and reconcile through session endpoints rather than inventing a new clock after reload.

Start should be idempotent for resumable sessions. Before creating a new row, look up the active key for the user, work item, and optional policy date. If the matching session is in progress or abandoned with remaining time, return it with existing answers and calculated remaining time. If it is completed, return a conflict.

Persist active time, not just wall-clock start time. Store elapsed seconds accumulated before pauses or abandons, plus the timestamp of the latest resume. Remaining time becomes `limit - (elapsed + running duration)` while active, and `limit - elapsed` while paused or abandoned.

Pause, resume, complete, and abandon should be explicit transitions. Each transition updates session fields and writes an event row so support and analytics can reconstruct the lifecycle. Completion should be idempotent and derive final counters from authoritative child rows when possible.

Timeout enforcement should be conservative. Use strict server-side checks before accepting answers or completing sessions, but consider a small timeout buffer for race conditions between client countdown, network delay, and database writes.

## Trade-offs

- Users can reload, switch tabs, or recover from disconnects without duplicate attempts.
- Server-derived remaining time reduces client clock drift.
- Event rows give an audit trail for support and analytics.
- Idempotent start adds branching and careful uniqueness constraints.
- Very frequent heartbeat-style updates can improve accuracy but add load and concurrency concerns.

## Anti-patterns

- Treating an abandoned session as permanently locked even when it still has time.
- Starting a new session before checking the unique active key.
- Computing remaining time only from the original start timestamp.
- Letting the client decide whether an answer is still valid without a server check.
- Incrementing summary counters as the only source of truth when answer rows can be aggregated.

## Checklist for a new project

- [ ] Define the unique active key for a session, including any policy date.
- [ ] Store `elapsedTimeSeconds`, `lastResumedAt`, `pausedAt`, and `timeLimitSeconds`.
- [ ] Make start return an existing resumable session when one exists.
- [ ] Make completed sessions conflict instead of silently reopening.
- [ ] Write event rows for start, pause, resume, complete, abandon, and submitted answers.
- [ ] Derive remaining time in one logic function and project it in the response.
- [ ] Check timeout on answer and completion paths, not only in the UI.

## Case studies

- [[MOC/product-domain]] - Product-domain examples for resumable user sessions.
- [[MOC/data-persistence]] - Persistence examples for unique session keys and event rows.

## Related

- [[principles/temporal-orchestration-of-content]]
- [[principles/pure-domain-logic-no-io]]
- [[MOC/product-domain]]
- [[MOC/data-persistence]]
