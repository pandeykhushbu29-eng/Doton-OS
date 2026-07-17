
import os
import sys
import struct
import json
import time
import logging
from pathlib import Path

from config import (
    GEXEL_CORRIDOR,
    DENEL_CORRIDOR,
    KERNEL_ROOT,
    BUS_STATE_PATH,
    BUS_MANIFEST_PATH,
    BUS_MAGIC,
    BUS_VERSION,
    BUS_STAGE_CONNECT,
    BUS_HEADER_FMT,
    BUS_HEADER_SIZE,
    DENEL_PREFIXES,
)

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logger = logging.getLogger("connection")

# ---------------------------------------------------------------------------
# PATHS (using config)
# ---------------------------------------------------------------------------
TARGET_CORRIDORS: tuple[str, ...] = (GEXEL_CORRIDOR, DENEL_CORRIDOR)


# ---------------------------------------------------------------------------
# CORRIDOR INDUCTION
# ---------------------------------------------------------------------------

def _induct_corridors() -> bool:
    """Verify or create the gexel/denel corridor directories."""
    for path in TARGET_CORRIDORS:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"corridor ready  path={path}")
        except OSError as exc:
            logger.critical(f"makedirs failed  path={path}  errno={exc.errno}")
            return False
    return True


# ---------------------------------------------------------------------------
# KERNEL TREE WALK + PARTITIONER
# ---------------------------------------------------------------------------

def _walk_and_partition() -> tuple[list[str], list[str]]:
    """
    Walk kernel source tree and partition files into gexel/denel buckets.

    Rule: if relative path starts with any DENEL_PREFIX → denel; else → gexel.

    Returns:
        Tuple of (gexel_files, denel_files) as absolute path lists.
    """
    gexel: list[str] = []
    denel: list[str] = []

    kernel_path = Path(KERNEL_ROOT)
    if not kernel_path.is_dir():
        logger.warning(f"kernel root absent — walk skipped  path={KERNEL_ROOT}")
        return gexel, denel

    logger.info(f"walking  root={KERNEL_ROOT}")
    total = 0

    try:
        for dirpath, dirnames, filenames in os.walk(str(kernel_path)):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for fname in filenames:
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(abs_path, KERNEL_ROOT).replace("\\", "/")
                if any(rel_path.startswith(p) for p in DENEL_PREFIXES):
                    denel.append(abs_path)
                else:
                    gexel.append(abs_path)
                total += 1
                if total % 5000 == 0:
                    logger.info(f"walk progress  scanned={total}")
    except OSError as exc:
        logger.critical(f"walk failed  errno={exc.errno}")
        return gexel, denel

    logger.info(f"walk complete  total={total}  gexel={len(gexel)}  denel={len(denel)}")
    return gexel, denel


# ---------------------------------------------------------------------------
# BUS STATE WRITER
# ---------------------------------------------------------------------------

def _write_bus_state(gexel: list[str], denel: list[str]) -> bool:
    """
    Write binary .bus_state file with header + JSON payload.

    Args:
        gexel: List of gexel-owned file paths.
        denel: List of denel-owned file paths.

    Returns:
        True if write succeeded.
    """
    try:
        bus_dir = Path(BUS_STATE_PATH).parent
        bus_dir.mkdir(parents=True, exist_ok=True)

        payload = json.dumps(
            {"gexel": gexel, "denel": denel}, separators=(",", ":")
        ).encode("utf-8")
        header = struct.pack(
            BUS_HEADER_FMT,
            BUS_MAGIC, BUS_VERSION, BUS_STAGE_CONNECT,
            0x0000, int(time.time()),
            len(gexel), len(denel), len(payload),
        )
        with open(BUS_STATE_PATH, "wb") as fh:
            fh.write(header)
            fh.write(payload)
        logger.info(
            f"bus_state written  path={BUS_STATE_PATH}  "
            f"header={BUS_HEADER_SIZE}B  payload={len(payload)}B  "
            f"total={BUS_HEADER_SIZE + len(payload)}B"
        )
        return True
    except OSError as exc:
        logger.critical(f"bus_state write failed  errno={exc.errno}")
        return False


def _write_manifest(gexel: list[str], denel: list[str]) -> None:
    """
    Write human-readable .bus_manifest.txt alongside .bus_state.

    Args:
        gexel: List of gexel-owned file paths.
        denel: List of denel-owned file paths.
    """
    try:
        with open(BUS_MANIFEST_PATH, "w", encoding="utf-8") as fh:
            fh.write(f"BUS MANIFEST\n")
            fh.write(f"generated={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
            fh.write(f"gexel_count={len(gexel)}\n")
            fh.write(f"denel_count={len(denel)}\n\n")
            fh.write("[GEXEL — kernel source files]\n")
            for p in gexel:
                fh.write(f"  {p}\n")
            fh.write("\n[DENEL — daemon/service files]\n")
            for p in denel:
                fh.write(f"  {p}\n")
        logger.info(f"manifest written  path={BUS_MANIFEST_PATH}")
    except OSError as exc:
        logger.warning(f"manifest write failed  errno={exc.errno}")


# ---------------------------------------------------------------------------
# PUBLIC ENTRY POINT
# ---------------------------------------------------------------------------

def check_and_wire_system_bus() -> bool:
    """
    Full Stage-2 wiring: induct corridors, walk kernel tree, write bus state.

    Returns:
        True on successful bus wiring.
    """
    try:
        logger.info("--- stage-2 bus wiring start ---")

        if not _induct_corridors():
            return False

        gexel_files, denel_files = _walk_and_partition()

        if not _write_bus_state(gexel_files, denel_files):
            return False

        _write_manifest(gexel_files, denel_files)

        logger.info(
            f"bus wiring complete  "
            f"gexel_owns={len(gexel_files)}  denel_owns={len(denel_files)}"
        )
        logger.info("--- stage-2 bus wiring done --- status=0")
        return True

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
    sys.exit(0 if check_and_wire_system_bus() else 1)
