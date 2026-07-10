# Generated API Clients and Contract CI

**When to use:** Use this pattern when frontend or consumer code should compile against provider API contracts before provider changes reach users.

## Body

Generated clients turn an API description into typed consumer code. The provider exposes a machine-readable contract, such as an OpenAPI document. A consumer runs an OpenAPI codegen tool to produce request functions, schemas, hooks, or types in a generated directory. Application code imports the generated surface instead of hand-writing endpoint URLs and response shapes.

Contract CI closes the loop. When provider DTOs, response objects, entities, or route handlers change, the integration workflow should start enough of the provider stack to serve the contract, regenerate the consumer client, and fail if generated files drift or the consumer no longer builds. For consumer-only changes, CI should also check that generated files are already up to date.

The generated directory is not design source; it is a committed compatibility artifact. Reviewers should inspect diffs for breaking shape changes, removed fields, renamed enum values, and client usage fallout. The source of truth remains the provider contract and the consumer code that compiles against it.

## Trade-offs

- Consumers get compile-time feedback when provider contracts move.
- Reviewers can see API drift as generated diffs instead of discovering it at runtime.
- CI can be slower because it may need provider services, databases, caches, and client builds.
- Generated files can create noisy diffs if the codegen tool is unstable or run with inconsistent versions.

## Anti-patterns

- Hand-editing generated client files instead of fixing the provider contract, codegen config, or consumer usage.
- Running codegen locally but not enforcing drift in forge CI.
- Treating a successful provider test suite as proof that all consumers still compile.
- Regenerating clients from a stale checked-in contract while the deployed provider serves a different one.
- Hiding breaking changes by committing generated diffs without updating the consumer code path that uses them.

## Checklist for a new project

- [ ] Define which provider artifacts trigger consumer contract validation.
- [ ] Pin the OpenAPI codegen tool and keep its config in version control.
- [ ] Commit generated clients only in a clearly named generated directory.
- [ ] Add a CI job that regenerates clients and fails on uncommitted drift.
- [ ] Add a CI job that builds or typechecks the consumer against regenerated clients.
- [ ] Document the local command reviewers should ask contributors to run after API changes.

## Case studies

- [[MOC/engineering-practice]] - Evidence and implementation examples for this pattern.

## Related

- [[principles/git-submodules-as-service-boundaries]]
- [[principles/shared-kernel-library-extraction]]
- [[MOC/engineering-practice]]
