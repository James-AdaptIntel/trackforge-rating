#!/usr/bin/env python3
"""Check a TrackForge rating statement: signature, log entry, timestamp.

Lookups only. This program does not recompute a rating, does not read the rule
book and does not judge whether the rated rows are true. It answers three
questions about a signed rating statement:

1. Was it signed by a published TrackForge signing key that was valid on the
   issue date?
2. Is its hash in the public log, is the log's chain of hashes intact, and is
   the statement still current (not replaced or withdrawn)?
3. Does the OpenTimestamps proof belong to this exact file, and (when the
   ``ots`` client is installed) does Bitcoin confirm it?

Usage::

    python check_rating.py statement SIGNED.json --keys keys/ --log log/entries.jsonl
    python check_rating.py log log/entries.jsonl --head log/heads/000003.json

Exit codes: 0 genuine, current and fully checked; 1 a check failed;
3 nothing failed but something could not be checked (no log given, ``ots``
not installed, timestamp still pending); 4 genuine but replaced or withdrawn.

The formats are specified in ``../spec/``. Requires Python 3.11+ and the
``cryptography`` package pinned in ``requirements.txt``.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

STATEMENT_FORMAT = "trackforge-rating-statement/1"
SIGNED_FORMAT = "trackforge-signed-rating-statement/1"
LOG_FORMAT = "trackforge-rating-log/1"
HEAD_FORMAT = "trackforge-rating-log-head/1"
KEY_FORMAT = "trackforge-signing-key/1"
ROTATION_FORMAT = "trackforge-key-rotation/1"

LETTERS = ("AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C", "D")
LOG_KINDS = ("issue", "replace", "withdraw")
ROTATION_REASONS = ("scheduled", "compromise")

HEX64 = re.compile(r"^[0-9a-f]{64}$")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
CATALOGUE_REF = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
RULE_BOOK_VERSION = re.compile(r"^v[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PRINTABLE_ASCII = re.compile(r"^[\x20-\x7e]*$")

# OpenTimestamps detached proof: magic, major version 1, then the file-hash
# operation tag (0x08 = SHA-256) and the 32-byte digest of the stamped file.
OTS_MAGIC = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94"
OTS_VERSION = b"\x01"
OTS_SHA256 = b"\x08"


class FormatError(ValueError):
    """A document does not follow its specification."""


# ---------------------------------------------------------------------------
# Canonical JSON and hashing
# ---------------------------------------------------------------------------


def canonical_json(value: Any) -> str:
    """The canonical form every TrackForge document is hashed and signed in.

    Byte for byte the rule-book engine's own ``canonical_json``: keys sorted,
    no whitespace, non-ASCII escaped. Documents in these formats hold only
    printable-ASCII strings, integers and null, so the bytes also equal
    RFC 8785 (JSON Canonicalization Scheme) output.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def statement_sha256(statement: dict[str, Any]) -> str:
    """The statement's identity: SHA-256 of its canonical JSON bytes."""
    return sha256_hex(canonical_bytes(statement))


def entry_sha256(entry: dict[str, Any]) -> str:
    return sha256_hex(canonical_bytes(entry))


def key_fingerprint(raw_public_key: bytes) -> str:
    """SHA-256 of the raw 32-byte Ed25519 public key, lowercase hex."""
    return sha256_hex(raw_public_key)


def load_canonical(data: bytes, what: str) -> dict[str, Any]:
    """Parse a document and insist it is stored in canonical form."""
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FormatError(f"{what}: not valid JSON ({exc})") from exc
    if not isinstance(value, dict):
        raise FormatError(f"{what}: not a JSON object")
    canonical = canonical_bytes(value)
    if data not in (canonical, canonical + b"\n"):
        raise FormatError(f"{what}: not stored in canonical JSON form")
    return value


# ---------------------------------------------------------------------------
# Field checks
# ---------------------------------------------------------------------------


def _date(value: Any, name: str) -> dt.date:
    if not isinstance(value, str) or not DATE.match(value):
        raise FormatError(f"{name} must be a YYYY-MM-DD date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise FormatError(f"{name} is not a real date") from exc


def _hex64(value: Any, name: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or not HEX64.match(value):
        raise FormatError(f"{name} must be 64 lowercase hex characters")


def _exact_keys(doc: dict[str, Any], required: set[str], what: str) -> None:
    missing = required - doc.keys()
    extra = doc.keys() - required
    if missing or extra:
        raise FormatError(f"{what}: missing {sorted(missing)}, unexpected {sorted(extra)}")


def _ascii_strings(value: Any, what: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _ascii_strings(key, what)
            _ascii_strings(item, what)
    elif isinstance(value, list):
        for item in value:
            _ascii_strings(item, what)
    elif isinstance(value, str):
        if not PRINTABLE_ASCII.match(value):
            raise FormatError(f"{what}: strings must be printable ASCII")
    elif isinstance(value, float):
        raise FormatError(f"{what}: numbers must be integers")


def _positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise FormatError(f"{name} must be a positive integer")
    return value


STATEMENT_KEYS = {
    "format",
    "rating_id",
    "catalogue_ref",
    "issue_number",
    "issue_date",
    "review_date",
    "letter",
    "tuple_hash",
    "rule_book",
    "proof_pack_sha256",
    "previous_statement_sha256",
    "signing_key",
}


def validate_statement(st: Any) -> dict[str, Any]:
    if not isinstance(st, dict):
        raise FormatError("statement: not a JSON object")
    _exact_keys(st, STATEMENT_KEYS, "statement")
    _ascii_strings(st, "statement")
    if st["format"] != STATEMENT_FORMAT:
        raise FormatError(f"statement: format must be {STATEMENT_FORMAT!r}")
    if not isinstance(st["rating_id"], str) or not UUID.match(st["rating_id"]):
        raise FormatError("rating_id must be a lowercase UUID")
    if not isinstance(st["catalogue_ref"], str) or not CATALOGUE_REF.match(st["catalogue_ref"]):
        raise FormatError("catalogue_ref must be an opaque lowercase identifier")
    issue_number = _positive_int(st["issue_number"], "issue_number")
    issued = _date(st["issue_date"], "issue_date")
    review = _date(st["review_date"], "review_date")
    if review <= issued:
        raise FormatError("review_date must fall after issue_date")
    if st["letter"] not in LETTERS:
        raise FormatError(f"letter must be one of {', '.join(LETTERS)}")
    _hex64(st["tuple_hash"], "tuple_hash")
    rule_book = st["rule_book"]
    if not isinstance(rule_book, dict):
        raise FormatError("rule_book must be an object")
    _exact_keys(rule_book, {"version", "sha256"}, "rule_book")
    if not isinstance(rule_book["version"], str) or not RULE_BOOK_VERSION.match(
        rule_book["version"]
    ):
        raise FormatError("rule_book.version must look like v2.4")
    _hex64(rule_book["sha256"], "rule_book.sha256")
    _hex64(st["proof_pack_sha256"], "proof_pack_sha256")
    _hex64(st["previous_statement_sha256"], "previous_statement_sha256", nullable=True)
    if (issue_number == 1) != (st["previous_statement_sha256"] is None):
        raise FormatError("previous_statement_sha256 is null exactly when issue_number is 1")
    _hex64(st["signing_key"], "signing_key")
    return st


def validate_signed(doc: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    _exact_keys(doc, {"format", "statement", "signature"}, "signed statement")
    if doc["format"] != SIGNED_FORMAT:
        raise FormatError(f"signed statement: format must be {SIGNED_FORMAT!r}")
    statement = validate_statement(doc["statement"])
    signature = _b64(doc["signature"], "signature", 64)
    return statement, signature


def _b64(value: Any, name: str, length: int) -> bytes:
    if not isinstance(value, str):
        raise FormatError(f"{name} must be base64 text")
    try:
        raw = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise FormatError(f"{name} is not valid base64") from exc
    if len(raw) != length or base64.b64encode(raw).decode("ascii") != value:
        raise FormatError(f"{name} must be {length} bytes in standard padded base64")
    return raw


def validate_entry(entry: dict[str, Any]) -> None:
    kind = entry.get("kind")
    required = {"format", "seq", "date", "kind", "statement_sha256", "prev_entry_sha256"}
    if kind == "replace":
        required |= {"replaces_statement_sha256"}
    _exact_keys(entry, required, f"log entry {entry.get('seq')!r}")
    if entry["format"] != LOG_FORMAT:
        raise FormatError(f"log entry: format must be {LOG_FORMAT!r}")
    if kind not in LOG_KINDS:
        raise FormatError(f"log entry kind must be one of {', '.join(LOG_KINDS)}")
    _positive_int(entry["seq"], "seq")
    _date(entry["date"], "date")
    _hex64(entry["statement_sha256"], "statement_sha256")
    _hex64(entry["prev_entry_sha256"], "prev_entry_sha256", nullable=True)
    if kind == "replace":
        _hex64(entry["replaces_statement_sha256"], "replaces_statement_sha256")


# ---------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------


@dataclass
class SigningKey:
    fingerprint: str
    public_key: Ed25519PublicKey
    holder: str
    valid_from: dt.date
    valid_until: dt.date | None = None  # set by a scheduled rotation
    revoked_from: dt.date | None = None  # set by a compromise rotation


def load_key(data: bytes, filename: str) -> SigningKey:
    doc = load_canonical(data, filename)
    _exact_keys(
        doc, {"format", "algorithm", "public_key", "fingerprint", "holder", "valid_from"}, filename
    )
    _ascii_strings(doc, filename)
    if doc["format"] != KEY_FORMAT or doc["algorithm"] != "ed25519":
        raise FormatError(f"{filename}: not a {KEY_FORMAT} ed25519 key")
    raw = _b64(doc["public_key"], "public_key", 32)
    if key_fingerprint(raw) != doc["fingerprint"]:
        raise FormatError(f"{filename}: fingerprint does not match the public key")
    if filename != f"{doc['fingerprint']}.json":
        raise FormatError(f"{filename}: key files are named <fingerprint>.json")
    if not isinstance(doc["holder"], str) or not doc["holder"]:
        raise FormatError(f"{filename}: holder must be named")
    return SigningKey(
        fingerprint=doc["fingerprint"],
        public_key=Ed25519PublicKey.from_public_bytes(raw),
        holder=doc["holder"],
        valid_from=_date(doc["valid_from"], "valid_from"),
    )


def _verify(key: SigningKey, signature: bytes, message: bytes) -> bool:
    try:
        key.public_key.verify(signature, message)
    except InvalidSignature:
        return False
    return True


def load_keyring(keys_dir: Path) -> dict[str, SigningKey]:
    """Read ``keys/<fingerprint>.json`` and apply ``keys/rotations/*.json`` in order."""
    keys: dict[str, SigningKey] = {}
    for path in sorted(keys_dir.glob("*.json")):
        key = load_key(path.read_bytes(), path.name)
        keys[key.fingerprint] = key
    rotations = sorted((keys_dir / "rotations").glob("*.json"))
    for expected_seq, path in enumerate(rotations, start=1):
        doc = load_canonical(path.read_bytes(), path.name)
        _exact_keys(
            doc, {"format", "seq", "date", "old_key", "new_key", "reason", "signatures"}, path.name
        )
        if doc["format"] != ROTATION_FORMAT or doc["reason"] not in ROTATION_REASONS:
            raise FormatError(f"{path.name}: not a valid {ROTATION_FORMAT} record")
        if doc["seq"] != expected_seq or path.name != f"{expected_seq:06d}.json":
            raise FormatError(f"{path.name}: rotations are numbered 000001.json upwards")
        when = _date(doc["date"], "date")
        _hex64(doc["old_key"], "old_key")
        _hex64(doc["new_key"], "new_key", nullable=True)
        if doc["old_key"] == doc["new_key"]:
            raise FormatError(f"{path.name}: a key cannot succeed itself")
        old = keys.get(doc["old_key"])
        new = keys.get(doc["new_key"]) if doc["new_key"] is not None else None
        if old is None or (doc["new_key"] is not None and new is None):
            raise FormatError(f"{path.name}: names a key that is not published")
        signatures = doc["signatures"]
        if not isinstance(signatures, dict):
            raise FormatError(f"{path.name}: signatures must be an object")
        body = canonical_bytes({k: v for k, v in doc.items() if k != "signatures"})
        # The new key always signs; the old key signs a scheduled rotation (and a
        # revocation with no successor). A compromised old key's signature is optional.
        allowed = {old.fingerprint} | ({new.fingerprint} if new else set())
        required = {new.fingerprint} if new else set()
        if doc["reason"] == "scheduled" or new is None:
            required.add(old.fingerprint)
        if not required <= signatures.keys() <= allowed:
            raise FormatError(f"{path.name}: needs signatures from {sorted(required)}")
        for fingerprint, sig in signatures.items():
            if not _verify(keys[fingerprint], _b64(sig, "signature", 64), body):
                raise FormatError(f"{path.name}: bad signature by {fingerprint[:16]}")
        if doc["reason"] == "scheduled":
            old.valid_until = when
        else:
            old.revoked_from = when
    return keys


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------


@dataclass
class LogState:
    entries: list[dict[str, Any]] = field(default_factory=list)
    hashes: list[str] = field(default_factory=list)
    # statement hash -> ("current" | "replaced" | "withdrawn", seq of the change)
    status: dict[str, tuple[str, int]] = field(default_factory=dict)
    replaced_by: dict[str, str] = field(default_factory=dict)
    issued_at: dict[str, int] = field(default_factory=dict)


def read_log(data: bytes) -> LogState:
    """Check every entry and the chain, and work out each statement's status."""
    state = LogState()
    previous_hash: str | None = None
    previous_date: dt.date | None = None
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    for number, line in enumerate(lines, start=1):
        entry = load_canonical(line, f"log line {number}")
        validate_entry(entry)
        if entry["seq"] != number:
            raise FormatError(f"log line {number}: seq is {entry['seq']}, expected {number}")
        if entry["prev_entry_sha256"] != previous_hash:
            raise FormatError(f"log entry {number}: chain broken (prev_entry_sha256 mismatch)")
        when = _date(entry["date"], "date")
        if previous_date is not None and when < previous_date:
            raise FormatError(f"log entry {number}: date goes backwards")
        subject = entry["statement_sha256"]
        kind = entry["kind"]
        if kind in ("issue", "replace"):
            if subject in state.status:
                raise FormatError(f"log entry {number}: statement already logged")
            if kind == "replace":
                old = entry["replaces_statement_sha256"]
                if state.status.get(old, ("",))[0] != "current":
                    raise FormatError(
                        f"log entry {number}: replaces a statement that is not current"
                    )
                state.status[old] = ("replaced", number)
                state.replaced_by[old] = subject
            state.status[subject] = ("current", number)
            state.issued_at[subject] = number
        else:  # withdraw
            if state.status.get(subject, ("",))[0] != "current":
                raise FormatError(f"log entry {number}: withdraws a statement that is not current")
            state.status[subject] = ("withdrawn", number)
        previous_hash = entry_sha256(entry)
        previous_date = when
        state.entries.append(entry)
        state.hashes.append(previous_hash)
    return state


def check_head(head_data: bytes, filename: str, state: LogState) -> dict[str, Any]:
    head = load_canonical(head_data, filename)
    _exact_keys(head, {"format", "seq", "entry_sha256"}, filename)
    if head["format"] != HEAD_FORMAT:
        raise FormatError(f"{filename}: format must be {HEAD_FORMAT!r}")
    seq = _positive_int(head["seq"], "seq")
    if filename != f"{seq:06d}.json":
        raise FormatError(f"{filename}: head files are named <seq, six digits>.json")
    if seq > len(state.hashes) or state.hashes[seq - 1] != head["entry_sha256"]:
        raise FormatError(f"{filename}: does not match log entry {seq}")
    return head


# ---------------------------------------------------------------------------
# OpenTimestamps
# ---------------------------------------------------------------------------


def ots_stamped_digest(proof: bytes) -> str:
    """The SHA-256 digest an OpenTimestamps proof was made for."""
    header = OTS_MAGIC + OTS_VERSION + OTS_SHA256
    if not proof.startswith(header) or len(proof) < len(header) + 32:
        raise FormatError("not an OpenTimestamps SHA-256 file proof")
    return proof[len(header) : len(header) + 32].hex()


def ots_verify(proof_path: Path, target: Path) -> tuple[str, str]:
    """Run ``ots verify``; returns (confirmed | pending | failed | not checked, detail).

    The ``ots`` client (``pip install opentimestamps-client``) checks the proof
    against Bitcoin block headers and needs a Bitcoin node or its own fallback
    to reach them. A proof made in the last few hours is pending until
    ``ots upgrade`` completes it.
    """
    ots = shutil.which("ots")
    if ots is None:
        return "not checked", "the ots client is not installed (pip install opentimestamps-client)"
    run = subprocess.run(  # noqa: S603 - fixed argument list, no shell
        [ots, "verify", "-f", str(target), str(proof_path)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = (run.stdout + run.stderr).strip()
    last = output.splitlines()[-1] if output else ""
    if run.returncode == 0 and "Success!" in output:
        return "confirmed", last
    if "Pending" in output:
        return "pending", last
    return "failed", last or f"ots exited {run.returncode}"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


class Report:
    def __init__(self) -> None:
        self.failed = False
        self.unchecked = False
        self.not_current = False

    def line(self, verdict: str, text: str) -> None:
        print(f"{verdict:<12} {text}")
        if verdict == "FAIL":
            self.failed = True
        elif verdict == "NOT CHECKED":
            self.unchecked = True

    def exit_code(self) -> int:
        if self.failed:
            return 1
        if self.not_current:
            return 4
        return 3 if self.unchecked else 0


def check_timestamp(report: Report, target: Path, proof_path: Path, label: str) -> None:
    if not proof_path.exists():
        report.line("NOT CHECKED", f"{label}: no timestamp proof at {proof_path}")
        return
    try:
        stamped = ots_stamped_digest(proof_path.read_bytes())
    except FormatError as exc:
        report.line("FAIL", f"{label}: {exc}")
        return
    if stamped != sha256_hex(target.read_bytes()):
        report.line("FAIL", f"{label}: the timestamp proof is for a different file")
        return
    report.line("PASS", f"{label}: timestamp proof is for this file")
    verdict, detail = ots_verify(proof_path, target)
    if verdict == "confirmed":
        report.line("PASS", f"{label}: Bitcoin confirms it: {detail}")
    elif verdict == "failed":
        report.line("FAIL", f"{label}: ots verify failed: {detail}")
    else:
        report.line("NOT CHECKED", f"{label}: Bitcoin confirmation {verdict}: {detail}")


def cmd_statement(args: argparse.Namespace) -> int:
    report = Report()
    signed_path = Path(args.signed)
    signed_bytes = signed_path.read_bytes()
    try:
        doc = load_canonical(signed_bytes, signed_path.name)
        statement, signature = validate_signed(doc)
    except FormatError as exc:
        report.line("FAIL", str(exc))
        return report.exit_code()
    digest = statement_sha256(statement)
    print(f"statement    {digest}")
    print(
        f"rating       {statement['rating_id']} issue {statement['issue_number']}, "
        f"letter {statement['letter']}, issued {statement['issue_date']}, "
        f"review {statement['review_date']}, rule book {statement['rule_book']['version']}"
    )

    # 1. Signature against a published key valid on the issue date.
    try:
        keys = load_keyring(Path(args.keys))
    except FormatError as exc:
        report.line("FAIL", f"keys: {exc}")
        return report.exit_code()
    key = keys.get(statement["signing_key"])
    issued = dt.date.fromisoformat(statement["issue_date"])
    if key is None:
        report.line("FAIL", "signature: signing key is not among the published keys")
    elif not _verify(key, signature, canonical_bytes(statement)):
        report.line("FAIL", f"signature: does not verify against key {key.fingerprint}")
    else:
        report.line("PASS", f"signature: valid, key {key.fingerprint} ({key.holder})")
        if issued < key.valid_from or (key.valid_until and issued >= key.valid_until):
            report.line("FAIL", "signature: key was not in service on the issue date")
        elif key.revoked_from and issued >= key.revoked_from:
            report.line("FAIL", f"signature: key revoked from {key.revoked_from}")
        elif key.revoked_from:
            report.line(
                "WARN",
                f"signature: key revoked from {key.revoked_from}; rely on it only if the "
                "timestamp below confirms the statement existed before that date",
            )

    # 2. The log.
    if args.log is None:
        report.line("NOT CHECKED", "log: no log given (--log)")
    else:
        try:
            state = read_log(Path(args.log).read_bytes())
        except FormatError as exc:
            report.line("FAIL", f"log: {exc}")
        else:
            report.line("PASS", f"log: {len(state.entries)} entries, chain intact")
            _statement_in_log(report, statement, digest, state)

    # 3. The timestamp on the signed file.
    proof = Path(args.ots) if args.ots else signed_path.with_name(signed_path.name + ".ots")
    check_timestamp(report, signed_path, proof, "timestamp")

    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.UTC).date()
    if today > dt.date.fromisoformat(statement["review_date"]):
        report.line("NOTE", f"past review date ({statement['review_date']})")
    return report.exit_code()


def _statement_in_log(
    report: Report, statement: dict[str, Any], digest: str, state: LogState
) -> None:
    if digest not in state.issued_at:
        report.line("FAIL", "log: statement is not in the log")
        return
    entry = state.entries[state.issued_at[digest] - 1]
    previous = statement["previous_statement_sha256"]
    if entry["kind"] == "replace" and entry["replaces_statement_sha256"] != previous:
        report.line("FAIL", "log: entry replaces a different statement from the one it names")
        return
    if entry["kind"] == "issue" and previous is not None:
        prior = state.status.get(previous)
        if prior is None or prior[0] != "withdrawn" or prior[1] > entry["seq"]:
            report.line(
                "FAIL", "log: a later issue must replace its predecessor or follow a withdrawal"
            )
            return
    report.line("PASS", f"log: logged at entry {entry['seq']} ({entry['kind']}, {entry['date']})")
    status, seq = state.status[digest]
    if status == "current":
        report.line("STATUS", "current")
    elif status == "replaced":
        report.line(
            "STATUS", f"replaced at log entry {seq} by statement {state.replaced_by[digest]}"
        )
        report.not_current = True
    else:
        report.line("STATUS", f"withdrawn at log entry {seq}")
        report.not_current = True


def cmd_log(args: argparse.Namespace) -> int:
    report = Report()
    try:
        state = read_log(Path(args.log).read_bytes())
    except FormatError as exc:
        report.line("FAIL", f"log: {exc}")
        return report.exit_code()
    report.line("PASS", f"log: {len(state.entries)} entries, chain intact")
    if state.hashes:
        print(f"head         entry {len(state.hashes)} {state.hashes[-1]}")
    for head in args.head or ():
        head_path = Path(head)
        try:
            parsed = check_head(head_path.read_bytes(), head_path.name, state)
        except FormatError as exc:
            report.line("FAIL", str(exc))
            continue
        report.line("PASS", f"head {parsed['seq']}: matches the log")
        check_timestamp(
            report, head_path, head_path.with_name(head_path.name + ".ots"), f"head {parsed['seq']}"
        )
    return report.exit_code()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    st = sub.add_parser("statement", help="check a signed rating statement")
    st.add_argument("signed", help="the signed statement file (*.signed.json)")
    st.add_argument("--keys", required=True, help="the published keys/ directory")
    st.add_argument("--log", help="the published log/entries.jsonl")
    st.add_argument("--ots", help="timestamp proof (default: <signed>.ots)")
    st.add_argument("--today", help="date to judge the review date against (YYYY-MM-DD)")
    st.set_defaults(func=cmd_statement)
    lg = sub.add_parser("log", help="check the log's chain and any timestamped heads")
    lg.add_argument("log", help="log/entries.jsonl")
    lg.add_argument("--head", action="append", help="a log/heads/<seq>.json file (repeatable)")
    lg.set_defaults(func=cmd_log)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
