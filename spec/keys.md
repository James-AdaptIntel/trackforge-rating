# Signing keys, format 1

Rating statements are signed by James, TrackForge's rating signatory, with a personal
Ed25519 key. This directory publishes the public half only. The private key never
enters this repository or any TrackForge server.

Schemas: [`key.schema.json`](key.schema.json),
[`key-rotation.schema.json`](key-rotation.schema.json).

## Key files

`keys/<fingerprint>.json`, canonical JSON:

| Field | Meaning |
|---|---|
| `format` | `"trackforge-signing-key/1"` |
| `algorithm` | `"ed25519"` |
| `public_key` | the raw 32-byte public key, standard padded base64 |
| `fingerprint` | SHA-256 of those 32 raw bytes, lowercase hex (64 characters) |
| `holder` | the signatory's name |
| `valid_from` | first day (UTC) the key may sign |

The **fingerprint** is the key's name everywhere: the file name, the statement's
`signing_key`, and the line printed on the Rating Report's summary page. On paper it may
be printed in groups of four (`3f2a 9c01 …`); the full 64 characters are always shown.

A key file is never edited or deleted once published.

## Rotation and revocation

A key leaves service only by a rotation record, `keys/rotations/<seq, six digits>.json`,
numbered from `000001.json` without gaps, canonical JSON:

| Field | Meaning |
|---|---|
| `format` | `"trackforge-key-rotation/1"` |
| `seq` | matches the file name |
| `date` | the day (UTC) the change takes effect |
| `old_key` | fingerprint of the key leaving service |
| `new_key` | fingerprint of its successor (already published in `keys/`), or `null` |
| `reason` | `scheduled` or `compromise` |
| `signatures` | `{fingerprint: base64 Ed25519 signature}` over the canonical bytes of the record without `signatures` |

Who signs:

- `scheduled`: both the old and the new key. The old key may sign statements dated
  before `date`; from `date` the new key signs.
- `compromise`: the new key (the old key's signature is optional, since it can no longer
  be trusted). A statement signed by the old key and dated on or after `date` is
  refused. One dated earlier is accepted with a warning: rely on it only if its
  OpenTimestamps proof confirms the signed statement existed before `date`.
- A rotation with `new_key: null` (revocation with no successor) is signed by the old key.

The first key is trusted because it is published here, on the check page and on every
Rating Report. Each later key is trusted through the rotation record signed by its
predecessor. Rotation records are timestamped with OpenTimestamps like the log heads
(`<file>.ots` beside each).

## Creating the key (step 4, James)

The key pair is created by James on his own machine. Only the public half and its
fingerprint come into `keys/`; the private key never enters this repository. The key
file is timestamped with OpenTimestamps before the first statement it signs.
