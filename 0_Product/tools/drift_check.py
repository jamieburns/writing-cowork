#!/usr/bin/env python3
"""
writing-cowork plugin / tools/drift_check.py — multi-project vault drift check.

Ships bundled inside the writing-cowork plugin (${CLAUDE_PLUGIN_ROOT}/tools/
drift_check.py) as of the plugin's drift-check incorporation pass
(2026-07-22). Previously lived in a separate cowork-tools repo
(~/code/cowork-tools/drift_check.py) — see DRIFT_CHECK_VERSION below for
this script's own version, independent of the plugin's version, since the
two can in principle be patched on different cadences.

Reads per-project config from YAML and runs eight checks per project:
  1. File inventory drift — vault files not in ownership table; ownership entries
     with no file on disk.
  2. Cross-reference validation — markdown links / image refs that don't resolve.
  3. Build freshness — source markdown vs. last-built deliverable mtimes
     (skipped if config build.enabled = false).
  4. Gitignored items in vault — surfaces scratch / build outputs that are present.
  5. Inbox surface — counts items in configured inbox buckets;
     flags items older than inbox.overdue_days as overdue.
  6. Cross-phase dependency change detection — warns on NEW dependencies across phases
     (v0.1.14 enhancement).
  7. Workstream status block staleness — detects status blocks not updated beyond threshold
     (v0.1.14 enhancement).
  8. Early-exit optimization — skips full check if no changes since last run;
     auto-disables after 7 days of inactivity (v0.1.14 enhancement).

Writes results to (per project, configured paths):
  - hub:           <!-- DRIFT-ATTENTION-START/END --> block (visible to writer)
  - ownership:     <!-- DRIFT-FOOTER-START/END --> block (operational footer)
  - drift_flag:    marker file (present iff drift detected)
  - reports_dir:   <date>.md detailed report (written on drift only)

Modes:
  drift_check.py --config /path/to/project.yaml   # single project
  drift_check.py --all                            # all enabled projects in registry
  drift_check.py --project NAME                   # named project from registry
  drift_check.py --registry /path                 # override registry location
  drift_check.py --dry-run                        # don't write outputs
  drift_check.py --version                        # print this script's own version and exit

Default registry: ~/.config/cowork/registry.yaml

Silent if clean; reports only on drift (per data-management charter).

Requires PyYAML. Install: pip3 install pyyaml --break-system-packages
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERROR: PyYAML not installed.\n"
        "Install: pip3 install pyyaml --break-system-packages\n"
    )
    sys.exit(2)


# ════════════════════════════════════════════════════════════════════════════ config

# This script's own version — independent of the writing-cowork plugin's
# version (plugin.json). Bump whenever this file's logic changes, on
# whatever cadence that happens, not necessarily in lockstep with a plugin
# release. Printed via --version and stamped into every report header, so
# a project's actual running script version can be confirmed directly
# rather than assumed from the plugin version alone.
DRIFT_CHECK_VERSION = "0.4.0"  # 2026-07-31: config preflight — unreadable input is a finding, not silence

DEFAULT_REGISTRY = Path.home() / ".config" / "cowork" / "registry.yaml"

# Every top-level key this script understands. Anything else in a
# drift_check.yaml is reported rather than ignored — see check_config_preflight.
# A key that is silently dropped is indistinguishable from a key that works,
# which is how `priority_prefixes` sat in planning docs for over a week as a
# settled mechanism that had never been written (task 6b91e2a5).
CONFIG_KNOWN_KEYS = {
    "project_name", "vault", "hub", "ownership_table", "drift_flag",
    "reports_dir", "exclude_prefixes", "exclude_patterns", "generated_patterns",
    "build", "xref_targets", "inbox", "markers", "checks", "session_hygiene",
}

DEFAULT_MARKERS = {
    "attention_start": "<!-- DRIFT-ATTENTION-START -->",
    "attention_end":   "<!-- DRIFT-ATTENTION-END -->",
    "footer_start":    "<!-- DRIFT-FOOTER-START -->",
    "footer_end":      "<!-- DRIFT-FOOTER-END -->",
}


class ProjectConfig:
    """Loaded per-project drift_check.yaml, with paths resolved against vault."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        self.unknown_keys = sorted(set(data.keys()) - CONFIG_KNOWN_KEYS)

        self.name = data.get("project_name") or config_path.parent.parent.parent.name
        vault_str = data.get("vault")
        if not vault_str:
            raise ValueError(f"{config_path}: 'vault' is required")
        self.vault = Path(os.path.expanduser(vault_str))

        # Resolved file paths
        self.hub             = self.vault / data.get("hub", "project_hub.md")
        self.ownership_table = self.vault / data.get(
            "ownership_table", "process/data_management/file_ownership.md"
        )
        self.drift_flag      = self.vault / data.get(
            "drift_flag", "process/data_management/.drift_flag"
        )
        self.reports_dir     = self.vault / data.get(
            "reports_dir", "process/data_management/drift_reports"
        )

        # Inventory filters
        self.exclude_prefixes = tuple(data.get("exclude_prefixes", []))
        self.exclude_patterns = [re.compile(p) for p in data.get("exclude_patterns", [])]
        self.generated_patterns = [re.compile(p) for p in data.get("generated_patterns", [])]

        # Build
        build = data.get("build", {}) or {}
        self.build_enabled = bool(build.get("enabled", False))
        self.build_sources = [self.vault / s for s in build.get("sources", [])]
        self.build_outputs = [self.vault / o for o in build.get("outputs", [])]
        self.build_grace_seconds = int(build.get("grace_seconds", 300))

        # Cross-references
        self.xref_targets = [self.vault / x for x in data.get("xref_targets", [])]

        # Inbox
        inbox = data.get("inbox", {}) or {}
        self.inbox_buckets = inbox.get("buckets", ["external", "promotion"])
        self.inbox_overdue_days = int(inbox.get("overdue_days", 14))

        # Markers
        markers = data.get("markers", {}) or {}
        self.markers = {**DEFAULT_MARKERS, **markers}

        # v0.1.14: Cross-phase dependency detection
        checks = data.get("checks", []) or []
        self.cross_phase_config = {}
        for check in checks:
            if check.get("type") == "cross-phase-dependency-change":
                self.cross_phase_config = check
                break

        # v0.1.14: Workstream status block staleness
        self.workstream_status_config = {}
        for check in checks:
            if check.get("type") == "workstream-status-staleness":
                self.workstream_status_config = check
                break

        # 2026-07-27: session hygiene — is anything hidden, stale, or stranded?
        sh = data.get("session_hygiene", {}) or {}
        self.session_hygiene_enabled = bool(sh.get("enabled", False))
        self.sh_uncommitted  = sh.get("uncommitted_durable", {}) or {}
        self.sh_log          = sh.get("log_unlanded", {}) or {}
        self.sh_memory_path  = sh.get("memory_path", {}) or {}
        self.sh_markers      = sh.get("managed_markers", {}) or {}


# ════════════════════════════════════════════════════════════════════════════ helpers

def excluded(rel_path: str, config: ProjectConfig) -> bool:
    if any(rel_path == p or rel_path.startswith(p + "/") for p in config.exclude_prefixes):
        return True
    return any(p.search(rel_path) for p in config.exclude_patterns)


def is_generated(rel_path: str, config: ProjectConfig) -> bool:
    return any(p.search(rel_path) for p in config.generated_patterns)


def all_vault_files(config: ProjectConfig):
    """Yield vault-relative path strings for every non-excluded file."""
    for root, dirs, files in os.walk(config.vault):
        rel_root = os.path.relpath(root, config.vault)
        if rel_root == ".":
            rel_root = ""
        dirs[:] = [
            d for d in dirs
            if not excluded((rel_root + "/" + d).lstrip("/"), config)
        ]
        for f in files:
            rel = (rel_root + "/" + f).lstrip("/")
            if not excluded(rel, config):
                yield rel


def count_files(folder_path):
    """Count files in folder, excluding dotfiles (for .gitkeep fix)."""
    if not os.path.isdir(folder_path):
        return 0
    files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
    return len(files)


def parse_ownership_paths(config: ProjectConfig):
    """Parse file_ownership.md table rows. Returns set of vault-relative paths.

    Rules:
      - Track current section header. If a section heading contains '(<path>/)' in
        parens, that path becomes the prefix for bare filenames in that section's
        table rows.
      - Skip the 'Long tail' section entirely (informational, not authoritative).
      - For each table row (line starting with '|'), extract only the FIRST cell's
        backticked value. Notes column content is ignored.
    """
    if not config.ownership_table.exists():
        return set()

    paths = set()
    current_prefix = ""
    in_long_tail = False

    for raw_line in config.ownership_table.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.rstrip()
        stripped = line.lstrip()

        m_h = re.match(r"^##\s+(.*)$", stripped)
        if m_h:
            heading = m_h.group(1).strip()
            in_long_tail = "long tail" in heading.lower()
            if in_long_tail:
                continue
            m_pre = re.search(r"\(([A-Za-z0-9_/.\- ]+/)\)?", heading)
            current_prefix = m_pre.group(1).strip() if m_pre else ""
            if "/" not in current_prefix:
                current_prefix = ""
            continue

        if in_long_tail:
            continue

        if not stripped.startswith("|"):
            continue
        if "----" in stripped or stripped.lower().startswith("| file |") or stripped.lower().startswith("| path |"):
            continue

        cells = stripped.split("|")
        if len(cells) < 3:
            continue
        first_cell = cells[1].strip()

        m = re.search(r"`([^`]+)`", first_cell)
        if not m:
            continue
        path_val = m.group(1).strip()

        candidates = [path_val]
        if current_prefix and not path_val.startswith(current_prefix):
            candidates.append(current_prefix + path_val)

        resolved = None
        for c in candidates:
            target = config.vault / c
            if c.endswith("/"):
                if target.exists() and target.is_dir():
                    resolved = c
                    break
            else:
                if target.exists():
                    resolved = c
                    break
        paths.add(resolved if resolved else candidates[-1])

    return paths


# ════════════════════════════════════════════════════════════════════════════ checks

def get_latest_commit_time(vault_path: Path):
    """Get timestamp of latest commit in vault. Returns None if git not available."""
    try:
        result = subprocess.run(
            ["git", "-C", str(vault_path), "log", "-1", "--format=%ci", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            # Parse git timestamp (format: 2026-05-23 14:00:00 +0000)
            ts_str = result.stdout.strip().split()[0]
            return datetime.fromisoformat(ts_str)
        return None
    except Exception:
        return None


def should_skip_full_check(vault_path: Path):
    """Check if full drift check should be skipped due to no changes.
    Returns (should_skip: bool, reason: str or None)
    """
    last_run_file = vault_path / ".drift_last_run"
    if not last_run_file.exists():
        return False, None  # first run, don't skip

    try:
        last_run_content = last_run_file.read_text(encoding="utf-8").strip()
        last_run_time = datetime.fromisoformat(last_run_content)
    except Exception:
        return False, None

    last_commit_time = get_latest_commit_time(vault_path)
    if not last_commit_time:
        return False, None  # can't determine, run full check

    if last_commit_time <= last_run_time:
        return True, "no_changes"

    return False, None


def record_drift_run_time(vault_path: Path, dry_run=False):
    """Record the time of this drift check run."""
    if dry_run:
        return
    last_run_file = vault_path / ".drift_last_run"
    last_run_file.parent.mkdir(parents=True, exist_ok=True)
    last_run_file.write_text(datetime.now().isoformat(), encoding="utf-8")


def check_config_preflight(config: ProjectConfig):
    """Report configuration this script cannot act on, before any check runs.

    Two failure modes, both of which previously produced a clean report:

      1. A key in drift_check.yaml that this script does not read. YAML accepts
         it, ProjectConfig ignores it, and nothing ever says so.
      2. A check whose input file does not exist. The check returns [], which
         renders identically to "ran and found nothing".

    Neither is an error — a project may legitimately not use a mechanism. But
    the difference between "clean" and "not looked at" has to be visible, or a
    green report means nothing. See Decisions.md, "Hygiene checks fail loudly".
    """
    issues = []

    if config.unknown_keys:
        issues.append({
            "kind": "config_unknown_keys",
            "summary": "Config — %d unrecognized key(s) in drift_check.yaml, silently ignored: %s"
                       % (len(config.unknown_keys), ", ".join(config.unknown_keys)),
            "details": {
                "config": str(config.config_path),
                "unknown": config.unknown_keys,
                "known": sorted(CONFIG_KNOWN_KEYS),
            },
        })

    # (label, path, what is lost when it is missing)
    declared = [
        ("inventory/ownership", config.ownership_table,
         "no provenance registry; the unaccounted-files check cannot run"),
        ("hub", config.hub,
         "the attention block has nowhere to be written"),
        ("cross-phase dependency", config.vault / "process/active/todos.md",
         "task rows cannot be read (this path is hardcoded, not configurable — task 7e4b1a93)"),
        ("workstream status staleness", config.vault / "process/active/roadmap.md",
         "phases cannot be read (this path is hardcoded, not configurable — task 7e4b1a93)"),
    ]

    sh_log = (config.sh_log or {}).get("path")
    if sh_log:
        declared.append(("session hygiene / log_unlanded", config.vault / sh_log,
                         "unlanded activity-log entries cannot be detected"))
    for f in (config.sh_markers or {}).get("files", []):
        declared.append(("session hygiene / managed_markers", config.vault / f,
                         "marker balance cannot be verified for this file"))
    for x in config.xref_targets:
        declared.append(("xref target", x, "its links cannot be validated"))

    missing = [(label, str(path), why) for label, path, why in declared
               if not Path(path).exists()]
    for label, path, why in missing:
        rel = path.replace(str(config.vault) + "/", "")
        issues.append({
            "kind": "config_input_missing",
            "summary": 'Config — check "%s" has no input at %s; %s' % (label, rel, why),
            "details": {"check": label, "path": path},
        })

    return issues


def check_inventory(config: ProjectConfig):
    issues = []
    vault_files = set(all_vault_files(config))

    # 2026-07-31: with no ownership table every file is "unaccounted", which
    # produced a single 131-file line that drowned the real findings under it.
    # check_config_preflight already reports the absent table once, precisely;
    # repeating it per-file is the noise this project keeps trying to kill.
    if not config.ownership_table.exists():
        generated_present = [r for r in sorted(vault_files) if is_generated(r, config)]
        return issues, generated_present

    ownership_paths = parse_ownership_paths(config)

    unaccounted = []
    generated_present = []
    for rel in sorted(vault_files):
        if is_generated(rel, config):
            generated_present.append(rel)
            continue
        if rel not in ownership_paths:
            parent = os.path.dirname(rel)
            covered_by_dir = any(
                o.rstrip("/") == parent or rel.startswith(o)
                for o in ownership_paths if o.endswith("/")
            )
            if not covered_by_dir:
                unaccounted.append(rel)
    if unaccounted:
        issues.append({
            "kind": "inventory_unaccounted",
            "summary": f"{len(unaccounted)} file(s) in vault not listed in file_ownership.md",
            "details": unaccounted,
        })

    missing = []
    for o in sorted(ownership_paths):
        if o.endswith("/"):
            full = config.vault / o
            if not full.exists() or not full.is_dir():
                missing.append(o)
        else:
            if not (config.vault / o).exists():
                missing.append(o)
    if missing:
        issues.append({
            "kind": "inventory_missing",
            "summary": f"{len(missing)} ownership entr(y/ies) with no corresponding file",
            "details": missing,
        })

    return issues, generated_present


XREF_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def check_xrefs(config: ProjectConfig):
    issues = []
    broken = []
    for src in config.xref_targets:
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        for m in XREF_RE.finditer(text):
            target = m.group(1).strip()
            if re.match(r"^[a-z]+://", target) or target.startswith("#") or target.startswith("mailto:"):
                continue
            target = target.split("#")[0].split("?")[0]
            if not target:
                continue
            resolved = (src.parent / target).resolve()
            if not resolved.exists():
                broken.append({
                    "in": str(src.relative_to(config.vault)),
                    "ref": target,
                })
    if broken:
        issues.append({
            "kind": "xref_broken",
            "summary": f"{len(broken)} broken cross-reference(s) in core docs",
            "details": broken,
        })
    return issues


def check_build_freshness(config: ProjectConfig):
    issues = []
    if not config.build_enabled:
        return issues
    if not config.build_sources:
        return issues
    if not all(s.exists() for s in config.build_sources):
        return issues
    latest_src = max(s.stat().st_mtime for s in config.build_sources)
    src_dt = datetime.fromtimestamp(latest_src)

    if not all(o.exists() for o in config.build_outputs):
        missing = [o.name for o in config.build_outputs if not o.exists()]
        issues.append({
            "kind": "build_missing",
            "summary": f"{len(missing)} build output(s) not present",
            "details": missing,
        })
        return issues

    stale = []
    for out in config.build_outputs:
        out_mtime = out.stat().st_mtime
        if (latest_src - out_mtime) > config.build_grace_seconds:
            delta_hours = (latest_src - out_mtime) / 3600
            stale.append({
                "out": out.name,
                "out_mtime": datetime.fromtimestamp(out_mtime).isoformat(timespec="seconds"),
                "latest_src_mtime": src_dt.isoformat(timespec="seconds"),
                "stale_by_hours": f"{delta_hours:.1f}",
            })
    if stale:
        issues.append({
            "kind": "build_stale",
            "summary": f"{len(stale)} build output(s) older than latest source change",
            "details": stale,
        })
    return issues


def check_inbox(config: ProjectConfig):
    issues = []
    info = {}
    for bucket in config.inbox_buckets:
        bdir = config.vault / "inbox" / bucket
        if not bdir.exists():
            continue
        # Use count_files to exclude dotfiles (.gitkeep)
        num_items = count_files(bdir)
        if num_items == 0:
            continue

        items = [p for p in bdir.iterdir() if p.is_file() and p.name != "README.md" and not p.name.startswith('.')]
        items_info = []
        overdue = []
        now = datetime.now().timestamp()
        for it in items:
            age_days = (now - it.stat().st_mtime) / 86400
            entry = {"name": it.name, "age_days": f"{age_days:.1f}"}
            items_info.append(entry)
            if age_days > config.inbox_overdue_days:
                overdue.append(entry)
        info[bucket] = {"items": items_info, "overdue": overdue}
    if info:
        any_overdue = any(b["overdue"] for b in info.values())
        kind = "inbox_overdue" if any_overdue else "inbox_present"
        summary_parts = []
        for bucket, data in info.items():
            n_items = len(data["items"])
            n_over = len(data["overdue"])
            extra = f" ({n_over} overdue)" if n_over else ""
            summary_parts.append(f"{bucket}: {n_items}{extra}")
        issues.append({
            "kind": kind,
            "summary": "Inbox — " + ", ".join(summary_parts),
            "details": info,
        })
    return issues


def load_todos(todos_path: Path):
    """Load todos.md and parse task rows. Returns dict: task_id -> task_dict."""
    tasks = {}
    if not todos_path.exists():
        return tasks

    for line in todos_path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.lstrip()
        if not stripped.startswith("|"):
            continue
        if "----" in stripped or stripped.lower().startswith("| id |"):
            continue

        cells = [c.strip() for c in stripped.split("|")]
        if len(cells) < 6:
            continue

        # Expected format: | id | title | status | priority | milestone | depends-on |
        task_id = cells[1]
        if task_id and len(task_id) == 8:  # hash ID format
            depends_on = cells[5] if len(cells) > 5 else ""
            milestone = cells[4] if len(cells) > 4 else ""
            tasks[task_id] = {
                "id": task_id,
                "depends_on": depends_on,
                "milestone": milestone,
            }
    return tasks


def parse_roadmap_phases(roadmap_path: Path):
    """Extract phase information from roadmap.md.
    Returns dict: task_id -> phase_name (or milestone for now-next-later)
    """
    phases = {}
    if not roadmap_path.exists():
        return phases

    current_phase = None
    for line in roadmap_path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.lstrip()

        # Detect phase headers (##  or ### )
        m_phase = re.match(r"^##\s+(.+)$", stripped)
        if m_phase:
            current_phase = m_phase.group(1).strip()
            continue

        # Extract task IDs from task rows (assuming markdown links like [#ID](link))
        if current_phase:
            for m in re.finditer(r"\[#([a-f0-9]{8})\]", stripped):
                task_id = m.group(1)
                phases[task_id] = current_phase

    return phases


def check_cross_phase_dependency(config: ProjectConfig):
    """Detect NEW dependencies that cross phases.
    Requires git access to get previous version of todos.md.
    """
    if not config.cross_phase_config:
        return []  # check disabled

    issues = []
    todos_path = config.vault / "process/active/todos.md"
    if not todos_path.exists():
        return issues

    # Load current todos
    current_todos = load_todos(todos_path)

    # Try to load previous version via git
    try:
        result = subprocess.run(
            ["git", "-C", str(config.vault), "show", "HEAD~1:process/active/todos.md"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return issues  # no previous version

        previous_content = result.stdout
        # Parse previous todos by simulating load_todos on the string
        previous_todos = {}
        for line in previous_content.splitlines():
            stripped = line.lstrip()
            if not stripped.startswith("|"):
                continue
            if "----" in stripped or stripped.lower().startswith("| id |"):
                continue
            cells = [c.strip() for c in stripped.split("|")]
            if len(cells) < 6:
                continue
            task_id = cells[1]
            if task_id and len(task_id) == 8:
                depends_on = cells[5] if len(cells) > 5 else ""
                milestone = cells[4] if len(cells) > 4 else ""
                previous_todos[task_id] = {
                    "id": task_id,
                    "depends_on": depends_on,
                    "milestone": milestone,
                }
    except Exception:
        return issues  # can't get git history

    # Load phase map
    roadmap_path = config.vault / "process/active/roadmap.md"
    phases = parse_roadmap_phases(roadmap_path)

    # Find NEW cross-phase dependencies
    exceptions = config.cross_phase_config.get("exceptions", [])
    findings = []

    for task_id, task_info in current_todos.items():
        current_deps_str = task_info.get("depends_on", "")
        previous_deps_str = previous_todos.get(task_id, {}).get("depends_on", "") if task_id in previous_todos else ""

        # Parse dependency lists (assuming format: "ID,ID,ID")
        current_deps = set(d.strip() for d in current_deps_str.split(",") if d.strip())
        previous_deps = set(d.strip() for d in previous_deps_str.split(",") if d.strip())

        # Find new dependencies
        new_deps = current_deps - previous_deps
        for dep_task_id in new_deps:
            if task_id in exceptions or dep_task_id in exceptions:
                continue

            source_phase = phases.get(task_id, "unknown")
            target_phase = phases.get(dep_task_id, "unknown")

            if source_phase != target_phase:
                findings.append({
                    "task_id": task_id,
                    "source_phase": source_phase,
                    "target_phase": target_phase,
                    "target_task": dep_task_id,
                })

    if findings:
        issues.append({
            "kind": "cross_phase_dependency",
            "summary": f"{len(findings)} NEW cross-phase dependenc(y/ies) detected",
            "details": findings,
        })

    return issues


def check_workstream_status_staleness(config: ProjectConfig):
    """Check project_hub.md for status blocks with embedded timestamps.
    Flags blocks not updated beyond configured threshold.
    """
    if not config.workstream_status_config:
        return []  # check disabled

    issues = []
    hub_path = config.hub
    if not hub_path.exists():
        return issues

    threshold_days = config.workstream_status_config.get("threshold-days", 14)
    skip_blocks = config.workstream_status_config.get("skip-blocks", [])

    content = hub_path.read_text(encoding="utf-8", errors="replace")
    findings = []

    # Find all <!-- ROLE-STATUS-START/END --> blocks
    pattern = r"<!-- (\w+)-STATUS-START -->"
    for match in re.finditer(pattern, content):
        role = match.group(1)
        if role in skip_blocks:
            continue

        # Look for "Updated: YYYY-MM-DD" within the block
        block_start = match.start()
        block_end = content.find(f"<!-- {role}-STATUS-END -->", block_start)
        if block_end == -1:
            continue

        block_text = content[block_start:block_end]
        ts_match = re.search(r"Updated:\s*(\d{4}-\d{2}-\d{2})", block_text)

        if not ts_match:
            findings.append({
                "role": role,
                "issue": "no update timestamp found",
            })
            continue

        timestamp_str = ts_match.group(1)
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d").date()
        except ValueError:
            findings.append({
                "role": role,
                "issue": f"invalid timestamp format: {timestamp_str}",
            })
            continue

        days_stale = (date.today() - timestamp).days
        if days_stale > threshold_days:
            findings.append({
                "role": role,
                "days_stale": days_stale,
                "threshold": threshold_days,
                "last_updated": timestamp_str,
            })

    if findings:
        issues.append({
            "kind": "workstream_status_staleness",
            "summary": f"{len(findings)} status block(s) not updated beyond threshold",
            "details": findings,
        })

    return issues


# ════════════════════════════════════════════════════════════════════════════ reporting

def check_session_hygiene(config: ProjectConfig):
    """Session hygiene — "is anything hidden, stale, or stranded?"

    Runs on the normal drift schedule and is invoked by pm-close-session as its
    verification step. Every check here is file/git based, so it behaves
    identically in every runtime (information architecture spine, section 6d).

    NOT here, deliberately: the session-managed ("hidden") memory store. In some
    runtimes that store sits behind a tool only an agent can call, so no script
    can reach it — pm-close-session performs that check itself.
    """
    import json
    import subprocess

    # 2026-07-30 (task c3f80b6e): returning [] here made an unconfigured or
    # disabled hygiene block indistinguishable from a clean one. The
    # post-commit hook greps for "session hygiene" and prints nothing when it
    # finds nothing, so a config missing this block reported success forever.
    # Absence of configuration is now itself a finding.
    if not getattr(config, "session_hygiene_enabled", False):
        return [{
            "kind": "session_hygiene_unconfigured",
            "summary": "Session hygiene — NOT CONFIGURED for this project "
                       "(session_hygiene.enabled is false or the block is absent); "
                       "no hygiene checking is happening here",
            "details": {"config": str(config.config_path)},
        }]

    issues = []
    vault = config.vault

    def _git(*args):
        try:
            out = subprocess.run(
                ["git", "-C", str(vault)] + list(args),
                capture_output=True, text=True, timeout=30,
            )
            return out.stdout if out.returncode == 0 else None
        except Exception:
            return None

    # ---- 1. durable content sitting uncommitted ---------------------------
    cfg = config.sh_uncommitted
    if cfg.get("enabled", True):
        porcelain = _git("status", "--porcelain")
        if porcelain is None:
            issues.append({
                "kind": "session_hygiene_no_git",
                "summary": "Session hygiene — not a git repo (or git failed); "
                           "uncommitted-content check skipped",
                "details": {"vault": str(vault)},
            })
        else:
            watch = tuple(cfg.get("watch", []))
            ignore = tuple(cfg.get("ignore_untracked", []))
            flagged = []
            for line in porcelain.splitlines():
                if len(line) < 4:
                    continue
                status, rel = line[:2], line[3:].strip()
                if " -> " in rel:                 # rename: take the destination
                    rel = rel.split(" -> ", 1)[1]
                rel = rel.strip('"')
                if watch and not rel.startswith(watch):
                    continue
                if status.strip() == "??" and ignore and rel.startswith(ignore):
                    continue
                flagged.append({"path": rel, "status": status.strip() or "M"})
            if flagged:
                shown = ", ".join(f["path"] for f in flagged[:5])
                more = "..." if len(flagged) > 5 else ""
                issues.append({
                    "kind": "uncommitted_durable",
                    "summary": "Session hygiene — %d durable file(s) uncommitted: %s%s"
                               % (len(flagged), shown, more),
                    "details": {"files": flagged},
                })

    # ---- 2. activity-log entries that never landed ------------------------
    cfg = config.sh_log
    if cfg.get("enabled", True):
        log_path = vault / cfg.get("path", "process/Log.md")
        placeholder = cfg.get("placeholder", "uncommitted")
        if log_path.exists():
            stranded = []
            try:
                lines = log_path.read_text(encoding="utf-8").splitlines()
            except Exception:
                lines = []
            in_fence = False
            for i, line in enumerate(lines, 1):
                # Skip fenced code blocks: the log template documents its own
                # entry schema with a literal "commit: <hash | uncommitted>"
                # example, which is documentation, not a stranded entry.
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                if "commit:" in line and placeholder in line:
                    stranded.append({"line": i, "text": line.strip()[:120]})
            if stranded:
                issues.append({
                    "kind": "log_unlanded",
                    "summary": "Session hygiene — %d activity-log entr(ies) still marked '%s'"
                               % (len(stranded), placeholder),
                    "details": {"entries": stranded},
                })

    # ---- 3. autoMemoryDirectory must resolve inside the vault -------------
    cfg = config.sh_memory_path
    if cfg.get("enabled", True):
        settings_path = vault / cfg.get("settings_file", ".claude/settings.json")
        key = cfg.get("key", "autoMemoryDirectory")
        settings = None
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text(encoding="utf-8"))
            except Exception as exc:
                issues.append({
                    "kind": "memory_path_unreadable",
                    "summary": "Session hygiene — %s did not parse as JSON (%s)"
                               % (settings_path.name, exc),
                    "details": {"path": str(settings_path)},
                })
        if settings is not None and key in settings:
            configured = Path(os.path.expanduser(str(settings[key])))
            try:
                resolved = configured.resolve()
                inside = True
                try:
                    resolved.relative_to(vault.resolve())
                except ValueError:
                    inside = False
            except Exception:
                resolved, inside = configured, False
            if cfg.get("must_be_inside_vault", True) and not inside:
                issues.append({
                    "kind": "memory_path_drift",
                    "summary": "Session hygiene — %s points outside this vault; "
                               "memory writes are landing where you will not see them" % key,
                    "details": {"configured": str(resolved), "vault": str(vault)},
                })
            elif not resolved.exists():
                issues.append({
                    "kind": "memory_path_missing",
                    "summary": "Session hygiene — %s points at a path that does not exist" % key,
                    "details": {"configured": str(resolved)},
                })

    # ---- 4. plugin-managed marker blocks must balance ---------------------
    cfg = config.sh_markers
    if cfg.get("enabled", True):
        def _marker_re(literal):
            # Require the real HTML-comment opener, so prose documenting the
            # convention (deliberately written with <!== ... ==> so it is inert)
            # is not counted as a marker. Tolerate internal whitespace runs,
            # because markers are padded for alignment: "END   WRITING-COWORK".
            parts = [re.escape(w) for w in str(literal).split()]
            return re.compile(r"<!--\s*" + r"\s+".join(parts))

        pairs = (
            (cfg.get("begin", "BEGIN WRITING-COWORK MANAGED:"),
             cfg.get("end", "END WRITING-COWORK MANAGED:"), "MANAGED"),
            (cfg.get("project_begin", "BEGIN PROJECT-OWNED"),
             cfg.get("project_end", "END PROJECT-OWNED"), "PROJECT-OWNED"),
        )
        unbalanced = []
        for rel in cfg.get("files", []):
            fp = vault / rel
            if not fp.exists():
                continue
            try:
                text = fp.read_text(encoding="utf-8")
            except Exception:
                continue
            for begin, end, label in pairs:
                n_begin = len(_marker_re(begin).findall(text))
                n_end   = len(_marker_re(end).findall(text))
                if n_begin != n_end:
                    unbalanced.append({
                        "file": rel, "block": label,
                        "begin": n_begin, "end": n_end,
                    })
        if unbalanced:
            issues.append({
                "kind": "managed_markers_unbalanced",
                "summary": "Session hygiene — unbalanced ownership markers in %d block(s); "
                           "a sync would have to guess block boundaries" % len(unbalanced),
                "details": {"blocks": unbalanced},
            })

    return issues


def format_report(config: ProjectConfig, issues, generated_present, when):
    lines = [
        f"# Drift report — {config.name} — {when.isoformat(timespec='seconds')} "
        f"— drift_check v{DRIFT_CHECK_VERSION}",
        "",
    ]
    if not issues:
        lines.append("All checks clean.")
        lines.append("")
        if generated_present:
            lines.append(f"_Informational — {len(generated_present)} gitignored generated artifact(s) present in vault:_")
            for g in generated_present:
                lines.append(f"- `{g}`")
        return "\n".join(lines)

    for issue in issues:
        lines.append(f"## {issue['kind']} — {issue['summary']}")
        lines.append("")
        details = issue["details"]
        if isinstance(details, list):
            for d in details:
                if isinstance(d, str):
                    lines.append(f"- `{d}`")
                elif isinstance(d, dict):
                    lines.append("- " + ", ".join(f"**{k}**: `{v}`" for k, v in d.items()))
                else:
                    lines.append(f"- {d}")
        elif isinstance(details, dict):
            for k, v in details.items():
                lines.append(f"### {k}")
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        lines.append(f"- **{k2}**: {v2}")
                else:
                    lines.append(f"- {v}")
        lines.append("")

    if generated_present:
        lines.append("---")
        lines.append("")
        lines.append(f"_Informational — {len(generated_present)} gitignored generated artifact(s) present:_")
        for g in generated_present:
            lines.append(f"- `{g}`")

    return "\n".join(lines)


def report_filename(when) -> str:
    """Report filename with time-of-day, so same-day reruns don't collide.

    Format: YYYY-MM-DDTHHMM.md (e.g. 2026-07-22T1430.md). Fixed 2026-07-22
    (drift_check v0.2.0) — the prior YYYY-MM-DD.md format let two runs on
    the same day silently overwrite each other with no trace the earlier
    run happened, even though this report's own header already carries a
    full timestamp.
    """
    return when.strftime("%Y-%m-%dT%H%M") + ".md"


def attention_block(config: ProjectConfig, issues, when):
    ts = when.isoformat(timespec="seconds")
    if not issues:
        return f"_Drift check clean as of {ts}._"
    parts = [f"**Attention — drift detected ({ts})**", ""]
    for issue in issues:
        parts.append(f"- {issue['summary']}")
    parts.append("")
    reports_rel = config.reports_dir.relative_to(config.vault)
    parts.append(f"Details: `{reports_rel}/{report_filename(when)}`.")
    return "\n".join(parts)


def footer_block(config: ProjectConfig, issues, when):
    ts = when.isoformat(timespec="seconds")
    if not issues:
        return f"- Last drift check: **{ts}** — clean"
    reports_rel = config.reports_dir.relative_to(config.vault)
    return f"- Last drift check: **{ts}** — **DRIFT** — see `{reports_rel}/{report_filename(when)}`"


def replace_block(text, start_marker, end_marker, new_inner, fallback_section=None):
    pattern = re.compile(
        re.escape(start_marker) + r"(.*?)" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{start_marker}\n{new_inner}\n{end_marker}"
    new_text, n = pattern.subn(replacement, text, count=1)
    if n == 0 and fallback_section is not None:
        if not text.endswith("\n"):
            text += "\n"
        new_text = text + "\n" + fallback_section + "\n" + replacement + "\n"
    return new_text


def update_hub(config: ProjectConfig, issues, when, dry_run=False):
    if not config.hub.exists():
        return
    text = config.hub.read_text(encoding="utf-8")
    block = attention_block(config, issues, when)
    new = replace_block(
        text,
        config.markers["attention_start"],
        config.markers["attention_end"],
        block,
        fallback_section="\n---\n\n## Attention",
    )
    if new != text and not dry_run:
        config.hub.write_text(new, encoding="utf-8")


def update_ownership_footer(config: ProjectConfig, issues, when, dry_run=False):
    if not config.ownership_table.exists():
        return
    text = config.ownership_table.read_text(encoding="utf-8")
    block = footer_block(config, issues, when)
    new = replace_block(
        text,
        config.markers["footer_start"],
        config.markers["footer_end"],
        block,
        fallback_section="\n---\n\n## Drift-check footer",
    )
    if new != text and not dry_run:
        config.ownership_table.write_text(new, encoding="utf-8")


def write_flag(config: ProjectConfig, issues, dry_run=False):
    if dry_run:
        return
    if issues:
        config.drift_flag.parent.mkdir(parents=True, exist_ok=True)
        config.drift_flag.write_text(f"{datetime.now().isoformat(timespec='seconds')}\n", encoding="utf-8")
    else:
        if config.drift_flag.exists():
            config.drift_flag.unlink()


def write_report(config: ProjectConfig, issues, generated_present, when, dry_run=False):
    if dry_run:
        return None
    config.reports_dir.mkdir(parents=True, exist_ok=True)
    if not issues:
        return None
    path = config.reports_dir / report_filename(when)
    path.write_text(format_report(config, issues, generated_present, when), encoding="utf-8")
    return path


# ════════════════════════════════════════════════════════════════════════════ per-project run

def run_one(config: ProjectConfig, dry_run=False):
    """Run checks for one project. Returns (issues, generated_present, report_path, when)."""
    when = datetime.now()

    # Early-exit optimization: check if any changes since last run
    should_skip, skip_reason = should_skip_full_check(config.vault)
    if should_skip and skip_reason == "no_changes":
        # Don't run full checks, but still record the run time
        record_drift_run_time(config.vault, dry_run=dry_run)
        return [], [], None, when

    issues = []
    # First: say what cannot be checked at all. Everything below reports on
    # what it could read; this reports on what it could not.
    issues.extend(check_config_preflight(config))
    issues.extend(check_xrefs(config))
    issues.extend(check_build_freshness(config))
    issues.extend(check_inbox(config))
    inv_issues, generated_present = check_inventory(config)
    issues.extend(inv_issues)

    # v0.1.14 enhancements
    issues.extend(check_cross_phase_dependency(config))
    issues.extend(check_workstream_status_staleness(config))

    # 2026-07-27: session hygiene
    issues.extend(check_session_hygiene(config))

    update_hub(config, issues, when, dry_run=dry_run)
    update_ownership_footer(config, issues, when, dry_run=dry_run)
    write_flag(config, issues, dry_run=dry_run)
    report_path = write_report(config, issues, generated_present, when, dry_run=dry_run)

    # Record run time for next time
    record_drift_run_time(config.vault, dry_run=dry_run)

    return issues, generated_present, report_path, when


def print_one_summary(config: ProjectConfig, issues, report_path, when):
    print(f"[{when.isoformat(timespec='seconds')}] {config.name}: ", end="")
    if not issues:
        print("clean")
    else:
        print(f"{len(issues)} issue(s)")
        for issue in issues:
            print(f"  - {issue['summary']}")
        if report_path:
            print(f"  report: {report_path}")


# ════════════════════════════════════════════════════════════════════════════ registry

def load_registry(path: Path):
    if not path.exists():
        sys.stderr.write(f"ERROR: registry not found: {path}\n")
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("projects", [])


def resolve_project_config(name_or_none, registry_entries):
    """Given a name (or None for all), yield (entry, ProjectConfig) for matching enabled projects."""
    for entry in registry_entries:
        if not entry.get("enabled", True):
            continue
        if name_or_none and entry.get("name") != name_or_none:
            continue
        config_path = Path(os.path.expanduser(entry["config"]))
        try:
            config = ProjectConfig(config_path)
        except Exception as e:
            sys.stderr.write(f"ERROR loading {entry.get('name', '?')} ({config_path}): {e}\n")
            continue
        yield entry, config


# ════════════════════════════════════════════════════════════════════════════ main

def main():
    parser = argparse.ArgumentParser(description="Cowork drift check — multi-project.")
    parser.add_argument("--version", action="store_true",
                        help="Print this script's own version (independent of plugin version) and exit")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--config", help="Path to a single project's drift_check.yaml")
    group.add_argument("--all", action="store_true", help="Run all enabled projects in registry")
    group.add_argument("--project", help="Run named project from registry")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                        help=f"Registry path (default: {DEFAULT_REGISTRY})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Read everything but don't write outputs")
    args = parser.parse_args()

    if args.version:
        print(f"drift_check.py version {DRIFT_CHECK_VERSION}")
        return 0

    if not (args.config or args.all or args.project):
        parser.error("one of the arguments --config --all --project is required (or use --version)")

    # Single-config mode
    if args.config:
        try:
            config = ProjectConfig(Path(os.path.expanduser(args.config)))
        except Exception as e:
            sys.stderr.write(f"ERROR loading config {args.config}: {e}\n")
            return 2
        issues, generated, report, when = run_one(config, dry_run=args.dry_run)
        print_one_summary(config, issues, report, when)
        return 0

    # Registry-based modes (--all or --project)
    registry_path = Path(os.path.expanduser(args.registry))
    entries = load_registry(registry_path)
    name_filter = args.project  # None if --all

    aggregate = []
    any_failure = False
    for entry, config in resolve_project_config(name_filter, entries):
        try:
            issues, generated, report, when = run_one(config, dry_run=args.dry_run)
            aggregate.append((config, issues, report, when))
            print_one_summary(config, issues, report, when)
        except Exception as e:
            sys.stderr.write(f"ERROR running {entry.get('name', '?')}: {e}\n")
            any_failure = True

    # Aggregate summary
    if len(aggregate) > 1:
        total_projects = len(aggregate)
        clean = sum(1 for _, issues, _, _ in aggregate if not issues)
        drifted = total_projects - clean
        print()
        print(f"[summary] {clean} clean, {drifted} drifted, {total_projects} total")

    if name_filter and not aggregate:
        sys.stderr.write(f"ERROR: no enabled registry entry matched --project={name_filter}\n")
        return 2

    return 1 if any_failure else 0


if __name__ == "__main__":
    sys.exit(main())
