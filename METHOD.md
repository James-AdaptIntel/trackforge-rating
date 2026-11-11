# Method statement: how a catalogue rating is reached

*TrackForge's published method statement. The same text is at <https://trackforge.studio/docs/certification/rating/method-statement>.*

> **Scope.** A TrackForge rating grades registration at the UK and US statutory collection routes: PRS for Music, MCPS, ICE, The MLC, PPL and SoundExchange, and, for a direct ASCAP or BMI member that supplies its own export of its account, that society as its US performing route (available on owner export; not yet exercised on an issued rating). It does not grade direct memberships of other societies (GEMA, SACEM, SOCAN, APRA and the rest), income collected abroad by a sub-publisher, or mechanicals outside The MLC. Income that reaches a PRS or PPL member through those societies' reciprocal agreements is in scope through PRS or PPL: the rating grades the home registration that the foreign society matches against, and does not read whether the foreign society has matched it. A direct ASCAP or BMI member that supplies no export is not graded on its US performing income, and the rating says so.

> **Rule book v2.8: published and frozen.** This statement describes rule book **v2.8**, which is published in full and frozen (see [the rule book](#the-rule-book)). Its SHA-256 hash is named under [the rule book](#the-rule-book) and timestamped on Bitcoin. A published version never changes. Its numbers are starting values: calibration on real catalogues changes them only by a new version of the rule book, with a new number and a new hash.

This is the method a TrackForge catalogue rating follows, in words. The rule book is the same method written as rules and numbers; this page and the rule book say the same thing, and where a term below has a plain name in the rule book, this page uses it. Terms in **bold** are defined in the [glossary](https://trackforge.studio/docs/certification/rating/glossary).

## What a rating says

A rating describes the **registration condition** of a music catalogue on a stated date: for each work the owner says is theirs, whether the registrations that make money flow are in place at each society that collects for it, from the evidence TrackForge read.

Every letter carries one fixed line:

> A letter describes the registration condition of the catalogue on its date. It is not a valuation, a credit rating or a legal opinion on title.

A rating proves what the evidence showed under these rules on that date. It does not prove the evidence is true; a reader checks that by looking the largest works up at the societies, and the Rating Report lists where.

## Levels

| Level | Name | Letter | What goes in |
|---|---|---|---|
| Tier 0 | Catalogue check | **No letter** | Public registries and identity data only |
| Tier 1 | Catalogue rating | Letter | Tier 0, plus the owner's attestation, the owner's exports from the societies it collects through, and statements, agreements and registration history where supplied |
| Tier 2 | Asset integrity assessment | Letter | Tier 1, plus a cash bridge from statements to bank, reconciliation of the population, exceptions and independence disclosures. Defined, not yet offered |

A tier 0 check is a check: it reports what public sources show and what they could not show, and never carries a letter. Coverage minimums apply only at tiers 1 and 2.

## What is surveyed

**The population.** The owner's attestation lists the works the rating covers before any lookup runs. The attestation fixes the population; it decides no state. A work recorded under the owner whose income belongs to someone else under an agreement (for example a work sold on with the owner left on the chain) can be removed by a **grading scope**, with a reason, the name of the person attesting, a date and an evidence reference. Removed works are never scored, and the rating discloses each one and the weight it would have carried.

**Rights positions.** Compositions (performing, digital and physical mechanical, sync) and sound recordings (neighbouring rights, master distribution) are surveyed separately, never in one denominator. A position the owner does not hold is not a defect: the work has no survey for it.

**Routes.** Scope is set by collecting **route**, not by where a work is used:

| Route | Collects |
|---|---|
| PRS for Music | Performing, including overseas performance income reaching a member through reciprocal agreements |
| MCPS | Digital and physical mechanicals |
| ICE | The registration hub for PRS and MCPS; takes no income of its own |
| The MLC | US digital mechanicals |
| PPL | Neighbouring rights, including PPL's reciprocals |
| SoundExchange | US neighbouring rights |
| ASCAP | US performing, for a direct member, on the owner's own export of its account (available on owner export; not yet exercised on an issued rating) |
| BMI | As ASCAP; a survey carries one of the two, the owner's own affiliate |

Out of scope, for example: direct memberships of societies other than ASCAP and BMI, income collected abroad by a sub-publisher, and mechanicals outside The MLC. CIS-Net, the ASCAP bulk data and the US Copyright Office show that a work exists and who is attached to it; they never decide a route's registration. From v2.7 CIS-Net is also read for identity: a work is placed on the societies' records that carry one of the owner's parties, and that placing counts as the identity reading for a work no higher-ranked reading has read, which is how the work of an owner outside PRS is read. An owner-export route is in scope only when the owner supplies its export; without it a declared direct member's US performing income is not graded, and the rating says so. With it in scope beside PRS, performance income divides by territory as digital mechanical income does between The MLC and MCPS: the US route takes the declared US performing share (or the rule book's default, disclosed with its source) and PRS the remainder.

## The four states

Each work is judged on each component, and on registration at each route, as one of four states:

| State | Means |
|---|---|
| **Sound** | The evidence read shows it in order |
| **Defective** | The evidence read shows a named defect |
| **Not checked** | No evidence could answer, for a recorded reason |
| **Not relevant** | The question does not arise, for example a right the owner does not hold |

A work's overall condition is defective if any component is defective, otherwise not checked if any is not checked, otherwise sound.

## Why a work is not checked

Not checked is never a choice. It is always the outcome of a recorded limit, and it always carries one of seven reasons. Each reason sits with one party:

| Reason | Who | What it means |
|---|---|---|
| Not supplied | The client | The client has not supplied the evidence that would answer: the society export, statement or agreement this check reads. For risk, no reading of the work at PRS, MCPS or The MLC |
| Too recent to appear | The society | The work or release is newer than the society's record has caught up with. Nobody has failed; a later run reads it |
| Waiting for the society to publish it | The society | The registration is in the society's queue and not yet published |
| Not reached in this run | TrackForge | TrackForge's run did not read the work at this source: it stopped short, or never read this code there |
| Source could not be read | TrackForge | TrackForge could not read the source, or the source did not say whose the work is |
| Reading past its age limit | TrackForge | TrackForge's only readings are older than the source's age limit, so none may decide |
| TrackForge's copy predates the release | TrackForge | The release is newer than TrackForge's dated copy of the catalogue it is read from, so the copy cannot have it. The limit is TrackForge's, not the society's; a live reading removes it. A rating is not issued while a material work (at or above the single-work share of weight, or among the heaviest twenty) is in this state; below that it is ordinary coverage shortfall |

Where a work's registration is not checked at more than one route for different reasons, its registration state carries the reason that comes first in this table.

A not-checked work is left out of the component's score and counted as a shortfall in **coverage** instead, so it neither flatters nor harms the score.

## The five components

| Component | Asks |
|---|---|
| Identity | Can each work and recording be told apart and matched: ISRC, ISWC, writer IPIs, one registration per work; for a sound recording, that its ISRC names one recording in the streaming services' catalogues |
| Title | Is the owner's claim to each work backed by an agreement at its society that binds the work, and does the society hold the share that agreement documents; for a sound recording, does the ℗ credit on the release name the owner |
| Registration | Is each work registered, under the owner, at every society where it earns |
| Collection | Is the money the registrations should bring in actually arriving |
| Risk | Disputes, competing claims, duplicate shells and sources that disagree |

**How a component is scored.** Each defect has a class, and each class a factor: a full deduction, a partial one or a minor one, or, for a share registered below what is owned, the size of the gap. A work's deduction on a component is the largest factor among its defects there. The component's score is, over the works assessed (sound or defective), the weight kept after deductions as a share of the weight assessed, out of 100.

**Registration is scored route by route.** A registration defect costs a work only that route's share of its income, not the whole work. A route that was not read for a work is left out of that work's sums: neither credited nor charged.

**Title compares shares.** For a work bound to one of the owner's agreements, the share the society holds for the owner of each right the agreement covers is compared with the share the agreement documents, scaled by the owner's declared attributable share of the work. A share lower by more than the rule book's tolerance is a leak with the gap as its factor; a higher one is a risk. A bound work whose society record is past its age limit is not checked for title, reason reading past its age limit, because a sound title says the shares agree.

**Title for an owner outside PRS.** A PRS member's title is read from its own PRS works list and its PRS agreement lists. An owner whose society is not PRS has neither. For such an owner TrackForge reads PRS's own record of the work: PRS's works database also carries works of other societies' members, with each party's society, chain and shares. A work is read on a record that carries one of the owner's parties by IPI name number and either a society work number its CIS-Net placing names or the work's ISWC, never by title alone. Where the owner's party holds a positive share on the record, the work is held there in the owner's name. No agreement list of the owner's society is read, so the binding to an agreement is inferred from the record and every title read this way carries the finding 'Agreement binding inferred or assumed'. No share is compared. A work with no such record is not checked for title; absence is never concluded from these records. The MLC's record and CIS-Net are not title readings: The MLC's record is the registration reading for that route, and CIS-Net shows identity and presence only.

**Collection needs statements.** Without them it reads "collection not assessed", and the composite is taken over the other four. A rating with collection not assessed carries no collection defects, so the letter says nothing about whether the money is arriving, and it is treated as a registration rating: the letter is capped at A, the cap is listed with the floors as `collection_not_assessed`, the record carries `collection_assessed`, and page 1 of the Rating Report and the check page label the letter a **registration rating (collection not assessed)**. It is a limit of scope, not a defect: no number changes, only the letter a narrow scope may reach.

**Risk counts as sound only where a risk check was read.** PRS, MCPS and The MLC can show a dispute or competing claim; PPL and SoundExchange cannot. A work is sound for risk when at least one of PRS, MCPS or The MLC read it and raised no risk. A work none of them read is not checked, reason not supplied, whatever other routes read it. So sound on risk means no known conflict was found in what was read, not that no risk exists.

## How works are weighted

A hit should count for more than a demo nobody plays, and a small stake for less than a whole one. Each work's weight is:

- **Demand, the larger part.** Within each income channel, the work's share of the catalogue's demand there, weighted by the catalogue's channel mix.
- **An equal part.** An equal share for every work, so works with no measured demand still count.
- **Scaled by the attributable share.** The blend is multiplied by the owner's share of the work and the weights rescaled to sum to one. A 1% stake carries 1% of the weight the work would carry at 100%.

**The demand measure.** For each channel the measure is statement lines where they are supplied. Otherwise Spotify lifetime plays come first: for each work, the plays per recording from a dated snapshot, where Spotify shows a count on any of the work's recordings. YouTube views per recording are used only where Spotify shows none. The snapshot records how each recording was matched to Spotify (by ISRC, or by title and artist where the ISRC found nothing) and a work sums its recordings. A refresh is a new dated snapshot, never a rewrite, and a snapshot that cannot be read stops the run rather than falling back to YouTube.

**Mixing plays and views.** Where a channel has Spotify plays for some works and only YouTube views for others, the views are converted into Spotify-equivalent plays at one ratio measured on the catalogue's own works that carry both counts, so the channel adds like with like. Below the minimum number of such works the views stand aside where plays are used, and those works get the equal share only. The ratio, the number of works it was measured on and both snapshot dates are disclosed in the rating.

Physical mechanicals use distributor sales, MCPS statement lines, then the release footprint; sync uses statement lines only. Income never sets a weight on its own: demand is the floor and income can only raise it. A work with no demand in any channel carries only its equal share and is reported in the unweighted tail. The measure and its date are frozen into the rating.

**Where the attributable share comes from.** In order: declared by the owner; from the owner's Workspace draft; from the society's chain; otherwise assumed whole. Every work states its source and the rating counts works by source, so a reader can see how many shares were assumed.

### Largest works

The largest works are the works with the highest weight under the rule above: demand first by statements, then Spotify lifetime plays, then YouTube views converted into Spotify-equivalent plays; mostly demand, with an equal part for every work; scaled by the owner's share. The Rating Report shows the condition of the top 20 and lists where a reader can look each one up.

## Routes and income

The channel mix says how much of the catalogue's income each channel carries; it is the owner's declaration, or statements where supplied. With no declared mix, a recording catalogue is taken as all neighbouring rights and any other as all digital mechanical.

A route's **expected-income share** is the sum of the mix over its channels. Two channels divide between routes:

- **Digital mechanicals**: The MLC takes the catalogue's US share and MCPS the rest. Undeclared, the US share is set deliberately above the US alone, so that leaving it undeclared never shrinks The MLC.
- **Neighbouring rights**: SoundExchange takes the catalogue's SoundExchange share and PPL the rest. Undeclared, it takes the same starting value.
- **Performance**: where a direct US performing route is in scope on the owner's export beside PRS for Music, that route takes the catalogue's US performing share and PRS the rest. Undeclared, it takes the same starting value.

If only one of the pair is in scope it takes the whole channel. A route below the materiality threshold of expected income is **immaterial**: its defects are found, listed and cost their share in the registration score, but it never caps the letter. With few lifetime streams across the catalogue and no US statements, The MLC is immaterial by default. The rating discloses each route's share and whether it is material.

A route that carries a rights type's main income must be in scope whenever the catalogue shows use in its channels: The MLC for compositions with digital releases, PPL and SoundExchange for recordings.

## From scores to a letter

**Composite.** The weighted mean of the component scores, over the components assessed.

**Letter before caps.** The composite read against the scale: each letter starts at a set composite, AAA highest and D lowest. The Rating Report shows where the catalogue's composite fell.

The letter issued is the letter before caps, lowered by any cap that applies. The lowest cap wins, and every cap is disclosed.

**Coverage minimums.** At tiers 1 and 2, coverage below the minimum withholds the letter, with the shortfall named. There is a minimum for:

- Identity: by count of clusters, with an alternative test by weight. A cluster is a work with its versions and stems, counted once.
- Title: by weight.
- Registration: by weight at each main route.

**Coverage cap (ladder).** Above the minimum, title coverage by weight, and registration coverage by weight at each route, cap the letter in steps: the less of the catalogue that could be checked, the lower the highest letter it can carry. The worst step met applies, and the Rating Report names it.

**Floors.** Some defects are too serious for an average. Each floor caps the letter at a set level when a set share of the catalogue carries the defect, whatever the composite says. There are floors for:

- works lacking an ISRC on an exploited recording (by count);
- a route's income unregistered, at two levels, the larger share capping lower;
- works without a PRS agreement binding them (by weight, where PRS is in scope);
- a route's income going to the wrong party: the floor reads two classes, income to the wrong payee (defined, not yet read) and registered under another party only (read), so today it fires on the second;
- a termination notice or dispute among the works carrying the most weight.

The Rating Report names every floor that capped the letter.

"Unregistered" means not registered where exploited, registered under another party only, or a recording absent from PPL or SoundExchange. Floors on a route's income use each work's **income weight** there, the demand part of its weight alone, so unplayed works cannot trip a floor; they are applied per route, scaled by the route's share of income, and never at an immaterial route.

**When no letter is issued.** No letter is issued when a coverage minimum is not met, or when any single work carrying a material share of the weight is not checked because evidence was not supplied, the work was not reached in this run, or a source could not be read.

**When a rating cannot be issued.** A run can reach a letter and still not be issued. An issued rating has no lookup limit: issue is refused while any work at all, whatever its weight, is not checked anywhere because it was not reached in this run. That limit is TrackForge's own cap on lookups, a gap of TrackForge's making, so it is never a reason on an issued rating. The same reason covers a code TrackForge never read at the PRS works database, PPL or SoundExchange, so those gaps refuse issue too. A draft or rehearsal run may still stop short and keeps its letter; TrackForge finishes the reading before issuing. Issue is also refused while a material work (one at or above the single-work share of weight, or among the heaviest twenty) is unchecked because TrackForge's copy predates its release; the top-up lane, below, reads such works first.

## Estimated inputs

Some inputs are declared rather than measured: the US share, the SoundExchange share, the US performing share and the channel mix. Each states its value, its basis and a plausible range. The catalogue is re-rated at every combination of the ends of the ranges, and the letter issued is the **lowest** of those and the letter at the declared values. The composite and components shown are those at the declared values; the Rating Report lists the letter at each end. An input measured from settled statements says so, with a range of one value. A rating cannot be issued on a declared input with no range.

## Money

A rating shows only **measured amounts**: a figure a society shows for the work, or a statement line, each with its source, in whole pence shown as pounds. Amounts attach to the registration leaks, usage unmatched at The MLC and unclaimed shares. Where there is no such figure the rating says **no amounts**, never £0. Amounts are disclosure: they never change a score or a letter. Estimates of what works are worth belong in the separate Fix plan, as labelled ranges, outside the rating.

## Sources and dates

Every source is named with the date its reading was true. Where two sources of one kind answer, the newer wins. Where sources of different kinds disagree within their age limits, the higher-ranked source decides and the disagreement is recorded as a risk, so a manufactured disagreement cannot hide a defect. Each kind of source has an age limit, and a reading older than its limit never decides. Identity readings do not age. An acknowledgement proves only that a file entered a society's queue, never that it was registered.

A table TrackForge reads live is a dated read, pinned by a hash of the rows read, which travel with the rating. The MLC's bulk data is pinned by the hash of its manifest. MusicBrainz takes its date from its version. Spotify plays and YouTube views each take the date of their snapshot, and the plays-per-view ratio is fixed with the number of works it was measured on.

**The streaming services' catalogues.** TrackForge also reads its own copies of the public catalogue data of three streaming services: Deezer and Tidal, in the MusicMoveArr editions of February 2026, and Beatport, to September 2023. Each is a dated public source whose date is its edition's, and they are read for identity and, for sound recordings, title; nothing else. Spotify's catalogue is not read for every work: it is read live, by ISRC, for the top-up set only, the material works whose release is newer than the dated copies, and each such read is a dated source on the rating, disclosed as a live read. Where the copies put one ISRC on two recordings that differ in artist, or in length by more than three seconds, the work carries an **ISRC collision** on identity, the full deduction; where they show one recording under two titles, or under a title that disagrees with the owner's, it carries a **cross-source inconsistency**, a minor one. A sound-recording survey takes its identity reading from the copies: held under one recording is sound, a disagreement is defective, held by no copy is not checked.

**The ℗ credit on the release.** A sound-recording survey takes its title reading from the ℗ credit on the release, as the Tidal copy holds it: the credit the releasing party delivered through its distributor, independent of PPL, SoundExchange and the owner's attestation. It has three outcomes. A credit that names the owner is sound. A credit that names another party and not the owner is a question, not a finding; it becomes a defect, the risk class **the release's ℗ credit names another party**, only when a registry names the same party. The recording is then not checked (not supplied: an agreement or licence is needed, and the Rating Report lists each such recording so the owner can supply it) unless PPL or SoundExchange hold the recording under the same party the credit names, in which case the release and the registry agree the master sits with someone other than the declared owner and the class applies. A distributor's default credit (DistroKid's numbered label, or the bare TuneCore, CD Baby, AWAL, Ditto, Amuse and Believe lines) names nobody, so it is a question too, never a defect. A credit that names only the artist corroborates nothing, so the recording is not checked, unless the owner is the artist. The credit ranks last among title sources and does not age. Label is not publisher: a composition survey never reads the credit.

## What is not checked

Eleven of the rule book's 38 defect classes are defined but nothing reads them yet; seven of the eleven would move the grade. A sound result says nothing about them, and the page [what is read](https://trackforge.studio/docs/certification/rating/what-is-read) lists every class with its reading status:

- Identity: no ISWC where the route allocates one.
- Title: a reversion or term expiry coming soon.
- Collection: no income despite usage; income to the wrong payee; an account on hold.
- Risk: a claim window closing; an administration or sub-publishing agreement ending.
- Opportunities: registered but not yet exploited; registered at a society outside the routes; sync not represented; physical exploitation not registered or claimed.

Collection is assessed only when statements are supplied.

The streaming services' catalogues are editions, not live reads. A recording released after the newest copy's edition (22 February 2026 for Deezer and Tidal; September 2023 for Beatport) is not checked by them, with the reason TrackForge's copy predates the release: that limit is TrackForge's copy, not any society's record, and a rating is not issued while a material work carries it. The top-up lane reads those material works in weight order until none remains: first live, from a public streaming catalogue read on the day, then, where the live read finds nothing, by a manual reading, a named person reading a named page or document on a named date. Each reading is a dated source pinned by the hash of what was read and carried in the proof pack; it sets identity and title only and decides no route's registration state; the rating discloses the count of works read by each top-up source, and the report names each manual reading with who read it and when. A recording held by no copy is not checked, with the reason source could not be read. They are never read for a composition's title, and a sound recording's ℗ credit is never read for a composition.

## Leaks, risks and opportunities

A **leak** loses money now; a **risk** could lose money later; an **opportunity** is income not yet earned. Leaks and risks move the grade. Opportunities are listed, never scored.

## In flight, the projected letter and the outlook

Work sent to a society and acknowledged but not yet published never changes the letter. The Rating Report shows it beside the letter, not in it: a **projected letter** with acknowledged, uncontested items treated as landed, and an **outlook**. Rule book v2.6 keeps their rules unchanged from v2.4; see [in flight](https://trackforge.studio/docs/certification/rating/in-flight).

## The scale

A letter describes the registration condition of the catalogue on its date. It is not a valuation, a credit rating or a legal opinion on title.

| Letter | Means |
|---|---|
| AAA | Registration is in order; only isolated minor items remain. |
| AA | Very few defects, none on the main earners. |
| A | Sound overall; defects are minor and not concentrated. |
| BBB | Adequate: most income is sound, with some material defects to fix. |
| BB | Noticeable income is exposed; expect a remediation plan before relying on it. |
| B | Substantial defects across the catalogue. |
| CCC | Widespread defects; much of the income is at risk now. |
| CC | Most of the catalogue is defective. |
| C | Nearly all of the catalogue is defective. |
| D | The registration position cannot be relied on. |

The composite at which each letter starts is a starting value of rule book v2.8, unchanged from v2.4. Calibration changes it only by a new version of the rule book.

## The rule book

The rule book is versioned. Each change takes a new version; a published version never changes. Its hash is timestamped on Bitcoin before the first rating under it, and every rating names the version and hash it was reached under. From v2.6 the rule book's full text is published, byte for byte as it is used: [v2.8.json](rule-book/v2.8.json) is the version in force, and [v2.7.json](rule-book/v2.7.json) and [v2.6.json](rule-book/v2.6.json) remain. Every number in it that moves a rating is set out on [the rule book: every number](https://trackforge.studio/docs/certification/rating/rule-book). The rule book is public. The scoring code, the reference model and the readers that obtain the evidence are not; a relying party can have a rating recomputed under a separate agreement.

The current version:

- **Version:** v2.8, published and frozen on 11 November 2026. It reads title for an owner outside PRS from PRS's record of the work. No score, weight, factor or threshold changed.
- **SHA-256:** `59f99d999410e961cd69a00918a2541e8f57c027ba6238e0660bb42ed8f4bf39`. It is the SHA-256 of the file's canonical JSON (keys sorted, no spaces, ASCII), not of the file's bytes: `python3 -c "import hashlib, json, sys; print(hashlib.sha256(json.dumps(json.load(open(sys.argv[1])), sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest())" v2.8.json` prints it.
- **Bitcoin timestamp:** Bitcoin block 975,482 (mined 22:16 GMT, 11 November 2026), submitted to OpenTimestamps at 22:04 GMT on 11 November 2026. The proof is [rule-book-v2.8.ots](https://trackforge.studio/docs/proofs/rule-book-v2.8.ots). It commits to the SHA-256 of the hash's 32 bytes, so to check it, write those bytes to a file and verify against it: `printf 59f99d999410e961cd69a00918a2541e8f57c027ba6238e0660bb42ed8f4bf39 | xxd -r -p > rule-book-v2.8` then `ots verify -f rule-book-v2.8 rule-book-v2.8.ots`.

Earlier versions stay named, and a rating names the version it was reached under and checks against that version's hash.

- **v2.7**, published 11 November 2026 and still published in full: [v2.7.json](rule-book/v2.7.json). SHA-256 `6df38bb202caf34463fbfd11ffe82156f8a55375ae1b78f3844b64a19c1420cf`. It reads CIS-Net for identity. A work is placed on the societies' records that carry one of the owner's parties, by IPI name number, by the work's ISWC and otherwise by its title; a fresh placing is a registry record of the work, so a work no higher-ranked reading has read is sound on it, which is how the work of an owner outside PRS is read. Conflicting ISWCs, duplicate work registrations and a writer without an IPI can be read from it. A CIS-Net reading keeps its age limit of 90 days; past that limit it decides nothing and changes no state. CIS-Net still never decides a route's registration state. No score, weight, factor or threshold changed from v2.6. Bitcoin block 975,469 (mined 19:56 GMT, 11 November 2026), submitted to OpenTimestamps at 17:42 GMT on 11 November 2026, proof [rule-book-v2.7.ots](https://trackforge.studio/docs/proofs/rule-book-v2.7.ots).
- **v2.6**, published 6 November 2026 and still published in full: [v2.6.json](rule-book/v2.6.json). SHA-256 `306515c149029dc3c762238519d8e288a42171021cd604bd38b994976547144f`, Bitcoin block 974,874 (mined 01:30 GMT, 7 November 2026), submitted to OpenTimestamps at 23:03 GMT on 6 November 2026, proof [rule-book-v2.6.ots](https://trackforge.studio/docs/proofs/rule-book-v2.6.ots). The first rating issued, on 9 November 2026, was reached under it.

The two before it are published by hash only: their files carry internal references, and no rating was issued under them.

- **v2.5**, published 5 November 2026: SHA-256 `b4b34ddf5aa3c18087e8e0cb12ad4061adc3ec6fbbf898db22931ae21a743aac`, Bitcoin block 974,722 (mined 22:42 GMT, 5 November 2026), proof [rule-book-v2.5.ots](https://trackforge.studio/docs/proofs/rule-book-v2.5.ots).
- **v2.4**, published 4 November 2026: SHA-256 `7729c243f2b2cc1ba5bfb2dd9e5618e6140508442bc4c8849b9e8afdf871b77f`, Bitcoin block 974,589 (mined 21:44 GMT, 4 November 2026), proof [rule-book-v2.4.ots](https://trackforge.studio/docs/proofs/rule-book-v2.4.ots).

Anyone can check that a rating was reached under this rule book: the rating names the hash, and the hash matches the one above and the one in the timestamp.
