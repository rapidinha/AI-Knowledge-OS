# Content Distribution By Channel

**When to use:** Use this pattern when the same content object must be available to different audience channels under different eligibility criteria.

## Body

Separate the content object from the rule that decides who can see it. The content record should own stable authoring fields, while distribution records map it to audience channels such as consumer, institution, cohort, partner, or internal segments.

Model a small base distribution row with the common content id and channel type, then store channel-specific criteria in dedicated rows or structured fields. This keeps shared queries simple while avoiding a sparse table full of optional fields that apply to only one channel.

Eligibility should be deterministic: given a channel and its criteria, the system can find matching content ids, then apply availability, publication, or completion rules separately. When a channel requires multiple criteria, require all of them at write time instead of discovering incomplete rules during reads.

Use stable lookup codes for channel types and rule categories. Numeric ids are efficient in storage, but business logic and APIs should speak in codes or constrained enums so adding a new channel does not scatter magic numbers across the service.

## Trade-offs

- Content can evolve independently from audience targeting.
- Channel-specific criteria stay explicit and easier to validate.
- Discovery reads can index by channel and criteria instead of scanning all content.
- The model adds joins and replacement logic when an operator edits distribution rules.
- New channels require schema, repository, validation, and migration work instead of only adding a JSON key.

## Anti-patterns

- Embedding every audience rule directly on the content row.
- Using a single generic JSON blob without validation for required channel criteria.
- Letting read paths decide how to handle incomplete distribution rows.
- Hard-coding lookup ids throughout application logic.
- Mixing temporal availability rules into channel targeting when they change at different times.

## Checklist for a new project

- [ ] Define the content record separately from its distribution rules.
- [ ] Create one canonical channel type lookup with stable codes.
- [ ] Validate required criteria for each channel at write time.
- [ ] Add indexes for the channel and criteria combinations used by discovery reads.
- [ ] Replace a content item's distribution set transactionally when operators edit it.
- [ ] Keep time windows, publication state, and prerequisite checks as separate eligibility layers.

## Case studies

- [[MOC/data-persistence]] - Persistence examples for lookup-backed distribution models.
- [[MOC/product-domain]] - Product-domain examples where audience targeting controls content access.

## Related

- [[principles/temporal-orchestration-of-content]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/data-persistence]]
- [[MOC/product-domain]]
