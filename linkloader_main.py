
import os
import sys
import mmap
import struct
import importlib.util
import time
import logging
import signal
from typing import Optional

from config import (
    EXPECTED_TOKEN,
    LINKLOADER_ROOT,
    TOKEN_MIRROR_PATH,
    TOKEN_FMT,
    TOKEN_SIZE,
    CONNECTION_MODULE,
    GIVE_CONTROLS_MODULE,
    BUS_STATE_PATH,
    BUS_MAGIC,
    BUS_STAGE_OK,
    BUS_HEADER_FMT,
    BUS_HEADER_SIZE,
    KERNEL_VERSION,
    KERNEL_NAME,
    MODULE_TIMEOUT_S,
)

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logger = logging.getLogger("linkloader")


# ---------------------------------------------------------------------------
# TIME HELPERS
# ---------------------------------------------------------------------------

def _ts() -> str:
    """Return formatted timestamp with microseconds."""
    t = time.time()
    return time.strftime("%H:%M:%S", time.gmtime(t)) + f".{t % 1:.6f}"[1:8]


# ---------------------------------------------------------------------------
# STAGE 1 — RDI TOKEN
# ---------------------------------------------------------------------------

def _write_token_mirror(token: int) -> bool:
    """
    Write boot token as little-endian uint64_t to mmap register mirror.

    Args:
        token: 64-bit boot token value.

    Returns:
        True if token was written successfully.
    """
    try:
        os.makedirs(os.path.dirname(TOKEN_MIRROR_PATH), exist_ok=True)
        with open(TOKEN_MIRROR_PATH, "wb") as fh:
            fh.write(struct.pack(TOKEN_FMT, token))
        logger.info(f"rdi_mirror written  val=0x{token:010X}  path={TOKEN_MIRROR_PATH}")
        return True
    except OSError as exc:
        logger.critical(f"rdi_mirror write failed  errno={exc.errno}")
        return False


def _verify_rdi_token() -> bool:
    """
    Read 8 bytes from mmap register mirror and verify against EXPECTED_TOKEN.

    Returns:
        True if token matches expected value.
    """
    try:
        if not os.path.isfile(TOKEN_MIRROR_PATH):
            logger.critical("rdi_mirror absent — bootloader stage did not fire")
            return False
        with open(TOKEN_MIRROR_PATH, "r+b") as fh:
            with mmap.mmap(fh.fileno(), TOKEN_SIZE, access=mmap.ACCESS_READ) as mm:
                raw = mm.read(TOKEN_SIZE)
        val = struct.unpack(TOKEN_FMT, raw)[0]
        if val == EXPECTED_TOKEN:
            logger.info(f"token OK  read=0x{val:010X}  expected=0x{EXPECTED_TOKEN:010X}")
            return True
        logger.critical(
            f"token MISMATCH  read=0x{val:010X}  expected=0x{EXPECTED_TOKEN:010X}"
        )
        return False
    except (OSError, struct.error) as exc:
        logger.critical(f"token read error: {exc}")
        return False


# ---------------------------------------------------------------------------
# STAGE 2b — BUS STATE VERIFY
# ---------------------------------------------------------------------------

def _verify_bus_state() -> bool:
    """
    Read .bus_state header and verify magic + stage.

    Returns:
        True if bus state header is valid.
    """
    try:
        if not os.path.isfile(BUS_STATE_PATH):
            logger.critical(f"bus_state absent  path={BUS_STATE_PATH}")
            return False
        with open(BUS_STATE_PATH, "rb") as fh:
            raw = fh.read(BUS_HEADER_SIZE)
        if len(raw) < BUS_HEADER_SIZE:
            logger.critical(f"bus_state truncated  read={len(raw)}B")
            return False
        magic, ver, stage, _res, ts, gexel_n, denel_n, jlen = \
            struct.unpack(BUS_HEADER_FMT, raw)
        if magic != BUS_MAGIC:
            logger.critical(f"bus_state magic invalid  got={magic!r}")
            return False
        if stage != BUS_STAGE_OK:
            logger.critical(f"bus_state stage invalid  got=0x{stage:02X}")
            return False
        logger.info(
            f"bus_state OK  magic={magic!r}  ver=0x{ver:02X}  stage=0x{stage:02X}  "
            f"files={gexel_n + denel_n}  payload={jlen}B  "
            f"ts={time.strftime('%H:%M:%S', time.gmtime(ts))}"
        )
        return True
    except (OSError, struct.error) as exc:
        logger.critical(f"bus_state read error: {exc}")
        return False


# ---------------------------------------------------------------------------
# MODULE RUNNER (with timeout)
# ---------------------------------------------------------------------------

class ModuleTimeout(Exception):
    """Raised when a boot module exceeds its time limit."""
    pass


def _timeout_handler(signum: int, frame) -> None:
    """Signal handler for module timeout."""
    raise ModuleTimeout("Module execution timed out")


def _run_module(label: str, path: str, entry: str) -> bool:
    """
    Dynamically load a Python module and call its entry function.

    The module is given MODULE_TIMEOUT_S seconds to complete.

    Args:
        label: Human-readable module name.
        path: Absolute path to the .py file.
        entry: Name of the entry-point function.

    Returns:
        True if module executed successfully.
    """
    # Validate inputs
    if not path or not os.path.isfile(path):
        logger.critical(f"module not found  path={path}")
        return False
    if not entry:
        logger.critical(f"entry function name is empty  module={label}")
        return False

    # Set timeout alarm (POSIX only — SIGALRM)
    old_handler = None
    try:
        if hasattr(signal, "SIGALRM"):
            old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(int(MODULE_TIMEOUT_S))
    except (ValueError, OSError):
        pass  # Timeout not supported on this platform

    try:
        spec = importlib.util.spec_from_file_location(label, path)
        if spec is None or spec.loader is None:
            logger.critical(f"spec build failed  path={path}")
            return False

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fn = getattr(mod, entry, None)
        if fn is None:
            logger.critical(f"entry not found  fn={entry}  module={label}")
            return False

        t0 = time.monotonic()
        result = bool(fn())
        elapsed_ms = (time.monotonic() - t0) * 1000
        logger.info(f"module={label}  fn={entry}  result={result}  elapsed={elapsed_ms:.2f}ms")
        return result

    except ModuleTimeout:
        logger.critical(f"module={label}  timed out after {MODULE_TIMEOUT_S}s")
        return False
    except Exception as exc:
        logger.critical(f"module={label}  exception: {exc}")
        return False
    finally:
        # Restore signal handler and cancel alarm
        if old_handler is not None and hasattr(signal, "SIGALRM"):
            signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)


# ---------------------------------------------------------------------------
# BOOT ORCHESTRATOR
# ---------------------------------------------------------------------------

def run_boot_sequence() -> bool:
    """
    Execute the full boot sequence in strict order.
    Halts on any stage failure.

    Boot stages:
        Stage 1  : RDI token verify
        Stage 2  : connection.py — bus wiring
        Stage 2b : .bus_state header verify
        Stage 3  : give_controls.py — master plane dispatch

    Returns:
        True if all stages completed successfully.
    """
    logger.info("--- boot sequence start ---")
    logger.info(f"kernel={KERNEL_VERSION}  codename='{KERNEL_NAME}'")
    logger.info(f"expected_token=0x{EXPECTED_TOKEN:010X}")

    # Stage 1 — RDI token
    logger.info("stage=1  op=rdi_token_verify")
    if not _write_token_mirror(EXPECTED_TOKEN):
        logger.critical("stage=1  result=FAIL  action=HALT")
        return False
    if not _verify_rdi_token():
        logger.critical("stage=1  result=FAIL  action=HALT")
        return False
    logger.info("stage=1  result=PASS")

    # Stage 2 — Bus wiring
    logger.info("stage=2  op=bus_wiring  module=connection.py")
    if not _run_module("connection", CONNECTION_MODULE, "check_and_wire_system_bus"):
        logger.critical("stage=2  result=FAIL  action=HALT")
        return False

    # Stage 2b — Bus state verification
    logger.info("stage=2b  op=bus_state_verify")
    if not _verify_bus_state():
        logger.critical("stage=2b  result=FAIL  action=HALT")
        return False
    logger.info("stage=2  result=PASS")

    # Stage 3 — Master plane dispatch
    logger.info("stage=3  op=master_plane_dispatch  module=give_controls.py")
    if not _run_module("give_controls", GIVE_CONTROLS_MODULE, "release_authority"):
        logger.critical("stage=3  result=FAIL  action=HALT")
        return False
    logger.info("stage=3  result=PASS")

    logger.info("--- boot sequence complete --- status=0")
    return True


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> bool:
    """Entry point. Wraps run_boot_sequence with top-level error handling."""
    try:
        return run_boot_sequence()
    except Exception as exc:
        logger.critical(f"boot sequence crashed: {exc}")
        return False


if __name__ == "__main__":
    # Configure logging for standalone run
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    sys.exit(0 if main() else 1)