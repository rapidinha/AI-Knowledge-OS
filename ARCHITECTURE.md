# Architecture

AI Knowledge OS is a **Protocol Kernel**.

## Layers

| Layer | Role | Replaceable? |
|-------|------|--------------|
| Contracts | Artifact schemas | No (versioned) |
| Engine cycle | capture → contextualize → decide → learn → produce | No |
| Wiki schema | Knowledge Base categories + templates | Via RFC |
| Agents | Skill packs | Yes |
| Providers | Signal/source adapters | Yes |
| Integrations | Tool adapters | Yes |
| Instance store | User markdown/YAML | Yes |

## OSS vs instance

- **OSS** ships protocols, scaffold, reference providers, and docs.
- **Instance** holds the living Knowledge Base (`wiki/`) and personal trees.
- Sync policy: **instance wiki wins**; scaffold only creates missing files.

See [GOVERNANCE.md](GOVERNANCE.md) and [engine/invariants.md](engine/invariants.md).
