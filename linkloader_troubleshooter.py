"""
linkloader_troubleshooter.py — Emergency backup/restore/diagnostics tool

Usage:
    python linkloader_troubleshooter.py --backup     Save originals to .backup/
    python linkloader_troubleshooter.py --verify     Check file integrity
    python linkloader_troubleshooter.py --restore    Restore originals from .backup/
    python linkloader_troubleshooter.py --status     Show current file state
"""

import os
import sys
import shutil
import ast
import hashlib
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(CURRENT_DIR, ".backup")
PROTECTED_FILES = (
    ".gitignore",
    "connection.py",
    "Give_controls.py",
    "linkloader_main.py",
    "denel master.py",
    "config.py",
    "__init__.py",
    "platform_utils.py",
    "cleanup.py",
    "ASbootloader.asm",
    "linkloader_troubleshooter.py",  # backup tool itself
)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _file_hash(path: str) -> str:
    """Return SHA-256 hex digest of file contents."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except (OSError, IOError):
        return "ERROR"


def _backup_path(filepath: str) -> str:
    """Return the backup path for a given file."""
    return os.path.join(BACKUP_DIR, os.path.basename(filepath))


def _syntax_check(path: str) -> bool:
    """Check Python file for syntax errors."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print(f"  ✖ SYNTAX ERROR in {os.path.basename(path)}: {e}")
        return False
    except Exception as e:
        print(f"  ✖ READ ERROR {os.path.basename(path)}: {e}")
        return False


def _required_functions(path: str, funcs: list[str]) -> bool:
    """Check that required functions exist in a Python file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        defined = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        missing = [f for f in funcs if f not in defined]
        if missing:
            print(f"  ✖ MISSING functions in {os.path.basename(path)}: {missing}")
            return False
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# COMMANDS
# ---------------------------------------------------------------------------

def cmd_backup() -> bool:
    """Backup all protected files to .backup/ directory."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"[{_ts()}] [BACKUP] Starting...")
    count = 0
    for fname in PROTECTED_FILES:
        src = os.path.join(CURRENT_DIR, fname)
        if not os.path.isfile(src):
            print(f"  ⚠ SKIP (not found): {fname}")
            continue
        dst = _backup_path(fname)
        try:
            shutil.copy2(src, dst)
            print(f"  ✔ BACKED UP: {fname}")
            count += 1
        except (OSError, IOError) as e:
            print(f"  ✖ BACKUP FAILED: {fname} — {e}")
            return False
    print(f"[{_ts()}] [BACKUP] Complete — {count} file(s) saved to {BACKUP_DIR}")
    return True


def cmd_restore() -> bool:
    """Restore all protected files from .backup/ directory."""
    if not os.path.isdir(BACKUP_DIR):
        print(f"[{_ts()}] [RESTORE] ✖ No backup directory found at {BACKUP_DIR}")
        return False
    print(f"[{_ts()}] [RESTORE] Starting...")
    count = 0
    for fname in PROTECTED_FILES:
        src = _backup_path(fname)
        if not os.path.isfile(src):
            print(f"  ⚠ SKIP (no backup): {fname}")
            continue
        dst = os.path.join(CURRENT_DIR, fname)
        try:
            shutil.copy2(src, dst)
            print(f"  ✔ RESTORED: {fname}")
            count += 1
        except (OSError, IOError) as e:
            print(f"  ✖ RESTORE FAILED: {fname} — {e}")
            return False
    print(f"[{_ts()}] [RESTORE] Complete — {count} file(s) restored")
    return True


def cmd_verify() -> bool:
    """Check all protected files for integrity (syntax + required functions)."""
    print(f"[{_ts()}] [VERIFY] Checking file integrity...")
    all_ok = True

    required_funcs_map = {
        "linkloader_main.py": [
            "_write_token_mirror", "_verify_rdi_token",
            "_verify_bus_state", "_run_module", "run_boot_sequence",
        ],
        "connection.py": [
            "_induct_corridors", "_walk_and_partition",
            "_write_bus_state", "_write_manifest", "check_and_wire_system_bus",
        ],
        "Give_controls.py": [
            "_preflight", "_spawn", "release_authority",
        ],
        "denel master.py": [
            "engage_freeze_rail", "disengage_freeze_rail", "main",
            "run_aslll_program",
        ],
    }

    for fname in PROTECTED_FILES:
        path = os.path.join(CURRENT_DIR, fname)
        if not os.path.isfile(path):
            print(f"  ⚠ MISSING FILE: {fname}")
            all_ok = False
            continue

        syntax_ok = True
        # Check syntax
        if fname.endswith(".py"):
            syntax_ok = _syntax_check(path)
            if not syntax_ok:
                all_ok = False

            # Check required functions
            funcs = required_funcs_map.get(fname, [])
            if funcs:
                funcs_ok = _required_functions(path, funcs)
                if not funcs_ok:
                    all_ok = False

        # Show current hash
        h = _file_hash(path)
        print(f"  {'✔' if syntax_ok else '✖'} {fname}  [{h}]")

    if all_ok:
        print(f"[{_ts()}] [VERIFY] ✅ All checks passed — system intact")
    else:
        print(f"[{_ts()}] [VERIFY] ❌ Issues found — run --restore to revert")
    return all_ok


def cmd_status() -> bool:
    """Show current state vs backup state for all files."""
    print(f"[{_ts()}] [STATUS] File state report:")
    for fname in PROTECTED_FILES:
        current = os.path.join(CURRENT_DIR, fname)
        backup = _backup_path(fname)

        cur_h = _file_hash(current) if os.path.isfile(current) else "---"
        bak_h = _file_hash(backup) if os.path.isfile(backup) else "---"

        if cur_h == "---" and bak_h == "---":
            status = "ABSENT"
        elif cur_h == bak_h:
            status = "ORIGINAL"
        elif bak_h == "---":
            status = "NEW (no backup)"
        else:
            status = "MODIFIED"

        print(f"  {status:15s}  {fname:30s}  cur={cur_h}  bak={bak_h}")
    return True


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> bool:
    if len(sys.argv) < 2:
        print(__doc__)
        return True

    command = sys.argv[1]
    commands = {
        "--backup": cmd_backup,
        "--restore": cmd_restore,
        "--verify": cmd_verify,
        "--status": cmd_status,
    }

    handler = commands.get(command)
    if handler is None:
        print(f"Unknown command: {command}")
        print(__doc__)
        return False

    return handler()


if __name__ == "__main__":
    sys.exit(0 if main() else 1)