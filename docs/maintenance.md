# Documentation and Scaffold Maintenance

Documentation is a **product** of the Protocol Kernel — versioned, governed, and maintained alongside contracts and scaffold.

## Docs as product

Institutional docs ([VISION.md](../VISION.md), [MISSION.md](../MISSION.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [GOVERNANCE.md](../GOVERNANCE.md), and this tree under `docs/`) are reviewed at each roadmap phase. They must stay aligned with [engine/invariants.md](../engine/invariants.md).

When architecture or governance changes, update the canonical doc first, then link dependents. Do not leave silent divergent copies.

## Drift checks

The **Documentation Maintainer** agent (see [agents/documentation-maintainer/](../agents/documentation-maintainer/)) watches for:

| Check | What to look for |
|-------|------------------|
| Dead links | Broken relative links across README, institutional docs, contracts |
| Orphan folders | Directories with no README or index pointer |
| Identity drift | Docs that describe AI Knowledge OS as a PKM app, wiki product, or news aggregator |
| Contradictions | Text that conflicts with [ARCHITECTURE.md](../ARCHITECTURE.md) or [engine/invariants.md](../engine/invariants.md) |
| Scaffold rot | Public `wiki/` containing living corpus (principles `.md`, filled case studies) |
| Provider prominence | Feature docs (e.g. `docs/radar/`) competing with kernel identity |

File issues or PRs when drift is found. Structural architecture changes require an RFC before merge.

## Contract versioning

Contracts under [contracts/](../contracts/) are the stable API of the kernel.

| Change type | Requirement |
|-------------|-------------|
| Additive (new optional fields) | Minor version note in contract file; document in PR |
| Breaking (removed/renamed required fields, semantic change) | RFC in `wiki/rfcs/` (instance) or OSS RFC process + **major** version bump in contract file |
| New contract type | RFC + new file under `contracts/` |

Breaking schema changes never ship silently. Consumers (agents, providers, instance tooling) must have a migration path or explicit deprecation window.

## Scaffold CI

Upstream CI enforces boundary rules so the public tree stays framework-only:

- Forbidden personal paths at repo root (`knowledge/`, `notes/`, `journals/`, `experiments/`, `obsidian/`, `vault/`)
- `research/` at root allowed **only** as scaffold (`README.md`, `.gitkeep`)
- Public `wiki/principles/` must not contain a markdown corpus

See [.github/workflows/boundary-check.yml](../.github/workflows/boundary-check.yml) and [GOVERNANCE.md](../GOVERNANCE.md).

Instance repos may contain full personal trees; those rules apply to the **public upstream** repository only.

## One source of truth

Each concept has one canonical home:

| Concept | Canonical location |
|---------|-------------------|
| Product identity | [VISION.md](../VISION.md), [ARCHITECTURE.md](../ARCHITECTURE.md) |
| Cycle protocol | [engine/cycle.md](../engine/cycle.md) |
| Artifact shapes | [contracts/](../contracts/) |
| Wiki schema | [wiki/_meta/templates.md](../wiki/_meta/templates.md), [wiki/_meta/governance.md](../wiki/_meta/governance.md) |
| OSS vs instance rules | [GOVERNANCE.md](../GOVERNANCE.md) |
| Agent behavior | [AGENTS.md](../AGENTS.md) + per-agent README under [agents/](../agents/) |
| Reference providers | [providers/](../providers/) + [docs/radar/](radar/) |

Do not duplicate full explanations across files without a link back to the canonical doc. Historical specs and plans under `docs/superpowers/specs/` and `docs/superpowers/plans/` are archive — not product identity.

## Reference providers

Providers (e.g. Leverage Radar under `providers/signals/`) are optional and replaceable. External API failure should degrade gracefully — it must not break the kernel.

Provider docs live under [docs/radar/](radar/) with an explicit banner that they describe a reference signal provider, not the product.

## Documentation Maintainer role

| Emits | Never does |
|-------|------------|
| Doc PRs, drift issues, link fixes | Change ADRs or architecture without RFC |
| Scaffold hygiene reports | Overwrite instance wiki content |
| Contract cross-reference updates | Promote personal knowledge to OSS |

Humans approve structural wiki moves in the instance. The Maintainer keeps the **framework** docs and scaffold healthy.

## Instance wiki review cadence

In the private instance, run periodic review (e.g. monthly):

- Orphan notes without inbound links
- Stale principles contradicting recent ADRs
- Broken wikilinks
- Concepts duplicated across categories

Use [wiki/_meta/governance.md](../wiki/_meta/governance.md) for create/update/archive rules. Archive to `_archive/` with reason; do not erase history without a Decision Log entry.
