# The rule book

`v2.6.json` is TrackForge's survey and rating rule book, version v2.6, published on
6 November 2026, byte for byte as it is used. It carries every rule and every number
that moves a rating: component weights, the scale, defect classes and their factors,
floors and caps, coverage minimums, routes and their income split, source age limits.
The method statement ([`../METHOD.md`](../METHOD.md)) says the same thing in words.

## Checking it against the timestamped hash

The rule book's hash, the methodology hash every rating names, is the SHA-256 of the
file's canonical JSON: keys sorted, no spaces, ASCII. It is not the SHA-256 of the
file's bytes. To compute it:

```
python3 -c "import hashlib, json, sys; print(hashlib.sha256(json.dumps(json.load(open(sys.argv[1])), sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest())" v2.6.json
```

It prints
`306515c149029dc3c762238519d8e288a42171021cd604bd38b994976547144f`, the hash named in
the method statement and timestamped on Bitcoin through OpenTimestamps.

## Earlier versions

v2.4 (`7729c243…`) and v2.5 (`b4b34ddf…`) are published by hash only: their files carry
internal references, and no rating was issued under them. Their hashes and Bitcoin
blocks are in the method statement.

## What is not here

The rule book is public. The scoring code, the reference model and the readers that
obtain the evidence are not; a relying party can have a rating recomputed under a
separate agreement.
