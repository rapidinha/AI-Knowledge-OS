# Event Capacity Overlay on Baseline Autoscaling

**When to use:** Temporarily raise compute and data capacity for a known high-traffic event without permanently rewriting baseline environment sizing.

## Body

Keep a **baseline** autoscaling policy for normal days (CPU/memory targets, nightly/weekend scale-down). For planned peak events, introduce an **overlay** controlled by a single feature flag:

- Merge higher min/desired/max task counts and optional larger instance classes into the production maps.
- **Suspend dynamic scale-in** (or suppress recurring downscales) so the pre-warmed floor is not eaten by idle metrics before the event.
- Schedule a **graceful step-down** after the event end (for example halve the floor, then return to baseline after a drain buffer).

Apply the overlay through infrastructure-as-code so capacity changes are reviewed like any other production change. Keep the overlay isolated in its own file or module so day-to-day sizing stays readable.

## Trade-offs

- Predictable headroom for known peaks without permanent over-provisioning.
- Operators must remember to toggle the flag and set end times; mistakes leave expensive capacity running.
- Overlay merges can obscure which values are baseline vs event-specific if not documented.

## Anti-patterns

- Manually clicking console capacity changes during the event with no IaC record.
- Leaving the event flag on indefinitely.
- Using only reactive autoscaling for a known spike that needs pre-warmed capacity.

## Checklist for a new project

- [ ] Document baseline vs event capacity maps.
- [ ] Gate the overlay behind one explicit enable flag.
- [ ] Suppress conflicting scheduled scale-downs while the overlay is active.
- [ ] Define post-event step-down schedule and drain buffer.
- [ ] Add an operational checklist to disable the flag after the event.

## Case studies

- [[MOC/infrastructure]] — Event capacity overlays on shared autoscaling.

## Related

- [[principles/multi-env-terraform-single-state]]
- [[principles/modular-iaas-boundaries]]
- [[MOC/infrastructure]]
