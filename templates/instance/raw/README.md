# Raw layer (immutable inputs + ops)

Human-curated sources and operational artifacts. The LLM **reads** this layer; it does not rewrite history in place.

| Path | Role |
|------|------|
| `sources/<slug>/` | Ingest — primary sources |
| `research/<slug>/` | Secondary research (not wiki truth yet) |
| `ops/` | Daily notes, posts, Leverage Radar, experiments |

Compiled knowledge lives in [`wiki/`](../../wiki/index.md). Schema: [`wiki/_meta/llm-wiki-schema.md`](../../wiki/_meta/llm-wiki-schema.md).
