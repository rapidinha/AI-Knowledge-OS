# Clients, DX, And Meta Practices (Tangram)

**When to use:** Read this case study when you need the concrete Tangram evidence for Notification providers, multi-client API consumption, local development presets, agent rules, ADRs, and GitHub metadata.

## Body

Tangram's Notification service uses channel lookup rows and provider adapters rather than one hard-coded delivery path. `CreateCampaignDto` accepts a channel constrained by `NOTIFICATION_CHANNEL`, `001-notification-channels.seed.ts` seeds `push`, `email`, and `sms`, and `CampaignController` chooses `ExpoPushProvider`, `SesProvider`, or `SnsProvider` by channel code. Delivery writes one `Notification` row per recipient with channel, recipient id/address, status, timestamps, external id, campaign id, and error message, while campaign counters and per-channel metrics are updated after provider results.

Scheduling is a separate provider boundary. `CampaignController.create` and `update` create or replace schedules through `EventBridgeProvider` when `scheduledAt` is present, `cancel` deletes schedules, and `processScheduled` returns scheduled campaigns to the normal send path. This keeps scheduling infrastructure out of the channel providers, but the current provider names and logs still expose AWS and Expo implementation choices inside the service.

The client surface is split across `apps/web`, `apps/backoffice`, and `apps/mobile`. The web app is a Next.js app with service rewrites in `next.config.mjs`, Orval-generated React Query clients under `src/api/generated/*`, and per-service fetch mutators such as `notification-fetch.ts`. The backoffice app is a Vite app with Orval projects for identity, organization, enrollment, catalog, notification, learning, and rewards, plus `check:contracts` to fail when generated files drift. The mobile app is an Expo/React Native WebView shell: `app/index.tsx` loads the web app URL, collects an Expo push token, injects `TangramNative`, and lets the web page register the token through the Notification `devices` endpoint.

Tangram's local DX centers on presets. The root `Makefile` includes `make/dev.mk`, which exposes `make dev`, `dev-presets`, `dev-preset`, `dev-last`, `dev-stop`, `dev-ps`, `doctor`, `setup-native`, `staging-config`, and CodeRabbit review aliases. `docs/desenvolvimento-workflow.md` explains the contract: native mode uses `NO_DOCKER=1`, Docker is optional, and hybrid presets can run selected local services while routing the rest to staging through a generated gateway. `config/dev/services.yaml` is the service catalog, `config/dev/presets/*.yaml` are reusable presets, and `scripts/dev/preset.sh` generates ignored frontend env files, service env files, Caddy config, process metadata, and known-limitation output.

Repository meta practices are similarly explicit. `.cursor/rules/*.mdc` frontmatter scopes agent rules by `globs` and `alwaysApply`; security and NestJS architecture rules are always active for service TypeScript, while `diplomat-architecture.mdc` is intentionally deprecated and points to `nestjs-architecture.mdc`. `.github/CODEOWNERS` assigns backend, frontend, devops, and tech-lead ownership; `.github/pull_request_template.md` asks for local tests, generated API clients after contract changes, CodeRabbit review, and no secrets or `.generated/`; root contract workflows regenerate backoffice clients and build the consumer; the web app has a custom PR workflow with static checks, four Vitest coverage shards, and an 80% patch coverage gate; the mobile workflow builds and submits Expo/EAS profiles for internal and production release paths.

Tangram has a brief ADR set rather than a full index in this extraction. `docs/architecture/ADR-001` covers seasonal challenge temporal orchestration, `ADR-002` covers Asaas B2C payment integration, `ADR-003` covers session resume, `ADR-004` covers the unified challenge engine, `ADR-005` proposes catalog audit evolution, `ADR-006` accepts user lifecycle lazy expiration, and `ADR-arc42-template.md` supplies the longer decision-record template. A full ADR index remains intentionally deferred to Task 10.

## Trade-offs

- Tangram can evolve notification channels by changing provider adapters and channel-specific recipient resolution instead of rewriting campaign APIs.
- Web and backoffice compile against generated service contracts while preserving their different routing and runtime models.
- The mobile WebView shell reuses the web app and adds native push, secure storage, network, theme, and tracking bridges without rebuilding the whole product UI natively.
- Native/hybrid dev presets reduce local startup cost and keep the full Docker stack optional.
- Agent rules, CODEOWNERS, PR templates, contract CI, and ADRs make standards reviewable in the repository.
- Notification provider classes currently leak vendor-specific names into service code, and only backoffice has root contract validation in the researched workflows.
- The mobile bridge directly calls the Notification service from the native shell, so its contract coverage is not generated the same way as web/backoffice clients.

## Anti-patterns

- Tangram avoids hand-editing most generated web/backoffice API clients; drift is handled by generation scripts and contract checks.
- Tangram avoids making full Docker the only local workflow; common presets use native processes and staging fallbacks.
- Tangram avoids silently removing old agent guidance; the deprecated Diplomat rule forwards to the active NestJS architecture rule.
- Current risk: notification scheduling catches provider errors during create/update/cancel but does not surface schedule failure to the campaign caller.
- Current risk: mobile bridge logs URLs, push token registration state, and device info during token registration; log policy should confirm this is acceptable outside development.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Notification channel seed | `services/notification-service/src/database/seeds/001-notification-channels.seed.ts` | Seeds `push`, `email`, and `sms` channel codes with provider-specific descriptions. |
| Campaign DTO | `services/notification-service/src/wire/in/campaign.dto.ts` | Validates channel, target type, message fields, data payload, and optional schedule timestamp. |
| Campaign orchestration | `services/notification-service/src/controllers/campaign.controller.ts` | Selects providers by channel code, schedules/cancels campaigns, resolves recipients, persists notification attempts, counters, and metrics. |
| Provider adapters | `services/notification-service/src/diplomat/providers/expo-push.provider.ts`, `ses.provider.ts`, `sns.provider.ts`, `eventbridge.provider.ts` | Implement push, email, SMS, and scheduler provider boundaries. |
| Notification persistence | `services/notification-service/src/diplomat/db/entities/campaign.entity.ts` and `notification.entity.ts` | Store campaign lifecycle, scheduled time, counters, delivery attempts, statuses, external ids, timestamps, and errors. |
| Notification HTTP contracts | `services/notification-service/src/diplomat/http-in/campaign.http.ts` and `device.http.ts` | Expose scoped campaign and device endpoints for generated clients and mobile token registration. |
| Web app contracts | `apps/web/package.json`, `apps/web/orval.config.ts`, `apps/web/src/api/mutator/notification-fetch.ts`, `apps/web/next.config.mjs` | Next.js app with Orval scripts, generated clients, service mutators, and service rewrites. |
| Backoffice contracts | `apps/backoffice/package.json`, `apps/backoffice/orval.config.ts`, `apps/backoffice/src/api/mutator/notification-fetch.ts`, `apps/backoffice/vite.config.ts` | Vite app with Orval projects, contract drift script, generated clients, service mutators, and dev proxy. |
| Mobile app shell | `apps/mobile/package.json`, `apps/mobile/app/index.tsx`, `apps/mobile/src/hooks/usePushNotifications.ts`, `apps/mobile/src/services/nativeBridge.ts`, `apps/mobile/app.config.ts`, `apps/mobile/eas.json` | Expo app loads the web app, handles push permission/token, injects the native bridge, registers devices, and defines build profiles. |
| Mobile release docs | `apps/mobile/README.md` and `apps/mobile/.github/workflows/release.yml` | Document EAS profiles, store submission, required secrets, and automated release workflow. |
| Local dev workflow | `docs/desenvolvimento-workflow.md`, `Makefile`, `make/dev.mk` | Document the native-first dev contract, root command surface, optional Docker path, and review aliases. |
| Dev presets and catalog | `config/dev/services.yaml`, `config/dev/presets/_template.yaml`, `backoffice-staging.yaml`, `native-organization.yaml`, `docker-full-local.yaml` | Define service ports, frontend commands, native/staging presets, and full-stack opt-in preset. |
| Dev scripts | `scripts/dev/compose-preset.sh` and `scripts/dev/preset.sh` | Compose interactive presets, generate frontend env, start selected services/frontends, and print known limitations. |
| Agent rules | `.cursor/rules/*.mdc` | Scope always-applied security, graph, NestJS, Ponytail, and workflow rules; keep service standards and migration rules optional. |
| Deprecated rule | `.cursor/rules/diplomat-architecture.mdc` | Marks the old Diplomat rule deprecated and points to `nestjs-architecture.mdc`. |
| Ownership and PR checklist | `.github/CODEOWNERS` and `.github/pull_request_template.md` | Assign reviewers and require tests, generated clients when contracts change, CodeRabbit, and no secrets/generated artifacts. |
| Contract workflows | `.github/workflows/backend-contract-check.yml` and `.github/workflows/backoffice-contracts.yml` | Regenerate backoffice clients, detect generated drift, and build backoffice against selected services. |
| Web PR workflow | `apps/web/.github/workflows/pr.yml` | Runs static checks, sharded tests, coverage merge, and patch coverage gate. |
| ADR docs | `docs/architecture/ADR-001-challenge-seasonal-temporal-orchestration.md`, `ADR-002-asaas-b2c-payment-integration.md`, `ADR-003-session-resume-time-is-money.md`, `ADR-004-challenge-engine.md`, `ADR-005-catalog-audit-system-evolution.md`, `ADR-006-user-lifecycle-lazy-expiration.md`, `ADR-arc42-template.md` | Brief ADR set for domain, integration, lifecycle, audit, and decision-record template evidence. |

## Deviations

- The generic provider principle hides provider brands behind channel adapters, while Tangram class names and seed descriptions currently name Expo, AWS SES, AWS SNS, and AWS EventBridge directly.
- The generic multi-client principle prefers all important clients to be contract-gated; Tangram root contract workflows gate backoffice, while web has generated clients and a PR workflow but not the same root contract check in the researched files.
- The mobile app shares the web product through a WebView and native bridge instead of generating its own full API client surface.
- `ADR-005` is proposed, while `ADR-006` is accepted; readers should not treat every ADR file as shipped behavior.

## Principles

- [[principles/pluggable-notification-providers]] - Generalizes Tangram's Notification channel lookup, provider adapters, delivery attempts, and scheduler boundary.
- [[principles/multi-client-same-api-contracts]] - Generalizes Tangram's web, backoffice, and mobile client contract patterns.
- [[principles/local-dev-presets-without-full-docker]] - Generalizes Tangram's native/hybrid/full-stack dev preset workflow.
- [[principles/agent-rules-as-living-standards]] - Generalizes Tangram's scoped agent rules and deprecated-rule forwarding.
- [[principles/architecture-decision-records]] - Generalizes Tangram's ADR set and status-aware decision documentation.
- [[principles/generated-api-clients-and-contract-ci]] - Connects Tangram's generated client drift checks to the existing contract CI pattern.

## Related

- [[case-studies/tangram/catalog-and-learning]]
- [[case-studies/tangram/monorepo-contracts-and-common]]
- [[case-studies/tangram/index]]
- [[MOC/product-domain]]
- [[MOC/engineering-practice]]
- [[MOC/async-scale]]
- [[MOC/architecture]]
