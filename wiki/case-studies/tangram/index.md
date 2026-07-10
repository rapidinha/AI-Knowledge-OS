# Tangram case studies

Evidence-backed notes from the Tangram Platform monorepo. Each case study links to one or more [[principles/<slug>|principle]] notes and cites repo-relative paths.

**Rules:**

- Service names, ADRs, and `tangram-platform` paths are allowed
- No secrets, credentials, or Terraform state
- Infra evidence uses **terraform-v2** only

## Case studies

- [[case-studies/tangram/diplomat-architecture]] — Diplomat service layers, logic sandwich, pure logic, and async/cache deviations.
- [[case-studies/tangram/identity-pbac-and-auth]] — JWT auth, PBAC scopes, service accounts, and S2S API keys.
- [[case-studies/tangram/terraform-v2-platform]] — terraform-v2 multi-env state, module boundaries, lifecycle exceptions, and secret handling.

## Related

- [[index]]
- [[MOC/architecture]]
- [[MOC/security-authz]]
- [[MOC/data-persistence]]
- [[MOC/async-scale]]
- [[MOC/infrastructure]]
- [[MOC/engineering-practice]]
- [[MOC/product-domain]]
- [[_meta/templates]]
- [[_meta/coverage-matrix]]
