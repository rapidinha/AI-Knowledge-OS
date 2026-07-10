# Multi-client Same API Contracts

**When to use:** Use this pattern when web, admin, mobile, or partner clients must consume the same backend capability without drifting into separate API shapes.

## Body

Keep the provider API contract as the shared compatibility surface. Each client can have its own framework, routing model, state library, and runtime constraints, but the request and response shapes should come from the same machine-readable contract.

Generated clients help make the contract concrete. A browser app may generate query hooks, a dashboard may generate fetch helpers, and a native shell may call a small subset through a bridge or service-specific mutator. The important invariant is that the endpoint path, DTO fields, response fields, and auth expectations are reviewed as one provider contract, not reinvented per client.

Client-specific routing belongs near the client boundary. Local proxies, service prefixes, server rewrites, and native bridges can adapt the runtime URL without changing the API contract. This lets each client run in its natural development mode while still compiling against the same backend shape.

## Trade-offs

- Teams get compile-time or build-time feedback when provider contracts drift.
- Clients can use different runtimes while sharing endpoint semantics.
- Generated code can be noisy and should be reviewed as compatibility evidence, not hand-edited design source.
- Some clients may intentionally consume only a subset, so contract coverage must be explicit.

## Anti-patterns

- Hand-writing slightly different DTOs in each client.
- Letting local proxy paths become public API paths.
- Treating generated client files as optional when provider routes or DTOs change.
- Adding a native bridge call that bypasses auth, validation, or the documented provider route.
- Assuming one client's successful build proves every other client remains compatible.

## Checklist for a new project

- [ ] Publish one machine-readable contract per provider service.
- [ ] Generate client code into clearly named generated directories.
- [ ] Keep client runtime URL adaptation outside the provider contract.
- [ ] Build or typecheck each important client against the generated contract.
- [ ] Document which clients are contract-gated in CI and which remain manual.
- [ ] Review generated diffs for removed fields, renamed enums, and route changes.

## Case studies

- [[MOC/product-domain]] - Product-domain examples where multiple client apps share backend capability.
- [[MOC/engineering-practice]] - Engineering examples where generated contracts and CI protect compatibility.

## Related

- [[principles/generated-api-clients-and-contract-ci]]
- [[principles/pluggable-notification-providers]]
- [[MOC/product-domain]]
- [[MOC/engineering-practice]]
