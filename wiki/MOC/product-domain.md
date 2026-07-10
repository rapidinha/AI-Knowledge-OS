# Product domain

Hub for learning flows, olympiad, enrollment, rewards, notifications, and client apps.

## Principles

- [[principles/webhook-ingestion-via-queues]] - Payment and provider-event domains where external events must become durable internal commands.
- [[principles/bulk-import-via-command-queues]] - Enrollment and access imports that outgrow a single request/worker path.

## Case studies

- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] - Tangram enrollment payment webhooks and olympiad import orchestration.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
