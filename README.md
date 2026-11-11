<p align="center">
  <a href="https://trackforge.studio"><img src="assets/trackforge-mark.svg" width="72" height="72" alt="TrackForge"></a>
</p>

<h1 align="center">TrackForge ratings: public record</h1>

<p align="center">
  <em>The registration-truth layer for music rights.</em><br>
  We find out what's actually registered, fix what's broken, and prove it's paying.
</p>

<p align="center">
  <a href="https://trackforge.studio">trackforge.studio</a> &middot;
  <a href="https://trackforge.studio/verify">Check a rating</a> &middot;
  <a href="https://trackforge.studio/docs/certification/rating">How a rating works</a> &middot;
  <a href="METHOD.md">Method statement</a>
</p>

<div align="center">
<table>
  <tr><th>Rule book in force</th><th>Signing key</th></tr>
  <tr><td><a href="rule-book/">v2.8</a></td><td><a href="keys/"><code>c38f1426…</code></a>, in service since 4 November 2026</td></tr>
</table>
</div>

This is the public record of catalogue ratings issued by TrackForge, Oxford, UK.
TrackForge rates the registration condition of music catalogues. Each issued rating
comes with a small **rating statement**, signed by TrackForge's rating signatory and
timestamped on Bitcoin with OpenTimestamps; its hash goes on a public, hash-only log.
This repository holds the rules a rating is reached under and what anyone needs to
check a rating document is genuine, unaltered and still current.

## What is here

| Path | What |
|---|---|
| [`METHOD.md`](METHOD.md) | the method statement in prose |
| [`rule-book/`](rule-book/) | the rule book in force (v2.8), byte for byte, with v2.7 and v2.6 beside it |
| [`keys/`](keys/) | TrackForge's Ed25519 public signing key(s) and any rotation records |
| [`log/`](log/) | the hash-only log of issues, replacements and withdrawals, and its timestamped heads |
| [`spec/`](spec/) | the formats: [statement](spec/statement.md), [log](spec/log.md), [keys](spec/keys.md), with JSON Schemas |
| [`checker/`](checker/) | a small checker for signature, log and timestamp lookups |

## Method statement

[`METHOD.md`](METHOD.md) is the method in words: the levels, what is surveyed, the five
components, how works are weighted, how the letter is read and capped, estimated
inputs, money, sources, what is not checked, and what each letter means. It names the
rule book by version and SHA-256 hash, with the Bitcoin block that timestamps the hash.
The same text is published at
<https://trackforge.studio/docs/certification/rating/method-statement>.

## What is public and what is not

Public: the method statement, the rule book, the public keys, the log and the checker.
From v2.6 the rule book is published in full, byte for byte as it is used, in
[`rule-book/`](rule-book/), v2.8 in force and v2.7 and v2.6 beside it; a version's hash is
timestamped on Bitcoin before the first rating under it (the timestamps of v2.7 and v2.8 are pending),
and the rule book's README says how to check the file against that hash. The earlier
versions, v2.4 and v2.5, are published by hash only.

Not public: the scoring code, the reference model and the readers that obtain the
evidence. A relying party can have a rating recomputed under a separate agreement. A
rating is private by default: the log holds hashes only, and the check page answers only
to a document's own code.

## Checking a rating

You need the signed statement (`rating-<id>.signed.json`) and its timestamp proof
(`rating-<id>.signed.json.ots`), both in the proof pack the catalogue owner shares.

```
pip install -r checker/requirements.txt
python checker/check_rating.py statement rating-<id>.signed.json --keys keys --log log/entries.jsonl
```

The checker confirms, and does nothing else:

1. the signature is by a published TrackForge key that was in service on the issue date;
2. the statement's hash is in the log, the log's chain is intact, and whether the
   statement is current, replaced or withdrawn;
3. the timestamp proof is for this exact file and, with the OpenTimestamps client
   installed (`pip install opentimestamps-client`), that Bitcoin confirms it.

Exit status: 0 genuine, current and fully checked; 1 a check failed; 3 nothing failed
but something could not be checked; 4 genuine but replaced or withdrawn.

The checker tells you a document is TrackForge's, unaltered, and when it existed. It
cannot tell you the society records it describes are right; the Rating Report lists the
largest works and where to look each one up.

To check the log on its own:

```
python checker/check_rating.py log log/entries.jsonl --head log/heads/000001.json
```
