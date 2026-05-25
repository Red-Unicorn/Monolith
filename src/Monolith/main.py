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
from gui.theme.fonts import register_application_fonts
from core.utils.env import load_environment
from core.utils.logger import logger

load_environment()

logger.info("Application started")


def main() -> None:
    """
    Bootstrap the Monolith application.

    Sets global appearance defaults, creates the root Tk window,
    hands control to the WindowManager, and enters the Tk event loop.
    """
    app = MonolithApp()
    app.mainloop()


if __name__ == "__main__":
    main()
