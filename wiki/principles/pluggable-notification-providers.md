# Pluggable Notification Providers

**When to use:** Use this pattern when a product sends notifications through multiple delivery channels and each channel needs a replaceable vendor adapter.

## Body

Model the notification domain around channel codes, campaigns, recipients, delivery attempts, and statuses. Channel codes such as push, email, and text message should be stable business values. Provider classes should translate a generic send request into a vendor-specific API call and return a normalized delivery result.

The orchestration layer chooses the provider by channel code, resolves recipients, batches delivery when the provider supports it, and stores one delivery attempt per recipient. The stored attempt should include the channel, recipient id or address, message fields, campaign id if present, status, provider external id, timestamps, and error message.

Scheduling is another provider boundary. A campaign can store its scheduled time and delegate the wake-up to a scheduler provider, while immediate delivery and scheduled delivery still converge on the same send path. This keeps campaign lifecycle, recipient targeting, and delivery accounting independent from the provider used to trigger the send.

## Trade-offs

- Adding a channel usually means adding one provider adapter plus channel-specific recipient resolution.
- Delivery attempts become auditable across providers because success, failure, external ids, and errors share one shape.
- Provider-specific capabilities can be harder to expose without leaking vendor details into the campaign API.
- Per-recipient persistence adds write load for large campaigns, so batching and retention policy matter.

## Anti-patterns

- Letting application code call provider SDKs directly from many feature modules.
- Treating all provider failures as transport errors instead of storing failed delivery attempts.
- Encoding channel names as scattered strings instead of stable lookup values or enums.
- Making scheduled delivery a separate code path that bypasses normal validation, status, and metrics.
- Assuming push tokens, email addresses, and phone numbers can be validated or resolved the same way.

## Checklist for a new project

- [ ] Define stable channel codes and delivery statuses.
- [ ] Keep provider adapters behind a normalized send-result contract.
- [ ] Persist one delivery attempt per recipient with external ids and errors.
- [ ] Resolve recipients before provider calls and handle empty audiences explicitly.
- [ ] Batch provider calls under documented provider limits.
- [ ] Route scheduled campaigns back into the same immediate-send path.
- [ ] Track send/failure metrics by channel.

## Case studies

- [[MOC/product-domain]] - Product-domain examples where notifications span channels, campaigns, devices, and client apps.
- [[MOC/async-scale]] - Async examples where scheduled work triggers normal delivery paths.

## Related

- [[principles/content-distribution-by-channel]]
- [[principles/temporal-orchestration-of-content]]
- [[MOC/product-domain]]
- [[MOC/async-scale]]
