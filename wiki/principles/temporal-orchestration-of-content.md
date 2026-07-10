# Temporal Orchestration Of Content

**When to use:** Use this pattern when content access depends on scheduled windows, staged release dates, or operator-managed calendar changes.

## Body

Treat time as a first-class model, not as scattered conditionals on content records. A temporal orchestration record should name the target content, define ordered milestones, and expose a small state machine derived from those timestamps.

For event-style content, store explicit milestones such as reveal, open, close, and finish. The derived state should be computed from those fields and the current clock, so every read path can return the same answer for upcoming, active, closed, or finished content.

For course-style content, store a schedule and schedule items. The schedule owns the start date, release frequency, audience context, and version metadata. Schedule items own release dates for each unit or task, plus a flag for manual overrides.

Regeneration should be deliberate. Operators often need to shift future dates, preserve manual overrides, preview changes, or regenerate only from a cutoff. The system should detect data-loss risk before replacing schedule items, especially when learners already have progress in the affected range.

Persist audit snapshots for calendar changes. Time-based access bugs are hard to reconstruct from the final state alone; storing before and after snapshots, actor, change type, and version number makes operations explainable.

## Trade-offs

- Time rules become inspectable, testable, and consistent across read paths.
- Operators can preview, regenerate, and audit schedule changes.
- Derived state avoids manually syncing status fields.
- Calendar models add operational complexity around drift, partial regeneration, and manual overrides.
- Cross-domain progress checks may be needed before releasing or moving content that users have already touched.

## Anti-patterns

- Encoding time windows as ad hoc booleans on the content row.
- Letting each endpoint compute availability with slightly different timestamp logic.
- Replacing generated schedule items without a preview or data-loss guard.
- Treating manual overrides as disposable during regeneration.
- Using local server time without a documented timezone policy for date-only schedules.

## Checklist for a new project

- [ ] Define the ordered timestamps or release dates as persisted fields.
- [ ] Derive state from timestamps in one logic or repository function.
- [ ] Normalize date-only schedules to an explicit timezone.
- [ ] Record manual overrides separately from generated items.
- [ ] Provide dry-run previews for regeneration and bulk shifts.
- [ ] Block or require confirmation for changes that would hide already-started work.
- [ ] Store audit/version snapshots for create, update, regenerate, restore, and delete actions.

## Case studies

- [[MOC/data-persistence]] - Persistence examples for calendar tables, audit logs, and schedule versions.
- [[MOC/product-domain]] - Product-domain examples where content access follows planned windows.

## Related

- [[principles/content-distribution-by-channel]]
- [[principles/timed-session-resume]]
- [[MOC/data-persistence]]
- [[MOC/product-domain]]
