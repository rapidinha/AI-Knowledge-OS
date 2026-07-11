---
date: {{date}}
status: open
generated_by: {{generated_by}}
providers: {{providers}}
signal_count: {{signal_count}}
opportunity_count: {{opportunity_count}}
---

# Daily Leverage Radar — {{date}}

## Executive Summary

{{executive_summary}}

## Top Opportunities

{{#opportunities}}
### {{rank}}. {{title}}

- **Topic:** [[journals/radar/topics/{{topic_slug}}|{{topic_title}}]]
- **Category:** {{category}}
- **Recurrence:** hits {{hit_count}} · first {{first_seen}} · providers {{provider_set}}
- **Scores:** {{scores_inline}}
- **Why:** {{rationale}}
- **Sources:** {{sources_md}}
- **Decide:** `pending` <!-- agent sets: ignore | watch | research | known | merge -->

{{/opportunities}}

## Highest ROI

| Kind | Opportunity |
|------|-------------|
| Learning | {{roi_learning}} |
| Content | {{roi_content}} |
| Project | {{roi_project}} |

## Worth Watching

{{worth_watching}}

## Ignore

{{ignore_list}}

## Signals

Raw: `journals/radar/_raw/{{date}}.jsonl`

## Topics

Index: `journals/radar/topics/_index.md` · Graph: `journals/radar/topics.yaml` (private)

