# Reusable PR Pipeline with Patch Coverage (Tangram)

**When to use:** Read this when you need Tangram's concrete reusable GitHub Actions PR pipeline, how services call it, and why the web app forked a faster variant while keeping the same patch-coverage gate.

## Body

Tangram centralizes PR quality checks in an organization reusable workflow: `TangramEd/.github/.github/workflows/pr.yml` (callable via `workflow_call`). The workflow the team maintains exposes inputs for Node version, package manager (`npm` | `pnpm` | `yarn`), script names (`typecheck`, `lint:check`, `format:check`, `test:cov`, `test:integration`), `skip-integration`, `skip-tests`, `coverage-threshold` (default 80), and `coverage-file` (default `coverage/cobertura-coverage.xml`).

Jobs:

1. **Static checks** — `actions/checkout` + `setup-node` with GitHub Packages registry for `@tangramed`, install via the selected package manager using `NODE_AUTH_TOKEN` (`NPM_TOKEN` or `GITHUB_TOKEN`), then typecheck, lint, and prettier check.
2. **Tests + coverage** — needs static; optional skip via `skip-tests`. Starts Postgres 16 and Redis 7 service containers, sets `DATABASE_URL` / `REDIS_URL`, runs unit coverage then optional integration tests, uploads the `coverage/` artifact (fails if missing).
3. **Patch coverage gate** — needs tests; full git history, downloads coverage, installs `diff-cover`, fails under the threshold against `origin/${{ github.base_ref }}`, builds a markdown summary from Cobertura line/branch rates, and posts a sticky PR comment (`marocchino/sticky-pull-request-comment`) with header `patch-coverage`.

Most backend services and the backoffice keep a thin caller. Examples on the platform workspace: `services/catalog-service/.github/workflows/pr.yml`, `enrollment-service`, `learning-service`, `organization-service`, `rewards-service`, and `apps/backoffice/.github/workflows/pr.yml` all `uses: TangramEd/.github/.github/workflows/pr.yml@main` with `node-version: "22"`, `package-manager: "npm"`, `skip-integration: true`, `coverage-threshold: 80`, and `secrets: inherit`. Comments in those callers note integration skips until testcontainers/schema migration setup is standardized.

The web app **intentionally replaces** the reusable workflow. `apps/web/.github/workflows/pr.yml` documents that the shared job was ~7 minutes sequential and started Postgres/Redis unnecessarily for pure unit tests. The custom pipeline keeps static checks, shards Vitest into four parallel coverage jobs, merges reports, still runs `diff-cover` at 80%, caches `node_modules`, pins actions by SHA for supply-chain policy, and uses concurrency cancellation per PR.

## Trade-offs

- Org-level reuse keeps service PR YAML tiny and thresholds consistent (80% patch).
- Widespread `skip-integration: true` means the shared integration lane is currently underused until schema/testcontainers work lands.
- Web's fork improves wall-clock time but must be maintained separately when the reusable workflow evolves.
- Sticky coverage comments improve PR review signal; they require `pull-requests: write` on the gate job.

## Anti-patterns

- Tangram avoids duplicating the full static/test/gate YAML in every service by calling the org workflow.
- Tangram avoids treating whole-repo coverage alone as the merge gate; patch coverage is the hard fail.
- A current risk is permanent integration skips without closing the tracked remediation.
- A current risk is diverging web custom CI without periodically reconciling thresholds and comment format with the org workflow.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Org reusable workflow (source of truth) | `TangramEd/.github/.github/workflows/pr.yml` | Callable PR Pipeline: static → tests+coverage → patch-coverage; inputs for PM, scripts, skips, 80% default threshold, Cobertura path, sticky PR comment. |
| Catalog caller | `services/catalog-service/.github/workflows/pr.yml` | `uses: …/pr.yml@main` with `skip-integration: true`, threshold 80. |
| Enrollment caller | `services/enrollment-service/.github/workflows/pr.yml` | Same reusable call pattern. |
| Learning caller | `services/learning-service/.github/workflows/pr.yml` | Same; notes testcontainers schema pending. |
| Organization caller | `services/organization-service/.github/workflows/pr.yml` | Same; TODO to remove skip. |
| Rewards caller | `services/rewards-service/.github/workflows/pr.yml` | Same reusable call pattern. |
| Backoffice caller | `apps/backoffice/.github/workflows/pr.yml` | Same reusable call pattern. |
| Web custom PR CI | `apps/web/.github/workflows/pr.yml` | Documents replacement of reusable workflow; sharded Vitest; `diff-cover` gate at 80%; no DB services. |

## Deviations

- **Web fork:** Same quality bar (static + patch coverage) without the reusable workflow's DB services or single long test job.
- **Integration skips:** Most callers set `skip-integration: true` while the reusable workflow still supports integration when ready.
- **Action pinning:** Web pins actions by SHA; the reusable workflow snippet uses major tags (`@v4`) — supply-chain strictness differs by consumer.

## Principles

- [[principles/reusable-pr-ci-with-patch-coverage]]
- [[principles/git-submodules-as-service-boundaries]]
- [[principles/generated-api-clients-and-contract-ci]]
- [[principles/shared-kernel-library-extraction]]

## Related

- [[case-studies/tangram/monorepo-contracts-and-common]]
- [[case-studies/tangram/clients-dx-and-meta]]
- [[MOC/engineering-practice]]
- [[_meta/coverage-matrix]]
