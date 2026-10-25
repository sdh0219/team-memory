#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Archive the oldest entries of .memory/LOG.md into LOG-archive.md.

Usage:
    python archive_log.py [--keep N] [path]

PATH is resolved the same way as validate_memory.py: if PATH/STATE.md exists,
PATH itself is the .memory directory, otherwise PATH/.memory is used.

LOG.md holds a "# " title followed by "## " entries (newest first).  When it
contains more than --keep entries (default 100), the oldest surplus entries
are moved into LOG-archive.md next to LOG.md:

  - LOG-archive.md does not exist  ->  created with the title
    "# 操作日志（归档）" followed by the moved entries
  - LOG-archive.md exists          ->  the moved entries are inserted right
    below its title line, so the archive also reads newest-first

Before anything is written, the script re-parses the rendered files in memory
and verifies that no entry is lost (entry count conserved across both files);
on mismatch it aborts without writing.

Exit code: 0 on success (including "nothing to archive"), 1 on failure,
2 on usage errors.
"""

import argparse
import sys
from pathlib import Path

DEFAULT_KEEP = 100
ARCHIVE_TITLE = "# 操作日志（归档）"


def _plural(n, singular, plural):
    return "%d %s" % (n, singular if n == 1 else plural)


def resolve_memory_dir(arg):
    """Resolve the .memory directory from the optional CLI path argument."""
    base = Path(arg) if arg else Path(".memory")
    if (base / "STATE.md").is_file():
        return base
    return base / ".memory"


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
            return fh.read().lstrip("\ufeff")
    except OSError:
        return None


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def split_entries(lines):
    """Split lines at "## " headings into entry blocks.

    Each block runs from its heading line to the line before the next
    heading; trailing blank separator lines are trimmed.
    """
    starts = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    blocks = []
    for k, start in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        block = list(lines[start:end])
        while block and not block[-1].strip():
            block.pop()
        blocks.append(block)
    return blocks


def parse_log(text):
    """Return (preamble_text, entry_texts); the preamble keeps the "# " title."""
    lines = text.splitlines()
    first = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), None)
    if first is None:
        preamble = list(lines)
        while preamble and not preamble[-1].strip():
            preamble.pop()
        return "\n".join(preamble), []
    preamble = list(lines[:first])
    while preamble and not preamble[-1].strip():
        preamble.pop()
    entries = ["\n".join(block) for block in split_entries(lines)]
    return "\n".join(preamble), entries


def count_entries(text):
    return len(parse_log(text)[1])


def render_log(preamble, entries):
    """Render LOG.md: preamble (title), then entries separated by one blank line."""
    parts = [p for p in [preamble] + list(entries) if p and p.strip()]
    return "\n\n".join(parts) + "\n" if parts else ""


def render_archive(existing_text, new_entries):
    """Render LOG-archive.md with new_entries inserted right below the title."""
    if existing_text is None or not existing_text.strip():
        head, rest = ARCHIVE_TITLE, ""
    else:
        lines = existing_text.splitlines()
        t = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), 0)
        head = "\n".join(lines[: t + 1])
        rest = "\n".join(lines[t + 1 :]).strip("\n")
    parts = list(new_entries) + ([rest] if rest else [])
    if not parts:
        return head + "\n"
    return head + "\n\n" + "\n\n".join(parts) + "\n"


def _use_utf8_console():
    """Make Chinese titles print correctly on Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _use_utf8_console()
    parser = argparse.ArgumentParser(
        description="Move the oldest entries of .memory/LOG.md into LOG-archive.md."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="project root or .memory directory (default: .memory)",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=DEFAULT_KEEP,
        metavar="N",
        help="number of newest entries kept in LOG.md (default: %d)" % DEFAULT_KEEP,
    )
    args = parser.parse_args(argv)

    if args.keep < 0:
        print("ERROR: --keep must be >= 0", file=sys.stderr)
        return 2
    if args.path:
        given = Path(args.path)
        if given.exists() and not given.is_dir():
            print("ERROR: %s is not a directory" % given, file=sys.stderr)
            return 2

    memory_dir = resolve_memory_dir(args.path)
    log_path = memory_dir / "LOG.md"
    log_text = read_text(log_path)
    if log_text is None:
        print("ERROR: LOG.md not found at %s" % log_path, file=sys.stderr)
        return 1

    preamble, entries = parse_log(log_text)
    if len(entries) <= args.keep:
        print("Nothing to archive (%d entries, keep=%d)" % (len(entries), args.keep))
        return 0

    kept = entries[: args.keep]
    moved = entries[args.keep :]

    archive_path = memory_dir / "LOG-archive.md"
    archive_text = read_text(archive_path)
    archive_before = count_entries(archive_text) if archive_text is not None else 0

    new_log_text = render_log(preamble, kept)
    new_archive_text = render_archive(archive_text, moved)

    # Zero-loss self check: re-parse the rendered files before writing anything.
    log_after = count_entries(new_log_text)
    archive_after = count_entries(new_archive_text)
    if not (
        log_after == len(kept)
        and archive_after == archive_before + len(moved)
        and len(entries) + archive_before == log_after + archive_after
    ):
        print(
            "ERROR: self-check failed, nothing was written "
            "(before: %s in LOG.md + %s in archive; after: %s + %s)"
            % (
                _plural(len(entries), "entry", "entries"),
                _plural(archive_before, "entry", "entries"),
                _plural(log_after, "entry", "entries"),
                _plural(archive_after, "entry", "entries"),
            ),
            file=sys.stderr,
        )
        return 1

    try:
        # Archive first: if the second write fails, the moved entries already
        # exist in the archive, so nothing is lost.
        write_text(archive_path, new_archive_text)
        write_text(log_path, new_log_text)
    except OSError as exc:
        print("ERROR: failed to write files: %s" % exc, file=sys.stderr)
        return 1

    print(
        "Archived %s from LOG.md to %s (%s kept in LOG.md, %s now in archive)"
        % (
            _plural(len(moved), "oldest entry", "oldest entries"),
            archive_path,
            _plural(len(kept), "entry", "entries"),
            _plural(archive_after, "entry", "entries"),
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
