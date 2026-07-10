# Deterministic Seed Scenarios with Cleanup

**When to use:** Give QA, automated tests, and demos reproducible multi-entity fixtures that can be created and torn down by a named scenario key.

## Body

Define seed **scenarios** as named strategies: each scenario has a stable name, metadata (description, tags), an `execute` method that creates the graph of users/orgs/enrollments/content needed, and a `getDeletePlan` that lists identifiers to remove afterward.

Register scenarios in a central registry so HTTP or CLI entry points can list and run them by name. Protect the endpoints with dedicated scopes or guards so only automated-test or admin principals can seed and delete.

Prefer deterministic identifiers derived from a caller-supplied `seedKey` so re-runs are idempotent or safely replaceable. Cleanup should be explicit and ordered (children before parents) to avoid orphan rows across schemas.

## Trade-offs

- Fast, repeatable environments without hand-crafted SQL dumps.
- Seed APIs are powerful; misuse can pollute shared staging data.
- Cross-service seeds need orchestration and careful delete plans.

## Anti-patterns

- One-off SQL scripts copied between engineers with no cleanup.
- Seed endpoints without strong authorization.
- Scenarios that create data but cannot enumerate what to delete.

## Checklist for a new project

- [ ] Define a scenario interface with execute + delete plan.
- [ ] Register scenarios centrally with listable metadata.
- [ ] Gate seed/delete behind dedicated permissions.
- [ ] Use a seed key for deterministic ids.
- [ ] Test delete plans against the created graph.

## Case studies

- [[MOC/engineering-practice]] — Cross-service automated-test seed scenarios.

## Related

- [[principles/local-dev-presets-without-full-docker]]
- [[principles/agent-rules-as-living-standards]]
- [[MOC/engineering-practice]]
