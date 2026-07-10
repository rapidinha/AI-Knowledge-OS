# Architecture Decision Records

**When to use:** Use this pattern when a technical decision needs durable context, trade-offs, and consequences beyond the code diff that introduced it.

## Body

An architecture decision record captures why a decision was made, not only what changed. The note should name the decision, status, date, context, constraints, decision, rationale, consequences, and follow-up work. It should be short enough to read during implementation and detailed enough to prevent the same debate from restarting later.

Records are most useful for cross-boundary decisions: service ownership, user lifecycle, event orchestration, external integrations, audit strategy, security posture, and frontend-backend contract behavior. A record can be accepted, proposed, superseded, or deprecated; the status matters because it tells readers whether the document describes shipped behavior, target architecture, or historical rationale.

Keep records linked to implementation evidence. The record should cite affected modules, data models, APIs, migrations, or workflows, and later changes should update the status or add a new record rather than silently invalidating the old one.

## Trade-offs

- Future contributors can recover decision context without relying on memory.
- Reviewers can distinguish intentional design from incidental code shape.
- Proposed records can guide implementation before all code exists.
- Stale records can mislead readers if status and follow-up sections are not maintained.

## Anti-patterns

- Writing a record after the fact that only repeats the final code structure.
- Mixing accepted behavior and future intent without status labels.
- Keeping architecture decisions only in chat, tickets, or pull request comments.
- Updating code that contradicts a record without superseding or amending the decision.
- Creating records for every small implementation detail instead of meaningful trade-offs.

## Checklist for a new project

- [ ] Store records in a predictable architecture docs directory.
- [ ] Use a consistent template with status, context, decision, rationale, consequences, and follow-ups.
- [ ] Record whether the decision is proposed, accepted, superseded, or deprecated.
- [ ] Link records to affected modules, APIs, migrations, or workflows.
- [ ] Add a lightweight index or MOC once records become numerous.
- [ ] Revisit records during major refactors and incident follow-ups.

## Case studies

- [[MOC/engineering-practice]] - Engineering examples for architecture records as maintained standards.
- [[MOC/architecture]] - Architecture examples where decisions document service and system boundaries.

## Related

- [[principles/agent-rules-as-living-standards]]
- [[principles/temporal-orchestration-of-content]]
- [[principles/timed-session-resume]]
- [[MOC/engineering-practice]]
- [[MOC/architecture]]
