# Design: Engineering Wiki Knowledge OS

**Status:** Superseded in part by [GOVERNANCE.md](../../GOVERNANCE.md)  
**Date:** 2026-07-10  

## Goal

Maintain a portable engineering wiki of reusable principles and optional public case studies.

## Non-goals

- Publishing personal vaults or employer-internal corpora by default
- Requiring named-system case studies for every principle
- Copying secrets or source blobs into the wiki

## Architecture

```
AI-Knowledge-OS/
├── README.md
├── GOVERNANCE.md
├── templates/personal-lab/   # structure for private SoTs
├── wiki/
│   ├── index.md
│   ├── MOC/
│   ├── principles/           # company-agnostic
│   ├── case-studies/         # optional public systems only
│   └── _meta/
└── docs/
```

### Hard rules

| Tree | Rule |
|------|------|
| `wiki/principles/` | No company names, repo names, service names, absolute paths, or product brands |
| `wiki/case-studies/<system>/` | Only when intentionally public; evidence paths allowed; no secrets |

## Success criteria

- [x] Wiki navigable from `wiki/index.md`
- [x] Principles contain no company leakage
- [x] Public tree does not publish employer-specific case-study corpora by default
