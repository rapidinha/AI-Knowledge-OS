# Git Submodules as Service Boundaries

**When to use:** Use this pattern when a monorepo must compose independently versioned services without collapsing their ownership, history, release, and review boundaries.

## Body

A submodule-based platform repository should be treated as an integration workspace, not as the source repository for every service. The root repository pins a known-good commit for each service, library, or application. Each nested repository keeps its own commit history, pull requests, CI, release tags, and access rules.

This pattern works best when the submodule boundary matches a deployable or reusable unit. A service submodule should expose behavior through documented APIs, events, database contracts, or generated clients instead of relying on source imports from sibling services. A shared library submodule should be published or otherwise consumed through a package boundary, not by path-peeking into its source.

The root repository should own integration concerns: local development orchestration, dependency bootstrap, contract checks, environment composition, and cross-submodule documentation. Updating a submodule pointer becomes an explicit integration event: review the nested repository change first, then move the root pin only when the platform workspace is compatible.

## Trade-offs

- Teams can ship, review, and permission services independently while preserving a runnable platform workspace.
- Root-level integration commits make cross-service compatibility visible and reversible.
- Developers must learn both nested repository workflows and root pointer updates.
- Atomic changes that span many services require coordination across repositories before the root pointer can advance.

## Anti-patterns

- Treating the root repository as if it owns the nested source code, which hides the real review and release boundary.
- Importing private implementation files from sibling submodules instead of using contracts or packages.
- Moving submodule pointers without evidence that the nested repository passed its own checks.
- Letting root CI duplicate every per-service test when it should focus on integration and contract compatibility.
- Leaving submodules empty or stale in local setup, making the root workspace appear broken for new contributors.

## Checklist for a new project

- [ ] Map each submodule to a service, application, infrastructure unit, or shared library with clear ownership.
- [ ] Document clone, init, update, and local development commands for nested repositories.
- [ ] Keep routine PR, test, and deploy workflows inside the nested repository that owns the code.
- [ ] Add root-level checks only for cross-submodule integration, contract compatibility, and workspace bootstrap.
- [ ] Require root pointer updates to cite the nested repository change they integrate.

## Case studies

- [[MOC/architecture]] - Evidence and implementation examples for this pattern.

## Related

- [[principles/shared-kernel-library-extraction]]
- [[principles/generated-api-clients-and-contract-ci]]
- [[MOC/architecture]]
