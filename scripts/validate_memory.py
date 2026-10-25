#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate team-memory protocol files (.memory/STATE.md, .memory/LOG.md).

Usage:
    python validate_memory.py [path]

PATH may be a project root containing a .memory/ directory, the .memory
directory itself, or omitted (defaults to ".memory").  Resolution rule: if
PATH/STATE.md exists, PATH itself is treated as the .memory directory,
otherwise PATH/.memory is used.

Rules (see docs/protocol.md):

STATE.md
  - must exist
  - whole file <= 50 lines
  - must contain the four required sections, by their Chinese or English
    names (case-insensitive):
        ## 正在做    / ## Doing
        ## 下一步    / ## Next steps
        ## 近期完成  / ## Recently done
        ## 坑与约定  / ## Pitfalls
  - the file header must contain "最后更新" or "Last updated"

LOG.md
  - must exist
  - every entry (from one "## " heading to the next, heading line and body
    included) must be <= 10 lines
  - entry headings must match "## YYYY-MM-DD HH:mm · <name>"
  - entry dates must be non-increasing from top to bottom (warning only)

Both files
  - secret-leak heuristics; every hit is a warning

Output: one "[error]" or "[warn]" line per finding, then a summary line.
Exit code: 0 when no error is found, 1 when at least one error is found.
"""

import argparse
import re
import sys
from pathlib import Path

STATE_LINE_LIMIT = 50
ENTRY_LINE_LIMIT = 10
HEADER_SCAN_LINES = 10

# (canonical Chinese name, English alias)
REQUIRED_SECTIONS = [
    ("正在做", "Doing"),
    ("下一步", "Next steps"),
    ("近期完成", "Recently done"),
    ("坑与约定", "Pitfalls"),
]

ENTRY_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) · (\S.*)$")

SECRET_PATTERNS = [
    ("sk-style API key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("GitHub token", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "credential assignment",
        re.compile(r"(?i)(password|passwd|token|secret|api[_-]?key)\s*[:=]\s*\S{8,}"),
    ),
]


class Report(object):
    """Collects and prints findings, keeping the error/warning counters."""

    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def error(self, message):
        self.errors += 1
        print("[error] " + message)

    def warn(self, message):
        self.warnings += 1
        print("[warn] " + message)

    def is_clean(self):
        return self.errors == 0 and self.warnings == 0


def resolve_memory_dir(arg):
    """Resolve the .memory directory from the optional CLI path argument."""
    base = Path(arg) if arg else Path(".memory")
    if (base / "STATE.md").is_file():
        return base
    return base / ".memory"


def read_text(path):
    """Read a UTF-8 text file; return (text, error_message)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
            return fh.read().lstrip("\ufeff"), None
    except OSError as exc:
        return None, str(exc)


def check_state(memory_dir, report):
    path = memory_dir / "STATE.md"
    text, _err = read_text(path)
    if text is None:
        report.error("STATE.md: missing (expected at %s)" % path)
        return
    lines = text.splitlines()

    # Rule: whole file <= 50 lines.
    if len(lines) > STATE_LINE_LIMIT:
        report.error(
            "STATE.md: file has %d lines (limit %d)" % (len(lines), STATE_LINE_LIMIT)
        )

    # Rule: the four required sections must be present (Chinese or English).
    headings = [
        ln.strip()[3:].strip().casefold()
        for ln in lines
        if ln.strip().startswith("## ")
    ]
    for cn_name, en_name in REQUIRED_SECTIONS:
        aliases = (cn_name.casefold(), en_name.casefold())
        if not any(h.startswith(a) for h in headings for a in aliases):
            report.error(
                "STATE.md: missing required section '## %s' (or '## %s')"
                % (cn_name, en_name)
            )

    # Rule: header must state when the file was last updated.
    head = "\n".join(lines[:HEADER_SCAN_LINES])
    if "最后更新" not in head and "last updated" not in head.casefold():
        report.error(
            "STATE.md: header must contain '最后更新' or 'Last updated' "
            "(checked first %d lines)" % HEADER_SCAN_LINES
        )

    check_secrets("STATE.md", text, report)


def check_log(memory_dir, report):
    path = memory_dir / "LOG.md"
    text, _err = read_text(path)
    if text is None:
        report.error("LOG.md: missing (expected at %s)" % path)
        return
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("## ")]

    prev_stamp = None
    for k, start in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        size = end - start

        # Rule: each entry (heading line .. line before the next heading) <= 10 lines.
        if size > ENTRY_LINE_LIMIT:
            report.error(
                "LOG.md: entry starting at line %d is %d lines (limit %d)"
                % (start + 1, size, ENTRY_LINE_LIMIT)
            )

        # Rule: heading must match "## YYYY-MM-DD HH:mm · <name>".
        m = ENTRY_HEADING_RE.match(lines[start])
        if not m:
            report.error(
                "LOG.md: line %d: entry heading must match "
                "'## YYYY-MM-DD HH:mm · <name>'" % (start + 1)
            )
            continue

        # Rule (warning only): dates must be non-increasing from top to bottom.
        stamp = "%s %s" % (m.group(1), m.group(2))
        if prev_stamp is not None and stamp > prev_stamp:
            report.warn(
                "LOG.md: line %d: entry date %s is newer than the entry above "
                "(%s); LOG should be newest-first" % (start + 1, stamp, prev_stamp)
            )
        prev_stamp = stamp

    check_secrets("LOG.md", text, report)


def check_secrets(label, text, report):
    """Heuristic secret scan; one warning per affected line."""
    for lineno, line in enumerate(text.splitlines(), 1):
        hits = [name for name, pattern in SECRET_PATTERNS if pattern.search(line)]
        if hits:
            report.warn(
                "%s: line %d: possible secret leak (%s)"
                % (label, lineno, ", ".join(hits))
            )


def _use_utf8_console():
    """Make Chinese section names print correctly on Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _use_utf8_console()
    parser = argparse.ArgumentParser(
        description="Validate team-memory protocol files (.memory/STATE.md, .memory/LOG.md)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="project root or .memory directory (default: .memory)",
    )
    args = parser.parse_args(argv)

    if args.path:
        given = Path(args.path)
        if given.exists() and not given.is_dir():
            print("ERROR: %s is not a directory" % given, file=sys.stderr)
            return 2

    memory_dir = resolve_memory_dir(args.path)
    report = Report()
    check_state(memory_dir, report)
    check_log(memory_dir, report)

    if report.is_clean():
        print("All checks passed")
        return 0
    print(
        "%d error%s, %d warning%s"
        % (
            report.errors,
            "" if report.errors == 1 else "s",
            report.warnings,
            "" if report.warnings == 1 else "s",
        )
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
