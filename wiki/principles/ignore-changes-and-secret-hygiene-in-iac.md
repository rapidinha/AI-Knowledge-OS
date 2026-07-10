# Lifecycle Drift Exceptions and Secret Hygiene in IaC

**When to use:** Use this pattern when generated artifacts, runtime scaling, or secret values cause infrastructure plans to show noise instead of meaningful change.

## Body

Keep secret ingress outside committed configuration. Use a local environment file for operator-supplied secret values, commit only an example file with empty or placeholder values, and load the local file through a wrapper so operators run plans and applies consistently. Mark secret inputs as sensitive and write real runtime values to managed secret or parameter storage.

Use lifecycle drift exceptions only for resources with a documented reason. Common cases include generated package hashes that vary by machine, secret values whose authoritative copy lives in the cloud control plane, and capacity fields changed by scheduled scaling. Every exception should name what is ignored, why it is ignored, and how to intentionally change it.

The operational runbook matters as much as the lifecycle setting. To change a protected field, temporarily remove the exception, run a focused plan, apply only the intended change, restore the exception, and commit the code. This prevents permanent blind spots while still avoiding repeated accidental diffs.

## Trade-offs

- Plans stay focused on intentional infrastructure changes.
- Secrets avoid direct commits and can be rotated through managed storage.
- Drift exceptions can hide real configuration decay if they are too broad.
- Local secret files make operator setup simple but require strong repository hygiene.

## Anti-patterns

- Ignoring entire resource definitions when only one generated or secret field is noisy.
- Committing real secret values, state files, or local operator environment files.
- Adding lifecycle exceptions without a documented change procedure.
- Treating placeholder values as a substitute for managed secret rotation.

## Checklist for a new project

- [ ] Commit an example environment file with placeholders only.
- [ ] Keep real environment files, state, and plan artifacts out of version control.
- [ ] Mark secret variables as sensitive and store runtime values in managed secret storage.
- [ ] Document every lifecycle drift exception in a table or runbook.
- [ ] Test the temporary-unignore procedure before relying on it during an incident.

## Case studies

- [[MOC/infrastructure]] — Evidence and implementation examples for this pattern.

## Related

- [[principles/multi-env-terraform-single-state]]
- [[principles/modular-iaas-boundaries]]
- [[MOC/infrastructure]]
