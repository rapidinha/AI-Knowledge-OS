# Stage: ICP & Dor (S1)

## Input

- `templates/sales/config.example.yaml` (if `raw/ops/sales/config.yaml` does not exist yet)
- Founder answers, gathered one question at a time in chat

## Output expectations

- Ask, one at a time: `product` (what's being sold), `goal` (what this run optimizes for),
  ICP **by language** ("who says X", not demographics), pain lexicon seed terms
  (intensity / workaround / willingness-to-pay), which channels to enable
  (`hn`, `reddit`, `rss`, `x_manual`).
- Write answers into `raw/ops/sales/config.yaml`.
- Summarize the built config back to the founder before moving to S2.

## Caps

- One question per message — do not batch the whole config into a single ask.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **No** proceeding to S2 without an explicit founder approval of the built config.
