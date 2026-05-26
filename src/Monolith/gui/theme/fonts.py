"""
================================================================================
Module:        gui.theme.fonts
Description:   Cross-platform application font registry framework router.
Author:        Red Unicorn (Intl') Holding Group
License:       Proprietary – All rights reserved
Version:       1.0.3
================================================================================
"""

from __future__ import annotations
import sys
import os
from typing import Final
from core.utils.paths import get_asset_path
from core.utils.paths import find_project_root

FONT_DIR = find_project_root("main.py") / "assets" / "fonts"

# Global Typography String Constants mapping to the Font Families
FONT_MAIN_REGULAR: Final[str] = "Inter"
FONT_MAIN_BOLD: Final[str] = "Inter"
FONT_CODE_MONO: Final[str] = "JetBrains Mono"

ROBOTO = FONT_DIR / "Roboto-Regular.ttf"
ROBOTO_BOLD = FONT_DIR / "Roboto-Bold.ttf"
OSWALD = FONT_DIR / "Oswald-Regular.ttf"

def register_application_fonts() -> None:
    """
    Detect the underlying operating system platform and dynamically inject
    custom font buffers into memory using platform-specific APIs.
    """
    # ── PATH A: MACOS ARCHITECTURE ────────────────────────────────────────────
    if sys.platform == "darwin":
        try:
            # We import locally INSIDE the conditional check block.
            # This ensures Windows completely ignores these lines at runtime.
            from Foundation import NSURL
            from CoreGraphics import (
                CGDataProviderCreateWithURL,
                CGFontCreateWithDataProvider,
            )
            from CTFontManager import CTFontManagerRegisterGraphicsFont
        except ImportError:
            print("[WARN] Cocoa wrappers missing. Falling back to system fonts.")
            return

        target_fonts: list[str] = [
            "fonts/Inter-Regular.ttf",
            "fonts/Inter-Bold.ttf",
            "fonts/JetBrainsMono-Regular.ttf",
            "assets/fonts/Roboto-Regular.ttf",
            "assets/fonts/Roboto-Bold.ttf",
            "assets/fonts/Oswald-Regular.ttf",
            "assets/fonts/Roboto-Regular.ttf",
            "assets/fonts/Roboto-Bold.ttf",
            "assets/fonts/Roboto-ExtraLight.ttf",
            "assets/fonts/PTSans-Regular.ttf",
            "assets/fonts/PTSans-Bold.ttf",
            "assets/fonts/Roboto-Condensed-Regular.ttf",
            "assets/fonts/Roboto-Condensed-Bold.ttf",
            "assets/fonts/Roboto-Condensed-Light.ttf",
        ]

        for font_suffix in target_fonts:
            absolute_path: str = get_asset_path(font_suffix)
            if not os.path.exists(absolute_path):
                continue

            font_url: NSURL = NSURL.fileURLWithPath_(absolute_path)
            provider = CGDataProviderCreateWithURL(font_url)
            if provider:
                cg_font = CGFontCreateWithDataProvider(provider)
                if cg_font:
                    CTFontManagerRegisterGraphicsFont(cg_font, None)

    # ── PATH B: WINDOWS ARCHITECTURE ──────────────────────────────────────────
    elif sys.platform == "win32":
        try:
            # Windows uses the native Win32 GDI library to load private fonts
            import ctypes

            target_fonts_win: list[str] = [
                "fonts/Inter-Regular.ttf",
                "fonts/Inter-Bold.ttf",
                "fonts/JetBrainsMono-Regular.ttf",
                "fonts/Roboto-Regular.ttf",
                "fonts/Roboto-Bold.ttf",
                "fonts/Oswald-Regular.ttf",
            ]

            FR_PRIVATE: int = (
                0x10  # GDI constant flag: limits font availability to this process only
            )

            for font_suffix in target_fonts_win:
                absolute_path: str = get_asset_path(font_suffix)
                if os.path.exists(absolute_path):
                    # Call the Windows kernel directly to add the font resource
                    ctypes.windll.gdi32.AddFontResourceExW(absolute_path, FR_PRIVATE, 0)
        except Exception as e:
            print(f"[WARN] Failed to register Windows system font resources: {e}")
