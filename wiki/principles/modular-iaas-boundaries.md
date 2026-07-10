# Modular IaaS Boundaries

**When to use:** Use this pattern when infrastructure spans networking, persistence, identity, compute, routing, storage, async work, and delivery pipelines.

## Body

Give each module one infrastructure responsibility and one stable contract. A networking module should expose subnet and security-boundary outputs. A persistence module should own database and cache resources. An identity module should own the managed identity provider and its client metadata. A compute module should own container runtime, task roles, logs, repositories, and service definitions. A routing module should own listener rules and target groups.

The root stack should orchestrate module relationships rather than hiding business decisions inside modules. It wires persistence outputs into secrets, secrets into compute, compute target groups into routing, queue URLs into services, and public endpoints into DNS or hosted frontend delivery.

Reusable modules work best when their inputs describe policy decisions and their outputs describe capabilities. For example, a queue module can expose URL and ARN while accepting visibility timeout, retry count, encryption key, and tags. Consumers should not reach into another module's internal resource names.

## Trade-offs

- Clear module ownership makes infrastructure review easier by concern.
- Stable outputs reduce coupling between teams and infrastructure layers.
- Root orchestration can become dense because it shows every cross-module dependency.
- Over-splitting creates many small modules with little reuse value.

## Anti-patterns

- Letting application modules create their own networks, databases, or routing rules independently.
- Passing raw internal resource names across modules instead of intentional outputs.
- Creating generic modules so broad that ownership and review responsibility become unclear.
- Hiding production-only behavior inside modules without surfacing the toggle at the root.

## Checklist for a new project

- [ ] Name each module after the infrastructure boundary it owns.
- [ ] Expose only outputs that consumers need to compose the platform.
- [ ] Keep cross-module wiring in the root stack unless a boundary has a strong reason to own it.
- [ ] Add reusable modules for repeated resource shapes such as queues or functions.
- [ ] Review module inputs for policy clarity before adding new conditionals.

## Case studies

- [[MOC/infrastructure]] — Evidence and implementation examples for this pattern.

## Related

- [[principles/multi-env-terraform-single-state]]
- [[principles/ignore-changes-and-secret-hygiene-in-iac]]
- [[MOC/infrastructure]]
