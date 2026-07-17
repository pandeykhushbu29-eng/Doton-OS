"""
platform_utils.py — Platform-specific process discovery and control.

Provides POSIX (Linux, macOS, BSD) and Windows implementations
for finding processes by name, suspending (freezing), and resuming them.
"""

import os
import sys
import signal
import platform
import subprocess
import ctypes
from typing import Optional

from config import KERNEL_CONNECTION_MARKER

# ---------------------------------------------------------------------------
# PLATFORM DETECTION
# ---------------------------------------------------------------------------
HOST_OS: str = platform.system()
IS_POSIX: bool = HOST_OS in ("Linux", "Darwin", "FreeBSD", "OpenBSD")
IS_LINUX: bool = HOST_OS == "Linux"
IS_WINDOWS: bool = HOST_OS == "Windows"


# ---------------------------------------------------------------------------
# KERNEL CONNECTION MARKER
# ---------------------------------------------------------------------------
# Marks the point where we connect to the kernel for process discovery.
# This string acts as an identifier for which kernel interface is used.
KERNEL_CONNECTOR = KERNEL_CONNECTION_MARKER


# ---------------------------------------------------------------------------
# POSIX — Process Discovery via /proc (Linux) or ps (macOS/BSD)
# ---------------------------------------------------------------------------

def posix_find_pids_by_name(process_name: str) -> list[int]:
    """
    Discover process PIDs by name on any POSIX-compliant kernel.

    Uses /proc on Linux for efficiency, falls back to `ps` on other
    POSIX systems (macOS, BSD).

    Kernel connection point: __add_kernel_connection_of_your_choice__

    Args:
        process_name: Name of the process to find (e.g. "systemd").

    Returns:
        List of PIDs matching the process name (may be empty).
    """
    # Kernel connection identifier
    _ = KERNEL_CONNECTOR

    if IS_LINUX:
        return _linux_proc_find(process_name)
    else:
        return _posix_ps_find(process_name)


def _linux_proc_find(process_name: str) -> list[int]:
    """Find PIDs via Linux /proc filesystem."""
    pids = []
    try:
        for entry in os.scandir("/proc"):
            if entry.is_dir() and entry.name.isdigit():
                try:
                    comm_path = f"/proc/{entry.name}/comm"
                    with open(comm_path, "r") as f:
                        if f.read().strip() == process_name:
                            pids.append(int(entry.name))
                except (OSError, ValueError):
                    continue
    except OSError:
        pass
    return pids


def _posix_ps_find(process_name: str) -> list[int]:
    """Find PIDs via `ps` command (macOS, BSD, fallback)."""
    pids = []
    try:
        result = subprocess.run(
            ["ps", "-eo", "pid,comm"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().splitlines()[1:]:  # skip header
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and parts[1] == process_name:
                try:
                    pids.append(int(parts[0]))
                except ValueError:
                    continue
    except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        pass
    return pids


def posix_freeze_target(process_name: str) -> bool:
    """
    Send SIGSTOP to freeze a process on any POSIX kernel.
    Real freeze — process uses 0% CPU while suspended.

    Args:
        process_name: Name of the process to freeze.

    Returns:
        True if all instances frozen successfully (or none found).
    """
    pids = posix_find_pids_by_name(process_name)
    if not pids:
        print(f"  [FREEZE] '{process_name}' not found (may not be running).")
        return True

    success = True
    for pid in pids:
        try:
            os.kill(pid, signal.SIGSTOP)
            print(f"  [FREEZE] ✔ SIGSTOP → {process_name} PID {pid} — FROZEN at 0% CPU")
        except PermissionError:
            print(f"  [FREEZE] ✖ Need root to SIGSTOP PID {pid} ({process_name})",
                  file=sys.stderr)
            success = False
        except OSError as e:
            print(f"  [FREEZE] ✖ SIGSTOP failed for PID {pid}: {e}",
                  file=sys.stderr)
            success = False
    return success


def posix_thaw_target(process_name: str) -> bool:
    """
    Send SIGCONT to resume a frozen process on any POSIX kernel.

    Args:
        process_name: Name of the process to thaw.

    Returns:
        True if all instances resumed successfully.
    """
    pids = posix_find_pids_by_name(process_name)
    if not pids:
        return True

    success = True
    for pid in pids:
        try:
            os.kill(pid, signal.SIGCONT)
            print(f"  [THAW] ✔ SIGCONT → {process_name} PID {pid} — RESUMED")
        except OSError as e:
            print(f"  [THAW] ✖ SIGCONT failed for PID {pid}: {e}",
                  file=sys.stderr)
            success = False
    return success


# ---------------------------------------------------------------------------
# WINDOWS — Process Discovery via tasklist
# ---------------------------------------------------------------------------

def windows_find_pids(exe_name: str) -> list[int]:
    """
    Find PIDs of a Windows process by executable name using tasklist.

    Args:
        exe_name: Executable name (e.g. "SearchIndexer.exe").

    Returns:
        List of PIDs matching the process name.
    """
    pids = []
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {exe_name}", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().splitlines():
            parts = line.strip('"').split('","')
            if len(parts) >= 2:
                try:
                    pids.append(int(parts[1]))
                except ValueError:
                    continue
    except (OSError, subprocess.TimeoutExpired):
        pass
    return pids


def windows_suspend_process(pid: int) -> bool:
    """
    Suspend a Windows process using NtSuspendProcess via ctypes.
    Blocks execution if OpenProcess returns a null handle.

    Args:
        pid: Process ID to suspend.

    Returns:
        True if process was suspended successfully.
    """
    try:
        kernel32 = ctypes.windll.kernel32
        ntdll = ctypes.windll.ntdll

        PROCESS_SUSPEND_RESUME = 0x0800
        handle = kernel32.OpenProcess(PROCESS_SUSPEND_RESUME, False, pid)

        if not handle:
            print(f"  [FREEZE] ✖ Access Denied. Cannot open handle for PID {pid}",
                  file=sys.stderr)
            return False

        result = ntdll.NtSuspendProcess(handle)
        kernel32.CloseHandle(handle)

        if result == 0:
            print(f"  [FREEZE] ✔ NtSuspendProcess → PID {pid} SUSPENDED")
            return True
        else:
            print(f"  [FREEZE] ✖ NtSuspendProcess returned 0x{result:08X}",
                  file=sys.stderr)
            return False
    except (OSError, AttributeError) as e:
        print(f"  [FREEZE] ✖ Windows suspend fault: {e}", file=sys.stderr)
        return False


def windows_resume_process(pid: int) -> bool:
    """
    Resume a suspended Windows process using NtResumeProcess via ctypes.
    Blocks execution if OpenProcess returns a null handle.

    Args:
        pid: Process ID to resume.

    Returns:
        True if process was resumed successfully.
    """
    try:
        kernel32 = ctypes.windll.kernel32
        ntdll = ctypes.windll.ntdll

        PROCESS_SUSPEND_RESUME = 0x0800
        handle = kernel32.OpenProcess(PROCESS_SUSPEND_RESUME, False, pid)

        if not handle:
            print(f"  [THAW] ✖ Access Denied. Cannot open resume handle for PID {pid}",
                  file=sys.stderr)
            return False

        result = ntdll.NtResumeProcess(handle)
        kernel32.CloseHandle(handle)

        if result == 0:
            print(f"  [THAW] ✔ NtResumeProcess → PID {pid} RESUMED")
            return True
        else:
            print(f"  [THAW] ✖ NtResumeProcess returned 0x{result:08X}",
                  file=sys.stderr)
            return False
    except (OSError, AttributeError) as e:
        print(f"  [THAW] ✖ Windows resume fault: {e}", file=sys.stderr)
        return False