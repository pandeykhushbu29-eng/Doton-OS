"""
Linkloader Package

Boot-stage orchestrator that manages RDI token verification,
system bus wiring, and master plane dispatch.

Exported components:
    linkloader_main      — Stage-2 boot orchestrator
    connection           — Bus wiring / kernel partitioner
    Give_controls        — Master plane subprocess dispatch
    denel master         — DENEL software master freeze rail
    config               — Central configuration constants
"""

__version__ = "0.1.0"
__codename__ = "avyaan"
