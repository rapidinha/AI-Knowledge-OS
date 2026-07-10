# Agent Rules As Living Standards

**When to use:** Use this pattern when AI-assisted development should follow team standards that evolve with the codebase.

## Body

Treat agent rules as executable documentation for contributors and coding agents. A rule should state when it applies, which files it covers, whether it is always active, and what behaviors it enforces. This makes standards visible at the same time code is being written or reviewed.

Rules work best when they encode stable expectations: architecture boundaries, security constraints, migration workflow, style conventions, investigation process, review gates, and local tooling. Prefer precise rules with scoped file globs over broad advice that applies everywhere but guides nothing.

Deprecation should be explicit. When a rule is replaced, keep a small forwarding note that names the current rule and disables automatic application. This avoids stale duplicate guidance while preserving discoverability for people and agents that still search for the old topic.

## Trade-offs

- Standards stay close to the repository and can evolve through review.
- Agents receive context before generating code, reducing repeated reviewer feedback.
- Always-active rules can overload simple tasks if they become too broad.
- Rule drift is possible when rules are updated without matching code or workflow changes.

## Anti-patterns

- Keeping conflicting rules active for the same file set.
- Encoding aspirational architecture that the current codebase does not follow.
- Hiding critical security rules behind optional or rarely matched globs.
- Deleting deprecated rules without a forwarding trail when contributors still reference them.
- Using rules as a substitute for tests, linters, or CI gates.

## Checklist for a new project

- [ ] Add frontmatter for description, file scope, and automatic application.
- [ ] Separate architecture, security, workflow, and tool-specific rules.
- [ ] Keep always-active rules short enough to influence code generation.
- [ ] Mark replaced rules as deprecated and point to the current rule.
- [ ] Review rules when architecture decisions or CI gates change.
- [ ] Back critical rules with tests, linters, or review checklists.

## Case studies

- [[MOC/engineering-practice]] - Engineering examples for repository-owned agent rules and review workflow standards.

## Related

- [[principles/architecture-decision-records]]
- [[principles/generated-api-clients-and-contract-ci]]
- [[MOC/engineering-practice]]
