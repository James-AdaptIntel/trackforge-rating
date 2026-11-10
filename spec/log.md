# Hash-only rating log, format 1

The log is the public record that a rating statement was issued, replaced or withdrawn.
It holds hashes and dates only: no catalogue, client, letter or figure. Every change
appends a line; no line is ever edited or removed.

Schemas: [`log-entry.schema.json`](log-entry.schema.json),
[`log-head.schema.json`](log-head.schema.json).

## The file

`log/entries.jsonl`: one entry per line, each line the entry's canonical JSON (see
[statement.md](statement.md#canonical-form-and-hash)) followed by a newline.

| Field | Type | Meaning |
|---|---|---|
| `format` | `"trackforge-rating-log/1"` | this format |
| `seq` | integer | 1 for the first line, then +1 per line |
| `date` | `YYYY-MM-DD` (UTC) | the day the entry was appended; never earlier than the line before |
| `kind` | `issue`, `replace`, `withdraw` | what happened |
| `statement_sha256` | SHA-256 | the statement issued, the new statement that replaces another, or the statement withdrawn |
| `replaces_statement_sha256` | SHA-256 | `replace` only: the statement it replaces |
| `prev_entry_sha256` | SHA-256 or `null` | SHA-256 of the previous line's canonical bytes; `null` on line 1 |

No other field may appear.

## Rules

- `issue`: the statement has not been logged before.
- `replace`: the new statement has not been logged before, and the statement it replaces
  is current. The replaced statement's status becomes "replaced".
- `withdraw`: the statement is current. Its status becomes "withdrawn".
- A statement's status is **current** from its `issue` or `replace` entry until a later
  entry replaces or withdraws it. "Past review date" is read from the statement's own
  `review_date`, not from the log.
- Cross-check with the statement: a `replace` entry's `replaces_statement_sha256` equals
  the new statement's `previous_statement_sha256`. An `issue` entry for a statement whose
  `previous_statement_sha256` is not null is allowed only when that previous statement
  was withdrawn earlier.

The chain of `prev_entry_sha256` hashes means changing or removing any line breaks every
line after it.

## Timestamped heads

After each append, the head of the log is written to `log/heads/<seq, six digits>.json`:

```json
{"entry_sha256":"<SHA-256 of line seq>","format":"trackforge-rating-log-head/1","seq":3}
```

and timestamped with OpenTimestamps as a detached proof beside it
(`log/heads/000003.json.ots`), made for the SHA-256 of the head file's bytes. Because
each entry names the one before it, a confirmed timestamp on head *N* proves the whole
log up to line *N* existed by that Bitcoin block. A reader checks it with

```
ots verify log/heads/000003.json.ots
python checker/check_rating.py log log/entries.jsonl --head log/heads/000003.json
```

Heads are never edited either; a proof upgraded from pending to confirmed by
`ots upgrade` replaces only its `.ots` file.
