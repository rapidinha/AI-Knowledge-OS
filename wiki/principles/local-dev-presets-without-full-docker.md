# Local Dev Presets Without Full Container Stack

**When to use:** Use this pattern when a monorepo has many services but most daily work needs only one or two local services plus stable remote dependencies.

## Body

Make local development a selectable preset, not a single all-or-nothing stack. A preset should define the frontend, runtime mode, local services, remote service fallback, environment source, gateway settings, and service-specific overrides. The default path should start only the processes needed for the current task.

Keep the root command surface small. The root task runner should expose memorable aliases such as interactive dev, list presets, run preset, repeat last preset, stop, and status. The real orchestration should live in scripts that can parse preset files, generate temporary env files, create a gateway config, start native service processes, and clean up generated artifacts.

Hybrid presets should route local service paths to localhost and all other service paths to a shared environment. Known gaps, such as webhooks, queues, object storage, or identity emulators, should be printed as limitations instead of hidden as partial behavior. Generated env, process ids, logs, and gateway config should be ignored by version control.

## Trade-offs

- Developers can start faster because they run only the services needed for the task.
- Shared environments keep complex dependencies available without recreating them locally.
- Presets make common setups repeatable and reviewable.
- Hybrid routing can hide integration issues that only appear in a full local or CI environment.
- Remote dependencies require network access and careful secret handling.

## Anti-patterns

- Putting long orchestration logic directly in the root task file.
- Committing generated env files, local process metadata, or gateway config.
- Making every team-specific experiment a permanent alias.
- Pretending unsupported local integrations work instead of printing limitations.
- Requiring the full stack for frontend-only or single-service changes.

## Checklist for a new project

- [ ] Define a service catalog with ports, health checks, and frontend commands.
- [ ] Store reusable presets as small declarative files.
- [ ] Add an interactive selector for one-off hybrid combinations.
- [ ] Generate local env and gateway config into ignored directories.
- [ ] Provide stop and status commands that understand native and full-stack sessions.
- [ ] Document known local limitations and the CI or remote path that covers them.
- [ ] Keep the root task file as aliases plus script delegation.

## Case studies

- [[MOC/engineering-practice]] - Engineering examples for presets, scripts, and local workflow maintenance.

## Related

- [[principles/generated-api-clients-and-contract-ci]]
- [[principles/multi-client-same-api-contracts]]
- [[MOC/engineering-practice]]
