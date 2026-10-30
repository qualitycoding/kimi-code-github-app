#!/usr/bin/env python3
"""Mechanical cold-read, Appendix C, and protocol v3.6 checks; no semantic independence claimed."""
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
    "plan/amendment-v36/EXECUTION_LOG.md", "plan/amendment-v36/DEVIATIONS.md",
    "plan/amendment-v36/ENVIRONMENT_PROBE.md",
    "research/spikes/v36-command-verification/README.md",
    "research/spikes/v36-command-verification/output.txt",
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
block_by_id = {}
for block in blocks:
    sid = re.match(r"### (S-[A-Z0-9]+)", block).group(1)
    block_by_id[sid] = block
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
    ("D", {f"D-{n:03d}" for n in range(1, 35)}),
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
knowledge_entries = [p for p in entries if p.name.startswith("K-")]
lk_count = len(entries)
if len(knowledge_entries) != 23:
    problems.append(f"knowledge item count changed from baseline 23: {len(knowledge_entries)}")
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

# ---------------------------------------------------------------------------
# Protocol v3.6 amendment checks (findings C-01, H-01..H-04, M-01..M-05)
# ---------------------------------------------------------------------------
handoff = (ROOT / "HANDOFF.md").read_text()
env_text = (ROOT / "plan/ENVIRONMENT.md").read_text()
profile_text = (ROOT / "plan/PROFILE.md").read_text()
state = json.loads((ROOT / ".checkpoints/state.json").read_text())
spike_readme = (ROOT / "research/spikes/v36-command-verification/README.md").read_text()

def done_when(sid: str) -> str:
    m = re.search(r"^- Done when: (.+)$", block_by_id[sid], re.M)
    return m.group(1) if m else ""

# H-02 / M-05: environment class recorded in PROFILE and checkpoint state
if not re.search(r"^-\s*environment_class:\s*(ephemeral|stable)\s*$", profile_text, re.M):
    problems.append("v3.6/H-02: plan/PROFILE.md missing 'environment_class: ephemeral|stable'")
if state.get("environment_class") not in {"ephemeral", "stable"}:
    problems.append("v3.6/H-02: .checkpoints/state.json missing environment_class")
env_class = state.get("environment_class", "")
if env_class == "ephemeral" and "plan/amendment-v36/ENVIRONMENT_PROBE.md" not in profile_text:
    problems.append("v3.6/H-02: PROFILE.md does not reference the probe evidence path")

# H-01: Rule 6 cadence in HANDOFF.md and PLAN.md, per-step persistence, remote-HEAD Done when
for needle in ["ls-remote", "gate record", "EXECUTION_LOG.md", "never force-push"]:
    if needle not in handoff:
        problems.append(f"v3.6/H-01: HANDOFF.md persistence rule missing '{needle}'")
if "Protocol v3.6 persistence rule" not in plan:
    problems.append("v3.6/H-01: PLAN.md missing the global persistence rule section")
for sid in steps:
    block = block_by_id[sid]
    if "Persistence (v3.6 Rule 6):" not in block:
        problems.append(f"v3.6/H-01: {sid}: missing Persistence (v3.6 Rule 6) action")
    dw = done_when(sid)
    if "ls-remote" not in dw or "remote HEAD" not in dw:
        problems.append(f"v3.6/H-01: {sid}: Done when missing remote-HEAD ls-remote verification")

# C-01: universal artifact clause + specific postcondition markers
UNIVERSAL = "every path listed in Outputs exists"
SPECIFIC_MARKERS = {
    "S-000": "environment class, remote head, and setup-check results",
    "S-002": "concurrent-refresh, replay, redaction, and fixed-clock results",
    "S-003": "redirect-to-private and DNS-rebinding cases",
    "S-004": "no pre-consent GitHub redirect and no GitHub token in browser or MCP output",
    "S-005": "wrong-resource and wrong-audience rejection",
    "S-006": "cross-tenant 404 behavior and refresh-generation protection",
    "S-007": "distinguishes connector truncation from GitHub truncation and records memory-bound results",
    "S-008": "exactly three exposed tools and unauthenticated rejection",
    "S-009": "duplicate webhook delivery, revocation, and sweep behavior",
    "S-010": "kimi.plugin.json` and the administrator/user documentation exist, validate, and contain no PAT or secret field",
    "S-011": "research/results/aggregate-test-log.json` records all frozen tests with zero skips or expected failures",
    "S-012": "research/results/performance-summary.json` contains five runs",
    "S-015": "personal/organization and all/selected repository matrix",
    "S-ADVERSARIAL": "reviews/ADVERSARIAL_REVIEW.md` records every confirmed break and disposition",
    "S-MUTATE": "reviews/MUTATION.md` records the score and every survivor class or justification",
    "S-019": "RELEASE_VERIFICATION.md` records the 60-minute checks, alert result, and revocation result",
    "S-RETRO": "RETROSPECTIVE.md` records every finding, its L/K links, and the deviation-diff result",
}
for sid in steps:
    if UNIVERSAL not in done_when(sid):
        problems.append(f"v3.6/C-01: {sid}: Done when missing universal artifact clause")
for sid, marker in SPECIFIC_MARKERS.items():
    if sid not in block_by_id or marker not in block_by_id[sid]:
        problems.append(f"v3.6/C-01: {sid}: missing specific artifact postcondition")

# H-03/H-04: command/pin evidence matrix, per-pin verdict, runner class
if "Amendment v3.6 command/pin evidence matrix" not in env_text:
    problems.append("v3.6/H-03: plan/ENVIRONMENT.md missing the evidence matrix")
if "linux-x86_64-2vCPU-4GiB-fuse.portal" not in env_text:
    problems.append("v3.6/H-04: plan/ENVIRONMENT.md missing the runner class")
if "runner-class-specific" not in env_text:
    problems.append("v3.6/H-04: runner-class specificity rule missing")
matrix_rows = [ln for ln in spike_readme.splitlines()
               if ln.startswith("| ") and "---" not in ln and "Evidence class" not in ln]
if len(matrix_rows) < 15:
    problems.append(f"v3.6/H-03: evidence matrix too small ({len(matrix_rows)} rows)")
EVIDENCE_CLASSES = ("planner-spike", "official-docs-locator", "registry-metadata",
                     "official-images-manifest", "blocked-unverified")
for ln in matrix_rows:
    low = ln.lower()
    if not any(cls in low for cls in EVIDENCE_CLASSES):
        problems.append(f"v3.6/H-03: matrix row without an evidence class or verdict: {ln[:80]}")
if "blocked-unverified" not in spike_readme.lower():
    problems.append("v3.6/H-03: spike does not record any blocked-unverified item")

# H-02: ephemeral execution and resumability rules
if env_class == "ephemeral":
    for needle in ["Ephemeral execution", "On container loss", ".runtime/"]:
        if needle not in handoff:
            problems.append(f"v3.6/H-02: HANDOFF.md ephemeral section missing '{needle}'")
    for sid in steps:
        if "Resumption (v3.6):" not in block_by_id[sid]:
            problems.append(f"v3.6/H-02: {sid}: missing turn-start Resumption check")
    if "Ephemeral environment (v3.6)" not in block_by_id.get("S-000", ""):
        problems.append("v3.6/H-02: S-000 missing the ephemeral environment action")

# M-02: S-RETRO deviation-diff procedure and artifact
retro = block_by_id.get("S-RETRO", "")
if "reviews/RETRO_DEVIATION_DIFF.md" not in retro:
    problems.append("v3.6/M-02: S-RETRO does not name reviews/RETRO_DEVIATION_DIFF.md")
if "git diff --stat" not in retro or "git log --oneline --name-only" not in retro:
    problems.append("v3.6/M-02: S-RETRO missing the deviation-diff procedure")
if "unlogged" not in done_when("S-RETRO"):
    problems.append("v3.6/M-02: S-RETRO Done when missing the zero-unlogged-substitutions result")

# M-03: immediate deviation logging
if "at the moment it is made" not in handoff:
    problems.append("v3.6/M-03: HANDOFF.md missing the immediate-deviation-logging rule")
for sid in ["S-000", "S-001", "S-012", "S-013", "S-014", "S-017"]:
    if "Deviations (v3.6):" not in block_by_id.get(sid, ""):
        problems.append(f"v3.6/M-03: {sid}: missing explicit deviation action")

# M-01: stale checkpoint push state removed, remote head recorded
if any("external-generation-branch-push" in x for x in state.get("pending", [])):
    problems.append("v3.6/M-01: state.json still lists the external push as pending")
if not state.get("verified_remote_head"):
    problems.append("v3.6/M-01: state.json missing verified_remote_head")
if state.get("amendment_decision") != "D-034":
    problems.append("v3.6/M-01: state.json missing amendment decision D-034")

# v3.6 status header: READY or BLOCKED, both truthful forms only
if not re.search(r"^Status: (READY|BLOCKED — HUMAN DECISION REQUIRED)", plan, re.M):
    problems.append("v3.6: plan status header must be READY or BLOCKED — HUMAN DECISION REQUIRED")

# M-04 support: failure-swallowing idiom scan over plan-specified commands
SWALLOW = re.compile(r"\|\|\s*(true|:)\b|2>/dev/null|;[\s]*true\b")
for doc in [plan, env_text, handoff]:
    for cmd_block in re.findall(r"```sh\n(.*?)```", doc, re.S):
        for ln in cmd_block.splitlines():
            if SWALLOW.search(ln):
                problems.append(f"v3.6/M-04: failure-swallowing idiom in plan command: {ln.strip()[:90]}")

# Dynamic cross-checks: plan header counts vs actual artifact rows
header = plan.split("### S-000")[0]
m = re.search(r"Risks: (\d+) total — (\d+) Critical[^\n]*", header)
risk_text = (ROOT / "premortem/RISK_REGISTER.md").read_text()
risk_rows = {}
for line in risk_text.splitlines():
    match = re.match(r"^\| (R-\d{3}) \|", line)
    if match:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        risk_rows[match.group(1)] = cells
severities = [cells[3] for cells in risk_rows.values() if len(cells) > 3]
actual_counts = {name: severities.count(name) for name in {"Critical", "High", "Medium", "Low"}}
if m:
    declared = {"Critical": int(m.group(2)), "High": actual_counts["High"] and int(re.search(r"(\d+) High", header).group(1)),
                "Medium": int(re.search(r"(\d+) Medium", header).group(1)), "Low": int(re.search(r"(\d+) Low", header).group(1))}
    if int(m.group(1)) != len(risk_rows) or actual_counts != declared:
        problems.append(f"v3.6: risk header/register mismatch: header={declared} register={actual_counts}")
if "No Critical/High risk is unresolved" not in risk_text:
    problems.append("risk convergence statement missing")

audit = (ROOT / "premortem/ASSUMPTION_AUDIT.md").read_text()
verdicts = []
decisions_text = (ROOT / "plan/DECISIONS.md").read_text()
d_count = len({int(n) for n in re.findall(r"(?<![A-Z0-9])D-(\d{3})", decisions_text)})
for prefix, count in [("A", 15), ("D", d_count), ("T", 30)]:
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
audit_counts = [verdicts.count(v) for v in ("confirmed", "falsified", "unverifiable")]
am = re.search(r"Assumption audit: (\d+) items — (\d+) confirmed, (\d+) falsified, (\d+) unverifiable", header)
if am:
    if [int(am.group(2)), int(am.group(3)), int(am.group(4))] != audit_counts or int(am.group(1)) != len(verdicts):
        problems.append(f"v3.6: assumption-audit header mismatch: header={[am.group(2), am.group(3), am.group(4)]} actual={audit_counts}")

if int(state.get("premortem_round", 0)) < 2 or state.get("research_round") != 5:
    problems.append("checkpoint round counts are stale")
for name, digest in state.get("artifacts", {}).items():
    path = ROOT / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        problems.append(f"checkpoint artifact mismatch: {name}")
for name in ["reviews/CODE_REVIEW.md", "reviews/ADVERSARIAL_REVIEW.md", "reviews/MUTATION.md"]:
    if "Status: NOT RUN" not in (ROOT / name).read_text():
        problems.append(f"review placeholder is not honestly NOT RUN: {name}")

print("\n".join(problems) if problems else
      f"all mechanical checks valid (v3.4 + v3.6): {len(steps)} steps, 30 tests, {len(claims)} claims, {lk_count} L/K entries")
sys.exit(1 if problems else 0)
