# Rating statement, format 1

The rating statement is the small document that TrackForge signs, timestamps and logs
for each issued rating. The Rating Report, the condition schedule and the proof pack all
hang from it. A document cannot carry the Bitcoin proof of itself, so this statement is
the proved object, and the report quotes it.

Schemas: [`statement.schema.json`](statement.schema.json),
[`signed-statement.schema.json`](signed-statement.schema.json).

## Fields

| Field | Type | Meaning |
|---|---|---|
| `format` | `"trackforge-rating-statement/1"` | this format |
| `rating_id` | lowercase UUID | TrackForge's id for this issued rating (one per issue) |
| `catalogue_ref` | opaque lowercase id, ≤ 64 chars | TrackForge's identifier for the rated catalogue; never a name |
| `issue_number` | integer ≥ 1 | 1 for the catalogue's first rating, then 2, 3, … |
| `issue_date` | `YYYY-MM-DD` (UTC) | the day the rating was issued |
| `review_date` | `YYYY-MM-DD` (UTC) | after this day the rating is "past review date"; normally six months after issue |
| `letter` | `AAA` `AA` `A` `BBB` `BB` `B` `CCC` `CC` `C` `D` | the rating |
| `tuple_hash` | SHA-256, lowercase hex | hash of the full rating tuple (the letter with everything that decides it) |
| `rule_book.version` | e.g. `v2.4` | the rule book the rating was made under |
| `rule_book.sha256` | SHA-256, lowercase hex | that rule book's hash; the rule book is published by hash only and timestamped before its first rating |
| `proof_pack_sha256` | SHA-256, lowercase hex | hash of the frozen proof pack (the ZIP the owner receives), frozen before the statement is built; see the hashing boundary below |
| `previous_statement_sha256` | SHA-256 or `null` | the catalogue's previous statement; `null` exactly when `issue_number` is 1 |
| `signing_key` | key fingerprint | the published key that signs this statement (see [keys.md](keys.md)) |

All strings are printable ASCII, all numbers are integers, and no other field may
appear. `review_date` must fall after `issue_date`. The statement carries no client
name, work list, share or money figure.

## Canonical form and hash

Every document in these formats is stored, hashed and signed as **canonical JSON**:
object keys sorted, no whitespace, UTF-8, non-ASCII escaped. In Python that is

```python
json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
```

which is byte for byte the function TrackForge's rating engine uses for its own hashes.
Because these documents hold only printable-ASCII strings, integers and null, the
bytes also match RFC 8785 (JSON Canonicalization Scheme), so other languages can
reproduce them.

The **statement hash** is the SHA-256 of the statement's canonical bytes, in lowercase
hex. It is the statement's identity: the log records it, the next statement names it in
`previous_statement_sha256`, and the check page looks it up.

Example (620 bytes; the hashes here are placeholders):

```json
{"catalogue_ref":"0f3c2a9e-7b1d-4c55-9a10-3e2f6d8b4c21","format":"trackforge-rating-statement/1","issue_date":"2026-11-10","issue_number":1,"letter":"BB","previous_statement_sha256":null,"proof_pack_sha256":"2222222222222222222222222222222222222222222222222222222222222222","rating_id":"add8e50a-0000-4000-8000-000000000001","review_date":"2027-05-10","rule_book":{"sha256":"7777777777777777777777777777777777777777777777777777777777777777","version":"v2.4"},"signing_key":"3333333333333333333333333333333333333333333333333333333333333333","tuple_hash":"1111111111111111111111111111111111111111111111111111111111111111"}
```

## Hashing boundary: what is signed, and what hangs from it

The statement is the only signed object. Everything else is bound to it by a hash it
carries or a hash that names it, in this order:

1. **The rating record** (the tuple: the letter with everything that decides it) is
   hashed first; the statement carries that hash as `tuple_hash`. The record itself is
   not in the statement and not published by this page; the Rating Report prints the
   hash, and the check page shows, beside the letter, the record's scope (tier, works
   rated, rights positions, routes in scope, income route coverage, whether collection
   was assessed, works set aside, caps applied), read from the record the hash names.
2. **The proof pack** (the ZIP the owner receives: the record, the rows it was computed
   from, the rule book pinned by hash, the checks run on it, the analyst's note) is
   built and hashed *before* the statement exists; the statement carries that hash as
   `proof_pack_sha256`. So the pack does not contain the statement, the signature or
   the timestamp, and cannot: the statement's timestamp covers the pack's hash. A pack
   that held its own statement would be circular.
3. **The statement** is hashed (the statement hash, above) and signed. The statement
   hash is the identity the log, the check page and the next issue's
   `previous_statement_sha256` use.
4. **The signed statement file** is timestamped: the OpenTimestamps proof is of the
   file's bytes, so it proves when the signature existed.
5. **The Rating Report (PDF) and the condition schedule** are produced *after* the
   statement is signed, from the stored record, and so cannot be fields of it. The PDF
   quotes the statement hash, the rating record hash and the check code. Its SHA-256,
   and the schedule's, are recorded against the rating in a **release** record
   (`subject_sha256` is the PDF's SHA-256; the detail carries the schedule's and the
   statement hash the report is of), and the check page's "Check a file you hold"
   compares a file's fingerprint with the released PDF's, the pack's and the signed
   statement's. A PDF with a different fingerprint is not the released report.

The format therefore does **not** carry the PDF's or the schedule's hash, and the
pack's hash is of the pack as frozen at issue, not of a wrapper around the statement.
Changing either would change what the check page promises, and would be a new format.

## Signed statement

The signed statement is a second canonical-JSON document:

```json
{"format":"trackforge-signed-rating-statement/1","signature":"<base64>","statement":{...}}
```

- `signature` is the Ed25519 signature (RFC 8032, pure Ed25519) by the key named in
  `statement.signing_key`, over the statement's canonical bytes exactly (no prefix, no
  trailing newline), written in standard padded base64.
- The file holds the canonical bytes, optionally followed by one newline.
- Suggested file name: `rating-<rating_id>.signed.json`.

## Timestamp

The signed statement file is timestamped with OpenTimestamps as a standard detached
proof beside it, `rating-<rating_id>.signed.json.ots`, made for the SHA-256 of the
file's bytes, so that

```
ots verify rating-<rating_id>.signed.json.ots
```

checks it. Stamping the signed file rather than the bare statement also proves when the
signature existed, which keeps signatures made before a key compromise usable
(see [keys.md](keys.md)).

## Successive issues

A later rating of the same catalogue is a new statement with the next `issue_number`
and the previous statement's hash in `previous_statement_sha256`. Its log entry is a
`replace` of that previous statement (see [log.md](log.md)), unless the previous one was
withdrawn first, in which case it is a fresh `issue`.
