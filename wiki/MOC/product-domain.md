# Product domain

Hub for learning flows, olympiad, enrollment, rewards, notifications, and client apps.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Payment and provider-event domains where external events must become durable internal commands.
- [[principles/bulk-import-via-command-queues]] - Enrollment and access imports that outgrow a single request/worker path.
- [[principles/specialized-read-model-cache]] - Ranking or progress views whose active read path needs bounded latency.
- [[principles/wallet-ledger-style-balances]] - Product balances stored for fast reads while every mutation remains ledgered.

## Case studies

- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] - Tangram enrollment payment webhooks and olympiad import orchestration.
- [[case-studies/tangram/rewards-ranking-cache]] - Tangram Rewards ranking cache, wallet transactions, and prize distribution.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
