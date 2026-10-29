#!/usr/bin/env python3
"""Mechanical cold-read and Appendix C checks; no semantic independence claimed."""
from __future__ import annotations
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
problems: list[str] = []
required = [
    "HANDOFF.md", "plan/PROFILE.md", "plan/PLAN.md", "plan/ASSUMPTIONS.md",
    "plan/DECISIONS.md", "plan/GATES.md", "plan/ENVIRONMENT.md",
    "plan/TRACEABILITY.md", "plan/OPERATIONS.md", "research/QUESTIONS.md",
    "research/PRIOR_KNOWLEDGE.md", "research/claims.json", "research/SOURCES.md",
    "tests/FROZEN_MANIFEST.sha256", "premortem/round-1.md",
    "premortem/round-2.md", "premortem/RISK_REGISTER.md",
    "premortem/ASSUMPTION_AUDIT.md", "reviews/COLD_READ.md",
    "reviews/CODE_REVIEW.md", "reviews/ADVERSARIAL_REVIEW.md",
    "reviews/MUTATION.md", "package-lock.json",
]
for name in required:
    if not (ROOT / name).is_file():
        problems.append(f"missing required file: {name}")

plan = (ROOT / "plan/PLAN.md").read_text()
steps = re.findall(r"^### (S-[A-Z0-9]+) ", plan, re.M)
if not steps or steps[0] != "S-000" or steps[-2:] != ["S-RETRO", "S-KNOW"]:
    problems.append(f"bad opening/closing steps: {steps[:1]} {steps[-2:]}")
for needed in ["S-REVIEW", "S-ADVERSARIAL", "S-MUTATE"]:
    if needed not in steps:
        problems.append(f"missing step {needed}")
fields = ["Tier", "Profile", "Depends on", "Inputs", "Actions", "Outputs", "Evidence produced", "Done when", "Checkpoint", "On failure", "Gate", "Relevant decisions/claims", "Lessons applied", "Exclusive resources"]
blocks = re.split(r"(?=^### S-[A-Z0-9]+ )", plan, flags=re.M)[1:]
for block in blocks:
    sid = re.match(r"### (S-[A-Z0-9]+)", block).group(1)
    for field in fields:
        if not re.search(rf"^- {re.escape(field)}: .+", block, re.M):
            problems.append(f"{sid}: missing field {field}")

claims = json.loads((ROOT / "research/claims.json").read_text())
claim_ids = {c["id"] for c in claims}
if len(claims) != 23 or len(claim_ids) != 23:
    problems.append("expected 23 unique claims")
for claim in claims:
    if claim["confidence"] not in {"corroborated", "verified"}:
        problems.append(f"{claim['id']}: confidence {claim['confidence']}")
    if not claim["informs"]:
        problems.append(f"{claim['id']}: empty informs")

test_text = "\n".join(p.read_text() for p in (ROOT / "tests").glob("*.test.ts"))
trace = (ROOT / "plan/TRACEABILITY.md").read_text()
for number in range(1, 31):
    tid = f"T-{number:03d}"
    if test_text.count(tid) != 1:
        problems.append(f"{tid}: test definition count {test_text.count(tid)}")
    if tid not in trace:
        problems.append(f"{tid}: missing trace row")

for line in (ROOT / "tests/FROZEN_MANIFEST.sha256").read_text().splitlines():
    digest, name = line.split("  ", 1)
    path = ROOT / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        problems.append(f"freeze mismatch: {name}")

texts = "\n".join(p.read_text() for p in ROOT.glob("plan/*.md")) + "\n" + plan + trace
for prefix, defined in [
    ("D", {f"D-{n:03d}" for n in range(1, 34)}),
    ("C", claim_ids),
    ("A", {f"A-{n:03d}" for n in range(1, 16)}),
    ("G", {"G-002", "G-003"}),
]:
    referenced = set(re.findall(rf"(?<![A-Z0-9]){prefix}-\d{{3}}", texts))
    for item in sorted(referenced - defined):
        problems.append(f"undefined {prefix} reference: {item}")
for path in ROOT.glob("plan/*.md"):
    for sid in re.findall(r"(?<![A-Z0-9])S-(?:\d{3}|REVIEW|ADVERSARIAL|MUTATE|RETRO|KNOW)", path.read_text()):
        if sid not in steps:
            problems.append(f"{path.name}: undefined step {sid}")

lesson_ids = {p.stem for p in (ROOT / "lessons").glob("L-*.md")}
for item in sorted(set(re.findall(r"L-\d{8}T\d{6}Z-[\w-]+", texts)) - lesson_ids):
    problems.append(f"undefined lesson reference: {item}")

REQUIRED = {
    "L": ["id", "title", "status", "supersedes", "recurrence_of", "occurrences", "severity", "tags", "recorded_by", "run", "recorded_at"],
    "K": ["id", "statement", "status", "supersedes", "tags", "applies_to_version", "source", "confidence", "derived_from", "discovered_by", "run", "recorded_at"],
}
FACETS = ("domain:", "tech:", "subject:", "phase:", "kind:", "applies:")
SECRET = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
entries = sorted([*(ROOT / "lessons").glob("**/L-*.md"), *(ROOT / "knowledge").glob("**/K-*.md")])
if len([p for p in entries if p.name.startswith("K-")]) != 23:
    problems.append("expected 23 knowledge items")
for path in entries:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    head = parts[1] if text.startswith("---") and len(parts) == 3 else ""
    fields_found = dict(re.findall(r"^(\w+):[ \t]*(.*)$", head, re.M))
    for field in REQUIRED[path.name[0]]:
        if field not in fields_found:
            problems.append(f"{path.relative_to(ROOT)}: missing {field}")
    if fields_found.get("id", "").split("#")[0].strip() != path.stem:
        problems.append(f"{path.relative_to(ROOT)}: id mismatch")
    tags = re.findall(r"[\w-]+:[\w.-]+", fields_found.get("tags", ""))
    if not tags or any(not tag.startswith(FACETS) for tag in tags):
        problems.append(f"{path.relative_to(ROOT)}: invalid tags")
    if path.name.startswith("K-") and not any(tag.startswith("subject:") for tag in tags):
        problems.append(f"{path.relative_to(ROOT)}: no subject tag")
    if SECRET.search(text):
        problems.append(f"{path.relative_to(ROOT)}: possible secret")

for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts and "node_modules" not in path.parts:
        try:
            if SECRET.search(path.read_text(encoding="utf-8")):
                problems.append(f"possible secret: {path.relative_to(ROOT)}")
        except UnicodeDecodeError:
            pass

operations = (ROOT / "plan/OPERATIONS.md").read_text()
if "./deploy/rollback.sh" not in operations:
    problems.append("operations missing rollback command")
gates = (ROOT / "plan/GATES.md").read_text()
if "G-003" not in gates or "G-002" not in gates:
    problems.append("missing gate definitions")
if not re.search(r"^Status: READY", plan, re.M):
    problems.append("plan is not READY")

risk_text = (ROOT / "premortem/RISK_REGISTER.md").read_text()
risk_rows = {}
for line in risk_text.splitlines():
    match = re.match(r"^\| (R-\d{3}) \|", line)
    if match:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        risk_rows[match.group(1)] = cells
expected_risks = {f"R-{n:03d}" for n in range(1, 16)}
if set(risk_rows) != expected_risks:
    problems.append("risk register must contain R-001 through R-015 exactly")
severities = [cells[3] for cells in risk_rows.values() if len(cells) > 3]
if {name: severities.count(name) for name in {"Critical", "High", "Medium", "Low"}} != {"Critical": 1, "High": 6, "Medium": 7, "Low": 1}:
    problems.append("risk severity counts differ from final plan header")
if "No Critical/High risk is unresolved" not in risk_text:
    problems.append("risk convergence statement missing")

audit = (ROOT / "premortem/ASSUMPTION_AUDIT.md").read_text()
verdicts = []
for prefix, count in [("A", 15), ("D", 33), ("T", 30)]:
    for number in range(1, count + 1):
        item = f"{prefix}-{number:03d}"
        rows = [line for line in audit.splitlines() if line.startswith(f"| {item} |")]
        if len(rows) != 1:
            problems.append(f"assumption audit row count for {item}: {len(rows)}")
            continue
        cells = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]
        if len(cells) < 5 or cells[3] not in {"confirmed", "falsified", "unverifiable"}:
            problems.append(f"{item}: missing or ambiguous verdict")
        else:
            verdicts.append(cells[3])
if [verdicts.count(v) for v in ("confirmed", "falsified", "unverifiable")] != [63, 0, 15]:
    problems.append("assumption-audit verdict counts differ from final totals")

state = json.loads((ROOT / ".checkpoints/state.json").read_text())
if state.get("premortem_round") != 2 or state.get("research_round") != 5:
    problems.append("checkpoint round counts are stale")
for name, digest in state.get("artifacts", {}).items():
    path = ROOT / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        problems.append(f"checkpoint artifact mismatch: {name}")
for name in ["reviews/CODE_REVIEW.md", "reviews/ADVERSARIAL_REVIEW.md", "reviews/MUTATION.md"]:
    if "Status: NOT RUN" not in (ROOT / name).read_text():
        problems.append(f"review placeholder is not honestly NOT RUN: {name}")

print("\n".join(problems) if problems else f"all mechanical checks valid: {len(steps)} steps, 30 tests, {len(claims)} claims, {len(entries)} L/K entries")
sys.exit(1 if problems else 0)
