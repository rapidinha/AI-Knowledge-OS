# Streaming Bulk File Import Workers

**When to use:** Use this pattern when a spreadsheet or file import must validate many rows, persist partial successes, and return row-level errors without loading the whole workload into one transaction.

## Body

Process the file as a stream of validated chunks. The request path should enforce file size and content type, then hand the file to a reader that yields bounded chunks containing valid rows, invalid rows, processed row counts, and a checkpoint such as the last row number.

Keep structural parsing separate from database validation. The reader should validate headers, sheet selection, row shape, duplicate ids, score ranges, required text, and other in-file constraints. The persistence worker should validate whether referenced records exist, whether rows are in scope, and whether domain-specific type rules match current database state.

Persist each chunk in a transaction. Within that transaction, load all referenced rows for the chunk, build maps for efficient lookups, create any missing versions needed for auditability, upsert draft records, update selection or status tables, and return chunk-level counts plus row-level errors.

Aggregate counts outside the chunk transaction. The import coordinator should maintain cumulative processed, valid, and invalid counts across chunks. It should collect all row errors for the response or for a durable result table, depending on whether the import is synchronous or backgrounded.

Prefer bounded fallbacks over silent failure. If the streaming reader cannot inspect workbook metadata reliably, a buffered fallback may be acceptable under a strict memory cap. The fallback should preserve the same chunk contract so the rest of the worker pipeline does not change.

## Trade-offs

- Large files are bounded by chunk size and file limits rather than by one giant transaction.
- Row-level errors can be returned without aborting the whole import.
- Database validations can reuse repositories and transactions per chunk.
- The workflow is more complex than a single parse-and-save function.
- Synchronous imports still hold the request open, so very large or slow imports may need promotion to a queue-backed job model.
- Buffered fallbacks improve compatibility but must have hard memory ceilings.

## Anti-patterns

- Reading the whole workbook into application objects with no byte limit.
- Mixing row parsing, domain validation, and persistence in one loop with hidden state.
- Aborting the whole import on the first invalid row when partial success is acceptable.
- Writing each row in its own transaction when chunk-level atomicity is enough.
- Returning only aggregate failure counts with no row numbers or reason codes.
- Treating a synchronous chunked import as a replacement for a background job when the workload can exceed request limits.

## Checklist for a new project

- [ ] Enforce file size, content type, and maximum in-memory fallback size.
- [ ] Parse headers before reading data rows and reject unknown shapes early.
- [ ] Yield chunks with valid rows, invalid rows, processed count, and checkpoint row number.
- [ ] Keep in-file validation separate from database validation.
- [ ] Persist each chunk in a transaction and return row-level database errors.
- [ ] Aggregate cumulative counts and errors in the coordinator.
- [ ] Make chunk size configurable with a documented maximum.
- [ ] Promote the same chunk contract to a queue-backed job when synchronous request time becomes the limit.

## Case studies

- [[MOC/async-scale]] - Worker examples for bounded imports and chunk persistence.
- [[MOC/product-domain]] - Product-domain examples where operators import evaluation or review data.

## Related

- [[principles/bulk-import-via-command-queues]]
- [[principles/layered-io-boundaries-diplomat]]
- [[MOC/async-scale]]
- [[MOC/product-domain]]
