"""
cleanup.py — Graceful shutdown and cleanup for the boot sequence.

Registers atexit handlers that clean up temporary files,
release resources, and ensure clean exit state.
"""

import atexit
import os
import logging
from pathlib import Path

logger = logging.getLogger("cleanup")

# Track registered resources for cleanup
_registered_cleanups: list[tuple[str, str]] = []  # (path, description)


def register_temp_file(path: str, description: str = "temporary file") -> None:
    """
    Register a temporary file for cleanup at exit.

    Args:
        path: Absolute path to the temporary file.
        description: Human-readable description for logging.
    """
    _registered_cleanups.append((path, description))
    logger.debug(f"Registered for cleanup: {description}  path={path}")


def _cleanup_all() -> None:
    """
    Execute all registered cleanup actions.
    Called automatically at interpreter exit via atexit.
    """
    logger.info("Running cleanup handlers...")
    cleaned = 0
    errors = 0

    for path, description in _registered_cleanups:
        try:
            p = Path(path)
            if p.is_file():
                p.unlink()
                logger.info(f"Cleaned: {description}  path={path}")
                cleaned += 1
            elif p.is_dir():
                import shutil
                shutil.rmtree(path, ignore_errors=True)
                logger.info(f"Cleaned: {description}  path={path}")
                cleaned += 1
        except (OSError, PermissionError) as exc:
            logger.warning(f"Cleanup failed for {description}: {exc}")
            errors += 1

    if errors:
        logger.warning(f"Cleanup complete — {cleaned} cleaned, {errors} errors")
    else:
        logger.info(f"Cleanup complete — {cleaned} items cleaned")


def register_bus_state_cleanup() -> None:
    """
    Register .bus_state and .bus_manifest for cleanup on exit.
    Call during boot start to ensure clean state after shutdown.
    """
    from config import BUS_STATE_PATH, BUS_MANIFEST_PATH
    bus_state_path = str(BUS_STATE_PATH)
    manifest_path = str(BUS_MANIFEST_PATH)
    register_temp_file(bus_state_path, "bus_state file")
    register_temp_file(manifest_path, "bus_manifest file")


def register_mirror_cleanup() -> None:
    """
    Register .rdi_mirror for cleanup on exit.
    """
    from config import TOKEN_MIRROR_PATH
    register_temp_file(str(TOKEN_MIRROR_PATH), "RDI token mirror")


# Register the atexit handler
atexit.register(_cleanup_all)

if __name__ == "__main__":
    # Test harness
    logging.basicConfig(level=logging.INFO)
    print("Cleanup module loaded — atexit handlers registered.")