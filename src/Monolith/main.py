"""
main.py  –  Monolith Application Entry Point
=============================================
Bootstraps CustomTkinter, creates the root window, hands control to
the WindowManager, and enters the Tk event loop.

Author  : Red Unicorn (Intl') Holding Group
License : Proprietary – All rights reserved
"""

from __future__ import annotations

# ── Local ─────────────────────────────────────────────────────────────────────
from gui.window_manager import MonolithApp
from core.utils.env import load_environment
from core.utils.logger import logger

from core.utils import ref_number_generator
from gui.widgets.image_provider import initialize_registry
from config.settings import REGISTRY

load_environment()

logger.info("Application started")


def main() -> None:
    """
    Bootstrap the Monolith application.

    Sets global appearance defaults, creates the root Tk window,
    hands control to the WindowManager, and enters the Tk event loop.
    """

    # Initializing values registry
    initialize_registry()

    # Start GUI
    app = MonolithApp()
    app.mainloop()


if __name__ == "__main__":
    main()
