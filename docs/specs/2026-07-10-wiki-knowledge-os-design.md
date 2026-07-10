# Design: Engineering Wiki Knowledge OS

**Status:** Approved  
**Date:** 2026-07-10  
**Language:** English  
**Source corpus:** Tangram Platform monorepo (`/Users/matheusborges/github/tangram-platform`)  
**Output repo:** AI-Knowledge-OS (`/Users/matheusborges/github/AI-Knowledge-OS`)

## Goal

Build a portable, Obsidian-style wiki of engineering knowledge extracted from a real SaaS monorepo, split into:

1. **Principles** — company-agnostic patterns reusable in any project
2. **Tangram case studies** — how those patterns appear (or are bent) in Tangram, with file evidence
3. **Extraction ledger** — what was extracted, what remains, brief for subsequent waves

## Non-goals

- Copying source code, secrets, or Terraform state
- Continuous automated ingestion (markdown + ledger only in this phase)
- Deep dive into legacy `terraform/` (v1); infra case study uses **`terraform-v2` only**

## Architecture

```
AI-Knowledge-OS/
├── README.md
├── wiki/
│   ├── index.md
│   ├── MOC/                         # Maps of Content (hubs)
│   ├── principles/                  # ZERO Tangram names/paths/products
│   ├── case-studies/tangram/        # Evidence-backed case notes
│   └── _meta/
│       ├── templates.md
│       ├── coverage-matrix.md       # topic × source × status
│       └── extraction-ledger.md     # wave log + next-wave brief
└── docs/
    ├── specs/
    └── plans/
```

### Hard rules

| Tree | Rule |
|------|------|
| `wiki/principles/` | No company names, repo names, service names, absolute paths, or product brands |
| `wiki/case-studies/tangram/` | Must cite evidence paths under tangram-platform; may name services/ADRs |
| Cross-links | Principles ↔ case studies via `[[wikilinks]]`; MOCs link both |

### Note template (both trees)

1. Title + one-line **When to use**
2. Body (decisions, mechanics)
3. **Trade-offs**
4. **Anti-patterns**
5. Principles only: **Checklist for a new project**
6. Case studies only: **Evidence** (paths) + **Deviations**
7. `[[wikilinks]]` footer

## Coverage (full monorepo)

Every row in `coverage-matrix.md` must end as `extracted`, `partial` (with gap note), or `out-of-scope` (with reason). Initial topic set:

| Domain | Topics |
|--------|--------|
| Architecture | Diplomat / layered I/O boundaries; microservices + shared DB schemas; git submodules monorepo; shared auth library |
| Security | Cognito + platform JWT; PBAC scopes; service accounts / API keys; contextual permissions |
| Data | TypeORM entities/migrations; lookup tables; audit logs; multi-channel content distribution |
| Async / scale | SQS webhooks & imports; Redis cache; specialized read-model cache; workers/streaming imports |
| Infra | terraform-v2 multi-env single state; ECS/ALB/Cognito/SQS/RDS Proxy; feature flags (Unleash) |
| Engineering | Contract codegen + CI; agent rules (`.cursor`); docs/ADRs; automated-test seed scenarios; observability |
| Product domain | Challenge/session/resume; olympiad cross-service; enrollment/payment; rewards/wallet/ranking; notification channels; frontends (web/admin/mobile) |

## Extraction waves

| Wave | Focus |
|------|--------|
| W1 | Scaffold + Auth/PBAC + terraform-v2 + Diplomat + contracts/monorepo + MOCs skeleton + ledger |
| W2 | Enrollment async, Rewards ranking cache, Catalog modeling, Learning sessions |
| W3 | Notification, demo provisioning, frontends, DX/Makefile, observability, `.cursor`/`.github`/`docs` |
| W4 | ADR sweep, hypothesis confirm/reject, coverage close-out, final next-extraction brief |

## Success criteria

- [ ] Wiki navigable from `wiki/index.md`
- [ ] Principles contain no Tangram leakage
- [ ] Every coverage-matrix row has a terminal status
- [ ] `extraction-ledger.md` summarizes extracted knowledge and lists next-wave priorities
- [ ] Case studies cite real paths from `origin/main` (or documented working tree) evidence

## Spec self-review

- No TBD placeholders for structure
- Principles vs case-study boundary is unambiguous
- Full-repo coverage is via matrix + waves, not a single unbounded dump
- Infra scope locked to terraform-v2
