# Soft Delete with Actor Audit

**When to use:** Persist business records that must disappear from default queries while remaining recoverable and attributable to who removed them.

## Body

Prefer soft delete over hard delete for user-facing and configuration entities. Mark rows with a deletion timestamp column that the ORM excludes from normal finds, and store an optional actor identifier for who requested the delete.

Keep create/update actor fields alongside delete metadata so the same entity carries a minimal audit trail without a separate audit table for every mutation. Use hard delete only for ephemeral or regenerable data where retention has no compliance or support value.

Apply the convention consistently across services that share the same persistence style, and document intentional exceptions (for example immutable event or session rows that should never soft-delete).

## Trade-offs

- Recoverability and support investigation without restoring from backups.
- Tables grow with tombstones; indexes and unique constraints must account for deleted rows.
- Every query path must respect soft-delete filters (including raw SQL and reports).

## Anti-patterns

- Mixing hard delete and soft delete for the same aggregate without an explicit rule.
- Soft-deleting without recording who deleted when the domain requires accountability.
- Unique constraints that block re-creating a logically deleted business key.

## Checklist for a new project

- [ ] Define which entities soft-delete vs hard-delete.
- [ ] Add deletion timestamp + optional deleted-by actor fields.
- [ ] Ensure ORM global filters or repository conventions hide deleted rows by default.
- [ ] Decide how unique indexes treat soft-deleted rows.
- [ ] Document exceptions for immutable/event tables.

## Case studies

- [[MOC/data-persistence]] — Soft-delete conventions across service entities.

## Related

- [[principles/layered-io-boundaries-diplomat]]
- [[principles/architecture-decision-records]]
- [[MOC/data-persistence]]
