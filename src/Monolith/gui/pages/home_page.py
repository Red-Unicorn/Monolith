"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.home_page
DESCRIPTION:   Streamlined single-action home operational hub. Removed wizard
               pipelines and multi-frame trackers for step-by-step clarity.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       7.0.0
================================================================================
"""

from __future__ import annotations

# from typing import Any, Optional
import customtkinter as ctk
from PIL import Image

# ── Design System Injections ──────────────────────────────────────────────────
from gui.widgets.buttons import make_button
from core.utils.paths import get_asset_path
from gui.theme.colors import BACKGROUND, TEXT_MUTED, TEXT, CARD_BG
from core.utils.logger import logger
from gui.widgets.stepper import Stepper

# from gui.theme.layout import APP_WIDTH, APP_HEIGHT

# ──────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ──────────────────────────────────────────────────────────────────────────────


class HomePage(ctk.CTkFrame):
    """
    Main wizard entry page.

    Presents the user with two large workflow choices:
    1. Project / Resource flow
    2. Document flow

    Designed for:
    - accessibility
    - large interaction targets
    - low cognitive load
    - future multi-step navigation
    """

    def __init__(self, master, on_navigate=None):
        super().__init__(master, fg_color=CARD_BG)

        self.on_navigate = on_navigate

        # ──────────────────────────────────────────────────────────────────
        # PAGE LAYOUT
        # ──────────────────────────────────────────────────────────────────

        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)

        # ──────────────────────────────────────────────────────────────────
        # HEADER / STEP INDICATOR
        # ──────────────────────────────────────────────────────────────────

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.header_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=(30, 30),
        )

        self.stepper = Stepper(
            self.header_frame,
            steps=[
                "Details",
                "Review",
                "Generated",
            ],
            current_step=1,
        )

        self.stepper.pack(
            fill="x",
        )

        # self.step_label = ctk.CTkLabel(
        #     self.header_frame,
        #     text="STEP 1 OF 3",
        #     font=("Oswald", 18, "bold"),
        #     text_color=TEXT_MUTED,
        # )
        # self.step_label.pack(anchor="w")  # ,pady=(0, 20))

        # self.title_label = ctk.CTkLabel(
        #     self.header_frame,
        #     text="Create Reference Number for:",
        #     font=("PT Sans", 12, "bold"),
        #     text_color=TEXT,
        # )
        # self.title_label.pack(anchor="w")  # , pady=(10, 0))

        # self.subtitle_label = ctk.CTkLabel(
        #     self.header_frame,
        #     text="Underping ?",
        #     font=("Arial", 12),
        #     text_color=MUTED,
        # )
        # self.subtitle_label.pack(anchor="w", pady=(10, 0))

        # ──────────────────────────────────────────────────────────────────
        # MAIN CONTENT
        # ──────────────────────────────────────────────────────────────────

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            # padx=20,
            pady=20,
            padx=60,
            # pady=(20, 20),
        )

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # ──────────────────────────────────────────────────────────────────
        # PROJECT / RESOURCE BUTTON
        # ──────────────────────────────────────────────────────────────────

        folder_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/folder.png")),
            dark_image=Image.open(get_asset_path("icons/folder.png")),
            size=(64, 64),
        )

        self.folder_button = make_button(
            master=self.content_frame,
            text="PROJECT/RESOURCE",
            command=self._handle_folder_workflow,
            enable_border_hover=True,
            image=folder_icon,
            variant="primary",
            size="lg",
        )

        self.folder_button.grid(
            row=0,
            column=0,
            padx=(0, 20),
            # pady=20,
            sticky="ew",
        )

        # ──────────────────────────────────────────────────────────────────
        # DOCUMENT BUTTON
        # ──────────────────────────────────────────────────────────────────

        document_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/file.png")),
            dark_image=Image.open(get_asset_path("icons/file.png")),
            size=(64, 64),
        )

        self.document_button = make_button(
            master=self.content_frame,
            text="DOCUMENTS",
            command=self._handle_document_workflow,
            enable_border_hover=True,
            image=document_icon,
            variant="primary",
            size="lg",
        )

        self.document_button.grid(
            row=0,
            column=1,
            padx=(20, 0),
            # pady=20,
            sticky="ew",
        )

    # ──────────────────────────────────────────────────────────────────────
    # ACTIONS
    # ──────────────────────────────────────────────────────────────────────

    def _handle_folder_workflow(self) -> None:
        """
        Navigate to project/resource workflow.
        """
        logger.debug("[NAVIGATION] Folder workflow selected.")

        if self.on_navigate:
            self.on_navigate("folder")

    def _handle_document_workflow(self) -> None:
        """
        Navigate to document workflow.
        """
        logger.debug("[NAVIGATION] Document workflow selected.")

        if self.on_navigate:
            self.on_navigate("document")
