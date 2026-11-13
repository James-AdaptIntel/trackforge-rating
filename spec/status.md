# Signed status answers, format 1

A rating can be replaced, withdrawn or left past its review date at any time. The live
check answers "is this rating still current?" in plain JSON. That answer proves nothing
afterwards. A counterparty who relied on it needs proof that TrackForge said "current"
at a given moment. A **status attestation** is that proof: a small signed answer, tied
to the caller's own nonce.

The signed answer is given by a status key published in
[`../status-keys/`](../status-keys/).

Schemas: [`status-attestation.schema.json`](status-attestation.schema.json),
[`status-key.schema.json`](status-key.schema.json),
[`status-key-retirement.schema.json`](status-key-retirement.schema.json).

## The status key

The rating key stays offline; it signs statements and nothing else. A separate **status
key** lives on the server and signs status attestations. The rating key vouches for it
in a published record, so a relying party trusts a status key only through a rating key
already published in [`keys/`](../keys/) (see [keys.md](keys.md)).

A status key can sign status attestations only. It is not a `trackforge-signing-key/1`
record, it is not in `keys/`, and no statement may name it as its signing key.

### Status key record

`status-keys/<fingerprint>.json`, canonical JSON:

| Field | Meaning |
|---|---|
| `format` | `"trackforge-status-key/1"` |
| `algorithm` | `"ed25519"` |
| `public_key` | the raw 32-byte public key, standard padded base64 |
| `fingerprint` | SHA-256 of those 32 raw bytes, lowercase hex (64 characters) |
| `holder` | who holds the key (printable ASCII) |
| `valid_from` | first day (UTC) the key may sign |
| `endorsed_by` | fingerprint of a rating signing key published in `keys/` |
| `endorsement` | base64 Ed25519 signature by that rating key over the canonical bytes of this record without `endorsement` |

The rating key must have been in service on `valid_from`. A record is never edited or
deleted once published.

### Retirement record

A status key leaves service by a record at `status-keys/retired/<fingerprint>.json`,
canonical JSON:

| Field | Meaning |
|---|---|
| `format` | `"trackforge-status-key-retirement/1"` |
| `fingerprint` | the status key leaving service |
| `date` | the day (UTC) the retirement takes effect |
| `reason` | `scheduled` or `compromise` |
| `endorsed_by` | fingerprint of a rating signing key published in `keys/` |
| `endorsement` | base64 Ed25519 signature by that rating key over the canonical bytes of this record without `endorsement` |

An attestation whose `checked_at` date is on or after `date` is refused.

## Status attestation

The envelope is

```json
{"attestation": {...}, "signature": "<base64 Ed25519 signature>"}
```

The signature is over the canonical JSON bytes of `attestation`, in the same canonical
form as statements (see [statement.md](statement.md)). The `attestation` holds exactly
these fields:

| Field | Meaning |
|---|---|
| `format` | `"trackforge-status-attestation/1"` |
| `statement_sha256` | hash of the rating statement the answer is about |
| `status` | `current`, `replaced`, `past_review_date` or `withdrawn` |
| `replaced_by` | `null`, or `{"issue_number", "issue_date"}` of the replacement |
| `checked_at` | server time in UTC, `YYYY-MM-DDTHH:MM:SSZ` |
| `nonce` | the caller's nonce, returned unchanged |
| `status_key` | fingerprint of the status key that signed |

### Asking for one

Add a `nonce` to the live check: `GET /api/v1/rating/check/<code>?nonce=<nonce>`. The
response is the usual answer with one extra member, `attestation`, holding the envelope.
Without a `nonce` the response is unchanged. A nonce is 16 to 128 characters from
`A-Z a-z 0-9 _ -`.

Choose a fresh random nonce for every check. An attestation proves the status at
`checked_at` only. A relying party should refuse an attestation that does not carry its
own nonce, or that is older than it is willing to accept.

## Checking one

Save the `attestation` member of the response and run

```
python checker/check_rating.py status attestation.json --keys keys --nonce <your nonce> \
    [--max-age SECONDS] [--statement rating-<id>.signed.json] [--status-keys status-keys]
```

The checker confirms that:

1. the status key is published in `status-keys/` and endorsed by a rating key published
   in `keys/` that was in service when the status key began;
2. the status key was in service and not retired at `checked_at`;
3. the signature verifies;
4. the nonce is the one you gave (with `--nonce`);
5. the answer is no older than `--max-age` seconds (with `--max-age`);
6. `statement_sha256` is the hash of the statement in your file (with `--statement`).

Exit status: 0 every check passed and the status is `current` or `past_review_date`; 1 a
check failed; 3 nothing failed but something could not be checked (no `--nonce` given);
4 genuine, but the status is `replaced` or `withdrawn`.
