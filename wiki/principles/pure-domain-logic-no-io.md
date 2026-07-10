# Pure Domain Logic with No I/O

**When to use:** Use this pattern when business rules must stay testable, deterministic, and separate from databases, caches, queues, clocks, and transport frameworks.

## Body

Put domain decisions in functions or classes that accept explicit inputs and return explicit outputs. The logic layer should validate rules, derive state transitions, calculate schedules or rankings, normalize domain values, and classify errors without opening network connections, writing records, reading request context, or emitting messages.

The application layer should gather everything the logic needs before calling it. If a rule depends on existing records, fetch those records first and pass the relevant data in. If the rule produces a decision that requires an effect, return that decision to orchestration and let the orchestration layer perform the write, publish the event, or update the cache.

Pure logic does not mean trivial logic. It is often where the most important behavior belongs because tests can cover edge cases with in-memory data. Keep dependencies small: value objects, enums, immutable inputs, and domain models are good inputs; repositories, cache clients, framework request objects, and global state are not.

When time, randomness, or configuration affects a rule, pass the value in as data. That keeps repeatability under the caller's control and prevents hidden production-only behavior from leaking into unit tests.

## Trade-offs

- Rules can be tested quickly with focused inputs and no service harness.
- Orchestration remains responsible for side effects, which makes failures and retries easier to reason about.
- Callers must gather enough context up front, so application methods can become longer.
- Over-purifying simple pass-through code can add indirection without improving reliability.

## Anti-patterns

- Calling repositories, cache clients, queues, or external APIs from rule code.
- Reading current user, request headers, environment variables, or mutable global state inside domain decisions.
- Hiding write operations behind methods named like validators or calculators.
- Mixing parsing of transport DTOs with domain validation when the transport shape is not the domain shape.
- Mocking heavy infrastructure in unit tests for logic that could have accepted plain data.

## Checklist for a new project

- [ ] Identify domain rules that should run without a database, cache, queue, or server.
- [ ] Pass existing state into the rule instead of letting the rule fetch it.
- [ ] Return decisions, errors, or derived values from the rule instead of performing effects inside it.
- [ ] Inject time, randomness, and configuration as explicit values when rules depend on them.
- [ ] Keep at least one focused unit test for every non-trivial rule branch.

## Case studies

- [[MOC/architecture]] - Evidence and implementation examples for this pattern.

## Related

- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/architecture]]
