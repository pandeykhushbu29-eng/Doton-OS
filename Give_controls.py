
import os
import sys
import subprocess
import threading
import time
import logging
from typing import Any

from config import (
    MASTER_PLANES_CONFIG,
    SETTLE_WINDOW_S,
)

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logger = logging.getLogger("give_controls")

# ---------------------------------------------------------------------------
# MASTER PLANE TARGET TABLE
# ---------------------------------------------------------------------------
_CURRENT_DIR = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))
ROOT = os.path.dirname(_CURRENT_DIR).replace("\\", "/")

MASTER_PLANES: tuple[tuple[str, str], ...] = MASTER_PLANES_CONFIG

_PYTHON: str = sys.executable  # reuse same interpreter binary


# ---------------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------------

def _ts() -> str:
    """Return formatted timestamp with microseconds."""
    return time.strftime("%H:%M:%S", time.gmtime()) + f".{time.time() % 1:.6f}"[1:8]


def _preflight(label: str, path: str) -> bool:
    """Verify that a master plane target file exists before launching."""
    if not path:
        logger.critical(f"{label}: target path is empty")
        return False
    if not os.path.isfile(path):
        logger.critical(f"{label}: target not found — path={path}")
        return False
    return True


def _spawn(label: str, path: str, out: dict) -> None:
    """
    Thread worker. Spawns master plane via subprocess.

    Args:
        label: Plane identifier.
        path: Path to the target script.
        out: Shared dict to store Popen handle or exception.
    """
    try:
        proc = subprocess.Popen(
            [_PYTHON, path],
            close_fds=True,
        )
        out[label] = proc
        logger.info(f"{label}: fork OK — pid={proc.pid}  path={path}")
    except OSError as exc:
        out[label] = exc
        logger.critical(f"{label}: fork failed — errno={exc.errno} {exc.strerror}")


# ---------------------------------------------------------------------------
# PUBLIC ENTRY POINT
# ---------------------------------------------------------------------------

def release_authority() -> bool:
    """
    Dispatch control to both master planes simultaneously.

    Procedure:
        1. Pre-flight: verify each target file exists.
        2. Launch two daemon threads; each calls subprocess.Popen concurrently.
        3. Join threads (launch completes, not process exit).
        4. Sleep SETTLE_WINDOW_S; poll each process for early exit.
        5. Return True if both processes are still running.

    Returns:
        True if both planes launched and are running.
    """
    try:
        # --- pre-flight ---
        for label, path in MASTER_PLANES:
            if not _preflight(label, path):
                logger.critical("pre-flight failed — handover aborted")
                return False

        logger.info(f"pre-flight OK — launching {len(MASTER_PLANES)} plane(s)")

        # --- simultaneous dispatch ---
        handles: dict = {}
        threads: list[threading.Thread] = [
            threading.Thread(
                target=_spawn,
                args=(label, path, handles),
                daemon=True,
                name=f"spawn:{label}",
            )
            for label, path in MASTER_PLANES
        ]

        t0 = time.monotonic()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        dispatch_ms = (time.monotonic() - t0) * 1000

        logger.info(f"dispatch complete — elapsed={dispatch_ms:.2f}ms")

        # --- settle + liveness poll ---
        time.sleep(SETTLE_WINDOW_S)

        all_live = True
        for label, _ in MASTER_PLANES:
            entry = handles.get(label)
            if isinstance(entry, subprocess.Popen):
                rc = entry.poll()
                if rc is None:
                    logger.info(f"{label}: pid={entry.pid}  state=RUNNING")
                else:
                    logger.critical(f"{label}: pid={entry.pid}  state=EXITED  rc={rc}")
                    all_live = False
            else:
                logger.critical(f"{label}: no handle — spawn did not complete")
                all_live = False

        if all_live:
            logger.info("authority transfer complete — all planes running")
        else:
            logger.critical("authority transfer incomplete — check logs above")

        return all_live

    except Exception as exc:
        logger.critical(f"unhandled exception: {exc}")
        return False


if __name__ == "__main__":
    # Configure logging for standalone run
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    sys.exit(0 if release_authority() else 1)