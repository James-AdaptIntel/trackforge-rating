# The rule book

`v2.8.json` is TrackForge's survey and rating rule book, version v2.8, published on
11 November 2026, byte for byte as it is used. It reads title for an owner outside PRS
from PRS's record of the work; no score, weight, factor or threshold changed. It carries every rule and every number
that moves a rating: component weights, the scale, defect classes and their factors,
floors and caps, coverage minimums, routes and their income split, source age limits.
The method statement ([`../METHOD.md`](../METHOD.md)) says the same thing in words.

## Checking it against the timestamped hash

The rule book's hash, the methodology hash every rating names, is the SHA-256 of the
file's canonical JSON: keys sorted, no spaces, ASCII. It is not the SHA-256 of the
file's bytes. To compute it:

```
python3 -c "import hashlib, json, sys; print(hashlib.sha256(json.dumps(json.load(open(sys.argv[1])), sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest())" v2.8.json
```

It prints
`59f99d999410e961cd69a00918a2541e8f57c027ba6238e0660bb42ed8f4bf39`, the hash named in
the method statement and timestamped on Bitcoin through OpenTimestamps, in block 975,482.

## Earlier versions

`v2.7.json` (published 11 November 2026) stays here in full, byte for byte; its hash is
`6df38bb202caf34463fbfd11ffe82156f8a55375ae1b78f3844b64a19c1420cf`, timestamped on Bitcoin in block 975,469. Check it the same way as above,
with `v2.7.json` in place of `v2.8.json`.

`v2.6.json` (published 6 November 2026) stays here in full, byte for byte; its hash is
`306515c149029dc3c762238519d8e288a42171021cd604bd38b994976547144f`, timestamped on Bitcoin in block 974,874. The first rating issued was reached
under it. Check it the same way as above, with `v2.6.json` in place of `v2.8.json`.

v2.4 (`7729c243…`) and v2.5 (`b4b34ddf…`) are published by hash only: their files carry
internal references, and no rating was issued under them. Their hashes and Bitcoin
blocks are in the method statement.

## What is not here

The rule book is public. The scoring code, the reference model and the readers that
obtain the evidence are not; a relying party can have a rating recomputed under a
separate agreement.
