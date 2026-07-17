#   ROLE
#   ----
#   Pure Software Control Layer. Manages the 0% CPU Freeze Rail and GUI
#   canvas state machine. Auto-detects host OS and applies the correct
#   freeze strategy for each platform.
#
#   FREEZE RAIL STRATEGY (auto-detected at runtime)
#   ------------------------------------------------
#   POSIX → signal.SIGSTOP sent to target processes (production)
#   Windows → NtSuspendProcess via ctypes (dev mode on Windows 10)
#
#   ASLLL SYNTAX (LOCKED — DO NOT MODIFY THE PARSER)
#   -------------------------------------------------
#   Pattern: :STP-{num}..{command}..!
#
#   TO ADD YOUR OWN COMMANDS:
#       1. Write a function below that returns True/False.
#       2. Register it in COMMAND_REGISTRY / COMMAND_REGISTRY_BY_BODY.
#
# ==============================================================================

import os
import sys
import re
import signal
import platform
import subprocess
import ctypes
import time
import logging
from typing import Any, Optional

from config import (
    DAEMON_PLACEHOLDER,
    POSIX_FREEZE_TARGETS,
    WINDOWS_FREEZE_TARGETS,
    KERNEL_CONNECTION_MARKER,
)
from platform_utils import (
    posix_find_pids_by_name,
    posix_freeze_target,
    posix_thaw_target,
    windows_find_pids,
    windows_suspend_process,
    windows_resume_process,
)

# ---------------------------------------------------------------------------
# Backward-compatible aliases
# ---------------------------------------------------------------------------
_linux_find_pids = posix_find_pids_by_name
_linux_freeze_target = posix_freeze_target
_linux_thaw_target = posix_thaw_target

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logger = logging.getLogger("denel_master")


# ---------------------------------------------------------------------------
#  PLATFORM DETECTION
# ---------------------------------------------------------------------------
_HOST_OS: str = platform.system()
_IS_POSIX: bool = _HOST_OS in ("Linux", "Darwin", "FreeBSD", "OpenBSD")
_IS_WINDOWS: bool = _HOST_OS == "Windows"

# Kernel connection marker
_kernel_conn = KERNEL_CONNECTION_MARKER

# ---------------------------------------------------------------------------
#  FREEZE RAIL TARGETS
# ---------------------------------------------------------------------------
# POSIX targets — uses SIGSTOP (works on Linux, macOS, BSD)
POSIX_TARGETS: tuple[str, ...] = POSIX_FREEZE_TARGETS

# Windows targets (development — background services safe to suspend briefly)
# These are non-critical services that bloat CPU. We suspend, not kill.
WINDOWS_TARGETS: tuple[str, ...] = WINDOWS_FREEZE_TARGETS

# ---------------------------------------------------------------------------
#  CANVAS STATE MACHINE
# ---------------------------------------------------------------------------
# States: VISIBLE, HIDDEN, MINIMIZED, FROZEN
_canvas_state: str = "VISIBLE"


def _set_canvas_state(new_state: str) -> None:
    """Set the canvas display state."""
    global _canvas_state
    _canvas_state = new_state
    logger.info(f"Canvas state → {new_state}")


# ---------------------------------------------------------------------------
#  POSIX FREEZE RAIL — SIGSTOP / SIGCONT via signal
# ---------------------------------------------------------------------------

def engage_freeze_rail() -> bool:
    """
    Engage the 0% CPU freeze rail.

    On POSIX  → SIGSTOP to target processes (production)
    On Windows → NtSuspendProcess on background service targets (dev mode)

    Returns:
        True if all targets were frozen successfully.
    """
    logger.info(f"Engaging freeze rail on {_HOST_OS}...")
    _set_canvas_state("FROZEN")
    all_ok = True

    if _IS_POSIX:
        for target in POSIX_TARGETS:
            try:
                ok = posix_freeze_target(target)
                all_ok = all_ok and ok
            except PermissionError:
                logger.critical(f"Permission denied freezing {target}")
                all_ok = False
            except OSError as exc:
                logger.critical(f"OS error freezing {target}: {exc}")
                all_ok = False

    elif _IS_WINDOWS:
        for exe in WINDOWS_TARGETS:
            try:
                pids = windows_find_pids(exe)
                if not pids:
                    logger.info(f"'{exe}' not running — skipped.")
                    continue
                for pid in pids:
                    ok = windows_suspend_process(pid)
                    all_ok = all_ok and ok
            except (OSError, subprocess.TimeoutExpired) as exc:
                logger.critical(f"Windows freeze error for {exe}: {exc}")
                all_ok = False
    else:
        logger.critical(f"Host OS '{_HOST_OS}' — freeze rail not implemented.")
        all_ok = False

    return all_ok


def disengage_freeze_rail() -> bool:
    """
    Release the freeze rail — resume all suspended processes.

    Returns:
        True if all targets were resumed successfully.
    """
    logger.info(f"Disengaging freeze rail on {_HOST_OS}...")
    _set_canvas_state("VISIBLE")
    all_ok = True

    if _IS_POSIX:
        for target in POSIX_TARGETS:
            try:
                ok = posix_thaw_target(target)
                all_ok = all_ok and ok
            except OSError as exc:
                logger.critical(f"OS error thawing {target}: {exc}")
                all_ok = False

    elif _IS_WINDOWS:
        for exe in WINDOWS_TARGETS:
            try:
                pids = windows_find_pids(exe)
                for pid in pids:
                    ok = windows_resume_process(pid)
                    all_ok = all_ok and ok
            except (OSError, subprocess.TimeoutExpired) as exc:
                logger.critical(f"Windows thaw error for {exe}: {exc}")
                all_ok = False
    else:
        logger.critical(f"Host OS '{_HOST_OS}' — thaw not implemented.")
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
#  ASLLL PARSER — STRUCTURE IS PERMANENTLY LOCKED
# ---------------------------------------------------------------------------

_ASLLL_PATTERN = re.compile(r"^:STP-(\d+)\.\.(.+?)\.\.\!$")


def _parse_aslll(command_str: str) -> tuple[bool, int, str]:
    """
    Parse a single ASLLL command string. LOCKED — do not modify.

    Args:
        command_str: Raw ASLLL command string.

    Returns:
        Tuple of (is_valid, step_number, command_body).
    """
    s = command_str.strip()
    if not (s.startswith(":STP-") and s.endswith("..!")):
        return False, -1, ""
    match = _ASLLL_PATTERN.match(s)
    if not match:
        return False, -1, ""
    return True, int(match.group(1)), match.group(2).strip()


def _dispatch_command(step_num: int, command_body: str) -> bool:
    """
    Dispatch a parsed ASLLL command to its registered handler. LOCKED.

    Args:
        step_num: Command step number.
        command_body: Command body string.

    Returns:
        True if command executed successfully.
    """
    canonical_key = f":STP-{step_num}..{command_body}..!"
    handler = COMMAND_REGISTRY.get(canonical_key)
    if handler is None:
        handler = COMMAND_REGISTRY_BY_BODY.get(command_body.lower())
    if handler is None:
        logger.warning(f"No handler for: {canonical_key}")
        return False
    try:
        return bool(handler())
    except Exception as exc:
        logger.critical(f"Handler for '{canonical_key}' raised: {exc}")
        return False


def run_aslll_program(commands: list[str]) -> dict:
    """
    Execute a list of ASLLL commands in sequence. LOCKED — do not modify.

    Args:
        commands: List of raw ASLLL command strings.

    Returns:
        Dict mapping command → True/False/None result.
    """
    results = {}
    logger.info(f"Running {len(commands)} command(s)...")
    for raw in commands:
        valid, step_num, body = _parse_aslll(raw)
        if not valid:
            logger.warning(f"Rejected invalid command: '{raw}'")
            results[raw] = None
            continue
        logger.info(f"Step {step_num}: '{body}'")
        ok = _dispatch_command(step_num, body)
        results[raw] = ok
        logger.info(f"Step {step_num} → {'OK' if ok else 'FAIL'}")
    return results


# ---------------------------------------------------------------------------
#  ===========================================================================
#  COMMAND REGISTRY — THIS IS THE ONLY SECTION USERS SHOULD EDIT
#  ===========================================================================
#
#  HOW TO ADD YOUR OWN COMMAND:
#  ----------------------------
#  1. Write a function below that performs the real action.
#     It must return True on success, False on failure.
#  2. Add to COMMAND_REGISTRY:  ":STP-N..your command..!" : your_function
#  3. Add to COMMAND_REGISTRY_BY_BODY: "your command" : your_function
#
# ---------------------------------------------------------------------------

# ── BUILT-IN SOFTWARE COMMAND HANDLERS ──────────────────────────────────────

def _cmd_freeze_background() -> bool:
    """Engage the 0% CPU freeze rail on background services."""
    return engage_freeze_rail()


def _cmd_thaw_background() -> bool:
    """Disengage the freeze rail and resume background services."""
    return disengage_freeze_rail()


def _cmd_hide_canvas() -> bool:
    """Transition canvas to HIDDEN state and engage freeze rail."""
    _set_canvas_state("HIDDEN")
    return engage_freeze_rail()


def _cmd_show_canvas() -> bool:
    """Transition canvas to VISIBLE state and disengage freeze rail."""
    return disengage_freeze_rail()


def _cmd_minimize_canvas() -> bool:
    """Transition canvas to MINIMIZED state and engage freeze rail."""
    _set_canvas_state("MINIMIZED")
    return engage_freeze_rail()


def _cmd_report_platform() -> bool:
    """Print full platform/OS report."""
    print(f"    OS       : {_HOST_OS}")
    print(f"    Release  : {platform.release()}")
    print(f"    Version  : {platform.version()}")
    print(f"    Machine  : {platform.machine()}")
    print(f"    Canvas   : {_canvas_state}")
    return True


# ── REGISTER BUILT-IN COMMANDS ───────────────────────────────────────────────

COMMAND_REGISTRY: dict = {
    ":STP-1..freeze background..!":   _cmd_freeze_background,
    ":STP-2..thaw background..!":     _cmd_thaw_background,
    ":STP-3..hide canvas..!":         _cmd_hide_canvas,
    ":STP-4..show canvas..!":         _cmd_show_canvas,
    ":STP-5..minimize canvas..!":     _cmd_minimize_canvas,
    ":STP-6..report platform..!":     _cmd_report_platform,
    # ── ADD YOUR COMMANDS HERE ──────────────────────────────────────────────
    # ":STP-7..your command here..!": your_function,
}

COMMAND_REGISTRY_BY_BODY: dict = {
    "freeze background": _cmd_freeze_background,
    "thaw background":   _cmd_thaw_background,
    "hide canvas":       _cmd_hide_canvas,
    "show canvas":       _cmd_show_canvas,
    "minimize canvas":   _cmd_minimize_canvas,
    "report platform":   _cmd_report_platform,
}

# ===========================================================================
#  END OF USER-EDITABLE SECTION
# ===========================================================================


# ---------------------------------------------------------------------------
#  MAIN ENTRY POINT
# ---------------------------------------------------------------------------

def main() -> bool:
    """Main entry point for the DENEL software master."""
    try:
        separator = "=" * 66
        print(separator)
        print("  firstAS v0.1 — DENEL SOFTWARE MASTER ONLINE")
        print(f"  Host OS: {_HOST_OS} | Freeze Rail: {'SIGSTOP' if _IS_POSIX else 'NtSuspendProcess'}")
        print(separator)

        # Run boot-time ASLLL software program
        boot_commands = [
            ":STP-6..report platform..!",
        ]

        results = run_aslll_program(boot_commands)

        passed  = sum(1 for v in results.values() if v is True)
        failed  = sum(1 for v in results.values() if v is False)
        invalid = sum(1 for v in results.values() if v is None)

        print(f"\n  [DENEL] Boot ASLLL program complete:")
        print(f"          Passed  : {passed}")
        print(f"          Failed  : {failed}")
        print(f"          Invalid : {invalid}")
        print(separator)
        print("  [DENEL] Software master plane ACTIVE.")
        print(f"  [DENEL] Freeze rail ARMED — will engage on canvas HIDE/MINIMIZE.")
        print(separator)
        return True

    except Exception as exc:
        logger.critical(f"Fatal fault: {exc}")
        return False


if __name__ == "__main__":
    # Simple test harness
    success = main()
    print(f"\n[DENEL] Exit status: {'OK' if success else 'FAIL'}")
    sys.exit(0 if success else 1)