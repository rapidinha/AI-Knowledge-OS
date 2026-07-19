---
date: {{date}}
status: open
generated_by: {{generated_by}}
---

# Sales Motion Verdict — {{date}}

## Beachhead: {{beachhead_title}}

- **Composite score:** {{composite_score}} (go ≥ {{go_threshold}} · watch ≥ {{watch_threshold}})
- **Evidence floor:** {{evidence_floor_met}} (signals {{signal_count}} ≥ {{min_signals_for_go}} · sources {{distinct_sources}} ≥ {{min_sources_for_go}})
- **Deterministic recommendation:** {{recommendation}}
- **Override rationale (if any):** {{override_rationale}}

## Decision

**Decide:** `pending` <!-- founder answers in chat: go | watch | no-go | pivot -->

## Evidence

{{evidence_signals}}
