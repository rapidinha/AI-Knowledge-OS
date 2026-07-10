# Monorepo Contracts and Common Library (Tangram)

**When to use:** Read this case study when you need the concrete Tangram evidence for submodule service boundaries, generated API clients, root contract checks, and `backend-common`.

## Body

Tangram's platform repository is an integration monorepo composed from Git submodules. `.gitmodules` maps backend services under `services/*`, frontend applications under `apps/*`, and the shared backend package under `libs/backend-common` to independent repositories. The root `README.md` presents the platform as a microservice monorepo, documents recursive clone and submodule update commands, and frames each service as a separately worked repository.

That ownership model is reinforced by CI placement. The root `.github` directory owns cross-cutting review metadata and contract checks: `CODEOWNERS` assigns backend, frontend, devops, and tech-lead review areas; `pull_request_template.md` asks contributors to regenerate API clients after contract changes; `backend-contract-check.yml` and `backoffice-contracts.yml` checkout submodules recursively, start selected backend services, run `apps/backoffice` API generation, and fail on generated-client drift or frontend build failure. Routine service CI and deploy workflows live inside service submodules, with `services/identity-service/.github/workflows/pr.yml` and `deploy-staging.yml` as representative examples.

Tangram uses generated clients as the consumer contract artifact. On `origin/main`, `apps/backoffice/package.json` exposes `generate:api`, service-scoped generation commands, and `check:contracts`; `apps/backoffice/orval.config.ts` points Orval at service Swagger JSON endpoints and writes generated React Query fetch clients under `src/api/generated/*`. The web app has the same pattern with `orval` scripts in `apps/web/package.json` and service projects in `apps/web/orval.config.ts`, including both live Swagger endpoints and a checked-in Rewards OpenAPI JSON file.

The shared backend kernel is extracted as `@tangramed/backend-common` in `libs/backend-common`. The package publishes compiled `dist` plus `config`, exposes guards, decorators, models, pipes, strategies, filters, metrics, cache, database helpers, constants, DTOs, and config factories through `src/index.ts`, and documents installation and CI/Docker package-auth setup in `docs/USING_COMMON_LIB.md` and `libs/backend-common/README.md`. Its own `.github/workflows/publish.yml` builds and publishes the package on main pushes and releases.

## Trade-offs

- Tangram keeps service history, PR checks, and deploy workflows close to each submodule while preserving a root workspace for integrated development.
- Root contract checks make backend API drift visible to frontend owners by regenerating generated clients and building the backoffice consumer.
- `backend-common` centralizes auth, validation, metrics, throttle, config, and tooling conventions that would otherwise be repeated across services.
- The submodule model makes cross-service features more operationally complex because contributors must coordinate nested repository PRs and root pointer updates.
- Contract workflows need service startup and private package access, so they are heavier than pure typecheck jobs and can drift when the service list changes.

## Anti-patterns

- Tangram avoids treating root CI as the owner of every service's normal test and deploy lifecycle; those workflows live in the service repositories.
- Tangram avoids hand-maintaining most backoffice API clients; generated directories are checked for drift after running Orval.
- A current risk is coverage mismatch: the root backoffice contract workflows start only identity, organization, enrollment, and catalog, while frontend codegen configs include additional service projects.
- A current risk is shared-kernel overreach: `backend-common` is useful for cross-cutting primitives, but domain rules should stay in owning services until they are stable enough to publish.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Submodule map | `.gitmodules` | Lists backend services, frontend apps, and `libs/backend-common` as independent submodule repositories. |
| Root monorepo docs | `README.md` | Documents recursive clone, submodule init/update, service ports, and working inside individual services. |
| Root contract push check | `.github/workflows/backend-contract-check.yml` | Triggers on backend DTO/response/entity/http-in changes, checks out submodules recursively, starts selected services, runs backoffice `generate:api`, builds, and shows generated diffs. |
| Root contract PR check | `.github/workflows/backoffice-contracts.yml` | Runs on backoffice and backend contract paths, regenerates backoffice API clients, fails on generated drift, and builds backoffice. |
| Ownership and PR checklist | `.github/CODEOWNERS` and `.github/pull_request_template.md` | Assigns review ownership and asks contributors to run `cd apps/backoffice && npm run generate:api` after API contract changes. |
| Backoffice scripts | `apps/backoffice/package.json` | On `origin/main`, exposes `generate:api`, per-service generation scripts, `check:contracts`, build, typecheck, lint, and coverage commands. |
| Backoffice codegen config | `apps/backoffice/orval.config.ts` | Uses Orval to read Swagger JSON or a local OpenAPI file and write generated clients under `src/api/generated/*`. |
| Web scripts | `apps/web/package.json` | On `origin/main`, exposes `orval` and per-service Orval project scripts alongside build, lint, typecheck, unit, coverage, and e2e commands. |
| Web codegen config | `apps/web/orval.config.ts` | Uses Orval projects for identity, organization, enrollment, catalog, learning, and rewards generated clients. |
| Representative service PR CI | `services/catalog-service/.github/workflows/pr.yml` (and peers) | Delegates service PR checks to `TangramEd/.github/.github/workflows/pr.yml@main` with Node, package-manager, integration skip, and coverage threshold inputs. See [[case-studies/tangram/reusable-pr-pipeline]]. |
| Representative service deploy CI | `services/identity-service/.github/workflows/deploy-staging.yml` | Owns staging deployment for the identity service inside the service submodule. |
| Shared backend package docs | `docs/USING_COMMON_LIB.md` and `libs/backend-common/README.md` | Document package installation, private package auth, CI/Docker setup, usage imports, and available exports. |
| Shared backend package surface | `libs/backend-common/package.json` and `libs/backend-common/src/index.ts` | Defines package metadata, peer dependencies, published files, and the public export surface for models, decorators, guards, pipes, strategies, filters, config, modules, database, cache, constants, and DTOs. |
| Shared package publish CI | `libs/backend-common/.github/workflows/publish.yml` | Builds and publishes the package to GitHub Packages on main pushes and releases. |

## Deviations

- The root contract workflows validate backoffice compatibility directly, while the web app has its own Orval config and PR workflow but no matching root web contract check in the researched root workflows.
- The backoffice contract workflows start a subset of services before running full backoffice generation; configs for additional service clients should be validated by their owning workflows or by extending the root contract job.
- `backend-common` is both a submodule in the platform workspace and a published package. The package boundary is the intended consumer boundary; direct source-path coupling would weaken the submodule boundary.

## Principles

- [[principles/git-submodules-as-service-boundaries]] - Generalizes Tangram's root repository as an integration workspace for independently owned submodules.
- [[principles/generated-api-clients-and-contract-ci]] - Generalizes Tangram's generated-client drift checks and frontend build gate.
- [[principles/shared-kernel-library-extraction]] - Generalizes Tangram's `backend-common` package as a narrow shared backend kernel.

## Related

- [[case-studies/tangram/diplomat-architecture]]
- [[case-studies/tangram/identity-pbac-and-auth]]
- [[case-studies/tangram/index]]
- [[MOC/architecture]]
- [[MOC/engineering-practice]]
