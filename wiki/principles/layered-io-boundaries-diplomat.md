# Layered I/O Boundary Architecture

**When to use:** Use this pattern when a service must keep transport, orchestration, domain rules, persistence, cache, external calls, and response contracts independently reviewable.

## Body

Treat every service boundary as a set of adapters around a small orchestration core. Inbound adapters should parse transport-specific input, apply authentication and routing, and hand validated command or query data to the application layer. They should not decide business outcomes.

The application layer coordinates the use case: gather existing state through repositories or outbound clients, call domain logic with plain data, then produce effects such as writes, cache updates, event publication, or outbound requests. This "gather, decide, effect" shape makes it clear which lines can talk to the outside world and which lines should be deterministic.

Domain logic should work on models or value objects, not on request objects, database rows, framework contexts, or network clients. Repositories own persistence details. Cache adapters own cache keys, serialization, TTL, and retry behavior. Data adapters translate between entities, models, input contracts, and output contracts.

Directory names are less important than the boundary rule: transport code depends inward, orchestration depends on ports and domain logic, domain logic depends on no I/O, and adapters sit at the edges.

## Trade-offs

- Clear boundaries make reviews faster because each file has an expected responsibility.
- Pure rules become easier to test without databases, queues, or web servers.
- The service gains more files than a single-handler implementation.
- Small features can feel ceremonious if the team creates every layer before there is real behavior.

## Anti-patterns

- Putting business decisions in route handlers because they already have request data.
- Letting domain rules call repositories, cache clients, clocks, queues, or external services directly.
- Returning persistence entities directly from public responses when a response contract should own shape and redaction.
- Creating adapters that contain hidden business rules instead of mechanical translation.
- Naming folders after layers while allowing any layer to import any other layer.

## Checklist for a new project

- [ ] Define inbound adapters, orchestration, domain logic, persistence adapters, cache adapters, and wire contracts before the first complex endpoint ships.
- [ ] Keep request parsing, auth decorators, and response serialization in the inbound boundary.
- [ ] Make orchestration code read as gather data, call logic, produce effects.
- [ ] Keep domain logic free of I/O clients, request objects, and persistence entities unless those entities are pure data in the project.
- [ ] Add tests at the cheapest boundary: pure logic first, adapter tests for transformations, orchestration tests when effects are coordinated.

## Case studies

- [[MOC/architecture]] - Evidence and implementation examples for this pattern.

## Related

- [[principles/pure-domain-logic-no-io]]
- [[MOC/architecture]]
