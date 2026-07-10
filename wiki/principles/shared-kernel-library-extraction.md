# Shared Kernel Library Extraction

**When to use:** Use this pattern when multiple services need the same small set of stable conventions, guards, models, configuration factories, or validation utilities.

## Body

A shared kernel is the narrowest common library that keeps independently owned services consistent. It should hold cross-cutting primitives whose semantics must match everywhere: auth payload models, decorators, guards, validation pipes, exception filters, metrics interfaces, configuration factories, and baseline tooling config.

The library boundary should be a package boundary. Services consume built exports through a versioned package, not through relative paths into another service. That keeps the dependency explicit, lets each service upgrade deliberately, and avoids turning the shared kernel into an implicit monolith.

Keep the shared kernel boring. Extract only behavior that has already repeated across services or must remain identical for platform safety. Domain-specific rules belong in the owning service until there is clear evidence that they are stable and shared. Every export should have a reason to be common, a documented import path, and a compatibility expectation for consumers.

## Trade-offs

- Shared primitives reduce duplicated security, validation, configuration, and observability code.
- Services stay independent because they depend on a package contract rather than sibling source trees.
- Breaking changes become package versioning and rollout work across all consumers.
- The library can become a dumping ground if teams extract convenience helpers before ownership is clear.

## Anti-patterns

- Moving domain rules into the shared kernel just because two services happen to look similar today.
- Exporting internal folders broadly instead of a small public index.
- Requiring consumers to import from source paths, build artifacts, or unpublished package internals.
- Releasing shared changes without a compatibility check against representative services.
- Putting secrets, environment values, or service-specific URLs inside shared utilities.

## Checklist for a new project

- [ ] List the conventions that must be identical across services before creating a shared package.
- [ ] Keep a single public export surface for consumers.
- [ ] Publish compiled artifacts and configuration files needed by consumers.
- [ ] Use peer dependencies for framework packages that the consuming service already owns.
- [ ] Document local authentication, install, build, and release steps for the package.
- [ ] Test shared changes against at least one representative consumer before release.

## Case studies

- [[MOC/architecture]] - Evidence and implementation examples for this pattern.

## Related

- [[principles/git-submodules-as-service-boundaries]]
- [[principles/generated-api-clients-and-contract-ci]]
- [[principles/dual-channel-auth-jwt-and-service-credentials]]
- [[MOC/architecture]]
