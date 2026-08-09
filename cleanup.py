# Copyright (C) 2024 Avyaan Mishra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
cleanup.py — Graceful shutdown and cleanup for the boot sequence.

Registers atexit handlers that clean up temporary files,
release resources, and ensure clean exit state."""

import atexit
import os
import logging
from pathlib import Path

logger = logging.getLogger("cleanup")

_registered_cleanups: list[tuple[str, str]] = []


def register_temp_file(path: str, description: str = "temporary file") -> None:
    _registered_cleanups.append((path, description))
    logger.debug(f"Registered for cleanup: {description}  path={path}")

def _cleanup_all() -> None:
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
    from config import BUS_STATE_PATH, BUS_MANIFEST_PATH
    bus_state_path = str(BUS_STATE_PATH)
    manifest_path = str(BUS_MANIFEST_PATH)
    register_temp_file(bus_state_path, "bus_state file")
    register_temp_file(manifest_path, "bus_manifest file")

def register_mirror_cleanup() -> None:
    from config import TOKEN_MIRROR_PATH
    register_temp_file(str(TOKEN_MIRROR_PATH), "RDI token mirror")


vexit.register(_cleanup_all)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Cleanup module loaded — atexit andlers registered.")