# Reusable PR CI with Patch Coverage Gate

**When to use:** Standardize pull-request quality checks across many repositories while still allowing per-repo knobs for package manager, scripts, integration tests, and a minimum coverage on *changed* lines.

## Body

Centralize the PR pipeline as a **callable workflow** owned by a shared automation repository. Consumer repositories keep a thin `pr.yml` that only declares triggers and passes inputs (`node-version`, package manager, script names, skip flags, coverage threshold, coverage report path).

Split the pipeline into ordered jobs:

1. **Static checks** — install dependencies, then typecheck, lint (no auto-fix), and format check. Fail fast before expensive tests.
2. **Tests + coverage** — after static succeeds, run unit tests with coverage; optionally run integration tests. Provide disposable data stores (database and cache) as job services when integration needs them. Upload the coverage directory as an artifact.
3. **Patch coverage gate** — download the artifact, compare coverage against the PR base branch with a patch-coverage tool, fail under a configured threshold (commonly 80%), and post a sticky PR comment with project totals plus the patch report.

Make the workflow **parameterized** so frontends without integration tests can skip those jobs, and repositories without a test runner can skip the entire test lane. Authenticate private package registries with an org token when present, falling back to the workflow token for same-org packages.

Keep script names as inputs (`typecheck`, `lint:check`, `format:check`, `test:cov`, `test:integration`) so each repo maps its `package.json` without forking the workflow YAML.

## Trade-offs

- One shared definition reduces drift and review cost across dozens of services.
- Inputs and skip flags add complexity; misuse can hide failing integration suites forever.
- Patch coverage rewards testing *changed* code; it does not guarantee high whole-project coverage.
- Shared workflows that always start database/cache services waste time for pure unit-test repos unless consumers can opt out or fork a lighter path.

## Anti-patterns

- Copy-pasting the full PR YAML into every repository instead of calling a shared workflow.
- Gating only on whole-project coverage while large untouched areas inflate the number.
- Skipping integration tests permanently without a tracked remediation plan.
- Auto-fixing lint/format in CI (hides local discipline; prefer check-only scripts).
- Commenting coverage on PRs without failing the job when the patch gate fails.

## Checklist for a new project

- [ ] Publish a callable PR workflow with static → tests → patch-coverage jobs.
- [ ] Expose inputs for package manager, script names, skip flags, coverage threshold, and coverage file path.
- [ ] Fail the pipeline when patch coverage is below the threshold.
- [ ] Upload coverage artifacts and post a durable PR comment summarizing project and patch coverage.
- [ ] Document when consumers should skip integration tests or replace the reusable workflow with a specialized variant (e.g. sharded unit tests without databases).

## Case studies

- [[MOC/engineering-practice]] — Organization-level reusable PR workflow and consumer call sites.

## Related

- [[principles/generated-api-clients-and-contract-ci]]
- [[principles/git-submodules-as-service-boundaries]]
- [[principles/shared-kernel-library-extraction]]
- [[MOC/engineering-practice]]
