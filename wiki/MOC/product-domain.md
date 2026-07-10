# Product domain

Hub for learning flows, olympiad, enrollment, rewards, notifications, and client apps.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Payment and provider-event domains where external events must become durable internal commands.
- [[principles/bulk-import-via-command-queues]] - Enrollment and access imports that outgrow a single request/worker path.
- [[principles/specialized-read-model-cache]] - Ranking or progress views whose active read path needs bounded latency.
- [[principles/wallet-ledger-style-balances]] - Product balances stored for fast reads while every mutation remains ledgered.
- [[principles/content-distribution-by-channel]] - Content access rules that differ by audience channel or enrollment context.
- [[principles/temporal-orchestration-of-content]] - Product content released by event windows, calendar schedules, and operator-managed timing.
- [[principles/timed-session-resume]] - Learning or assessment sessions that must survive reload, pause, abandon, and resume.
- [[principles/streaming-bulk-file-import-workers]] - Operator-imported evaluation or review spreadsheets processed in bounded chunks.
- [[principles/pluggable-notification-providers]] - Product notifications that span push, email, SMS, devices, campaigns, and scheduled sends.
- [[principles/multi-client-same-api-contracts]] - Product APIs consumed by web, admin, mobile, or partner clients without contract drift.

## Related

- [[index]]
- [[MOC/engineering-practice]]
- [[MOC/async-scale]]
- [[_meta/coverage-matrix]]
