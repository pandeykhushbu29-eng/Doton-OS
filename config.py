"""
Central configuration module.

All magic constants, paths, and tunables are defined here.
Import via:  from config import *
"""

import os
import struct
from pathlib import Path

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
ROOT_STR = str(ROOT).replace("\\", "/")  # string version for backward-compat

# Default path placeholder — user should replace with actual kernel directory
KERNEL_PLACEHOLDER = "_Fill_name_of_your_file_needed_here_"

# Daemon placeholder
DAEMON_PLACEHOLDER = "__fill_name_of_daemon_service_needed_here__"

# Kernel connection placeholder
KERNEL_CONNECTION_MARKER = "__add_kernel_connection_of_your_choice__"

# ---------------------------------------------------------------------------
# BOOT TOKEN (RDI)
# ---------------------------------------------------------------------------
EXPECTED_TOKEN: int = 0x0011045110
TOKEN_FMT: str = "<Q"
TOKEN_SIZE: int = struct.calcsize(TOKEN_FMT)

# ---------------------------------------------------------------------------
# MODULE ROOTS
# ---------------------------------------------------------------------------
LINKLOADER_ROOT: str = f"{ROOT_STR}/{KERNEL_PLACEHOLDER}"
TOKEN_MIRROR_PATH: str = f"{LINKLOADER_ROOT}/.rdi_mirror"

CONNECTION_MODULE: str = f"{LINKLOADER_ROOT}/connection.py"
GIVE_CONTROLS_MODULE: str = f"{LINKLOADER_ROOT}/give_controls.py"

# ---------------------------------------------------------------------------
# BUS STATE
# ---------------------------------------------------------------------------
BUS_STATE_PATH: str = f"{ROOT_STR}/.bus_state"
BUS_MANIFEST_PATH: str = f"{ROOT_STR}/.bus_manifest.txt"
BUS_MAGIC: bytes = b"FASB"
BUS_VERSION: int = 0x01
BUS_STAGE_CONNECT: int = 0x02
BUS_STAGE_OK: int = 0x02
BUS_HEADER_FMT: str = "<4sBBHQIII"
BUS_HEADER_SIZE: int = struct.calcsize(BUS_HEADER_FMT)

# ---------------------------------------------------------------------------
# KERNEL METADATA
# ---------------------------------------------------------------------------
KERNEL_VERSION: str = "7.1.0-rc3"
KERNEL_NAME: str = "Baby Opossum Posse"

# ---------------------------------------------------------------------------
# BOOT TIMEOUTS
# ---------------------------------------------------------------------------
MODULE_TIMEOUT_S: float = 30.0   # max seconds for a module to run
SETTLE_WINDOW_S: float = 0.30    # seconds to wait before liveness poll

# ---------------------------------------------------------------------------
# CORRIDOR PATHS
# ---------------------------------------------------------------------------
GEXEL_CORRIDOR: str = f"{ROOT_STR}/{KERNEL_PLACEHOLDER}"
DENEL_CORRIDOR: str = f"{ROOT_STR}/{KERNEL_PLACEHOLDER}"
KERNEL_ROOT: str = f"{ROOT_STR}/{KERNEL_PLACEHOLDER}/{KERNEL_PLACEHOLDER}"

# Daemon-related path prefixes — files matching these go to DENEL bucket
DENEL_PREFIXES: tuple[str, ...] = tuple(
    [DAEMON_PLACEHOLDER] * 14
)

# ---------------------------------------------------------------------------
# MASTER PLANES
# ---------------------------------------------------------------------------
MASTER_PLANES_CONFIG: tuple[tuple[str, str], ...] = (
    (DAEMON_PLACEHOLDER, f"{ROOT_STR}/{KERNEL_PLACEHOLDER}/{KERNEL_PLACEHOLDER}"),
    (DAEMON_PLACEHOLDER, f"{ROOT_STR}/{KERNEL_PLACEHOLDER}/{KERNEL_PLACEHOLDER}"),
)

# ---------------------------------------------------------------------------
# FREEZE RAIL TARGETS (POSIX)
# ---------------------------------------------------------------------------
POSIX_FREEZE_TARGETS: tuple[str, ...] = (
    DAEMON_PLACEHOLDER,
    DAEMON_PLACEHOLDER,
)

# ---------------------------------------------------------------------------
# FREEZE RAIL TARGETS (WINDOWS)
# ---------------------------------------------------------------------------
WINDOWS_FREEZE_TARGETS: tuple[str, ...] = (
    DAEMON_PLACEHOLDER,
    DAEMON_PLACEHOLDER,
    DAEMON_PLACEHOLDER,
)
