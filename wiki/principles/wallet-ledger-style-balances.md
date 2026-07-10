# Wallet Ledger-Style Balances

**When to use:** Use this pattern when a product balance must be fast to read while every mutation remains auditable, attributable, and safe under concurrent credits or debits.

## Body

Keep a wallet row for the current balance, but make every balance mutation create a ledger transaction in the same database transaction. The wallet balance is the read-optimized snapshot; the transaction table is the history of how the snapshot changed.

Each transaction should record the wallet id, amount, resulting balance, transaction type, source type, optional source id, actor, timestamps, and domain metadata needed for statements, support, and downstream eligibility. Store enough source information to detect or prevent duplicate credits from the same business event.

Balance-changing writes should run at a strong isolation level and lock the wallet row before calculating the new balance. The write order is: load wallet with a write lock, calculate the new balance, insert the transaction with `balanceAfter`, update the wallet balance, and commit. Reads can use the wallet row for balance and the transaction table for statements or period summaries.

Initial balances should follow the same rule. If a wallet starts with a non-zero amount, create an initialization transaction in the same creation transaction. Avoid hidden "opening balance" state that does not appear in the ledger.

Domain controllers should validate ids and business rules before calling the repository mutation, but they should not hand-edit balances. Centralize balance mutation in one repository or domain service so future credits, debits, prizes, adjustments, and imports all share the same concurrency and audit behavior.

## Trade-offs

- Balance reads stay fast without summing the full transaction history.
- Statements, support investigations, and audits can explain every mutation.
- Strong transaction isolation and row locks prevent lost updates under concurrent credits.
- Duplicate-source constraints can make event replay safer.
- The design writes more data and requires careful transaction boundaries.
- The stored balance can drift if any path bypasses the ledger mutation API.

## Anti-patterns

- Updating a wallet balance directly without inserting a matching transaction.
- Recomputing current balance from all transactions on every user request.
- Creating initial balances without ledger entries.
- Letting multiple controllers implement their own balance math.
- Relying on application-level reads without row locks for concurrent mutations.
- Omitting source identifiers, actors, or resulting balances from the transaction record.

## Checklist for a new project

- [ ] Define wallet, wallet type, and transaction tables before exposing balance reads.
- [ ] Store `amount`, `balanceAfter`, source metadata, actor, and timestamps on every transaction.
- [ ] Centralize all balance mutations behind one API.
- [ ] Use a database transaction and row-level write lock around balance mutation.
- [ ] Insert an initialization transaction for non-zero starting balances.
- [ ] Add duplicate-source constraints or idempotency checks for replayable business events.
- [ ] Keep statement queries paginated or bounded by period.
- [ ] Add tests proving a mutation inserts a transaction and updates the wallet in one transaction.

## Case studies

- [[MOC/product-domain]] - Evidence and implementation examples for product wallets, credits, prizes, and statements.

## Related

- [[principles/pure-domain-logic-no-io]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/product-domain]]
