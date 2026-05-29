"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.home_page
DESCRIPTION:   Streamlined single-action home operational hub.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       8.1.0
================================================================================
"""

from __future__ import annotations

import customtkinter as ctk
from PIL import Image

# ── Design System Injections ──────────────────────────────────────────────────
from gui.widgets.buttons import make_button
from core.utils.paths import get_asset_path
from gui.theme.colors import CARD_BG
from core.utils.logger import logger
from gui.widgets.stepper import Stepper

# ──────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ──────────────────────────────────────────────────────────────────────────────

CONTENT_PADX = 60
CARD_SPACING = 20

# ──────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ──────────────────────────────────────────────────────────────────────────────


class HomePage(ctk.CTkFrame):
    """
    Main operational entry page.

    Layout:
    ─────────────────────────────────────────
    TOP:
        [ PROJECT ] [ DOCUMENT ]

    BOTTOM:
        [ DATABASE ]
    """

    def __init__(self, master, on_navigate=None):

        super().__init__(
            master,
            fg_color=CARD_BG,
        )

        self.on_navigate = on_navigate

        # ─────────────────────────────────────────────────────────────
        # PAGE LAYOUT
        # ─────────────────────────────────────────────────────────────

        self.pack(
            fill="both",
            expand=True,
        )

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # BUILD UI
        self._build_header()
        self._build_content()

    # ─────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────

    def _build_header(self):

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=40,
            pady=(30, 30),
        )

        self.stepper = Stepper(
            self.header_frame,
            steps=[
                "Type",
                "Details",
                "Generated",
            ],
            current_step=1,
        )

        self.stepper.pack(
            fill="x",
        )

    # ─────────────────────────────────────────────────────────────
    # MAIN CONTENT
    # ─────────────────────────────────────────────────────────────

    def _build_content(self):

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=CONTENT_PADX,
            pady=(0, 30),
        )

        # ONLY 2 COLUMNS
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # ROWS
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=0)

        self._build_project_button()
        self._build_document_button()
        self._build_database_button()

    # ─────────────────────────────────────────────────────────────
    # PROJECT BUTTON
    # ─────────────────────────────────────────────────────────────

    def _build_project_button(self):

        folder_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/folder.png")),
            dark_image=Image.open(get_asset_path("icons/folder.png")),
            size=(64, 64),
        )

        self.project_button = make_button(
            master=self.content_frame,
            text="PROJECT / RESOURCE",
            command=self._handle_folder_workflow,
            enable_border_hover=True,
            compound="top",
            image=folder_icon,
            variant="primary",
            size="lg",
        )

        self.project_button.grid(
            row=0,
            column=0,
            padx=(0, CARD_SPACING),
            sticky="nsew",
        )

    # ─────────────────────────────────────────────────────────────
    # DOCUMENT BUTTON
    # ─────────────────────────────────────────────────────────────

    def _build_document_button(self):

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
            compound="top",
            image=document_icon,
            variant="primary",
            size="lg",
        )

        self.document_button.grid(
            row=0,
            column=1,
            padx=(CARD_SPACING, 0),
            sticky="nsew",
        )

    # ─────────────────────────────────────────────────────────────
    # DATABASE BUTTON (BOTTOM FULL WIDTH)
    # ─────────────────────────────────────────────────────────────

    def _build_database_button(self):

        database_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/data-search.png")),
            dark_image=Image.open(get_asset_path("icons/data-search.png")),
            size=(40, 40),
        )

        self.database_button = make_button(
            master=self.content_frame,
            text="CHECK / VIEW DATABASE",
            command=self._handle_database_workflow,
            enable_border_hover=True,
            image=database_icon,
            compound="left",
            anchor="w",
            variant="primary",
            height=80,
            border_spacing=20,
        )

        self.database_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(25, 40),
        )

    # ─────────────────────────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────────────────────────

    def _handle_folder_workflow(self):

        logger.debug("[NAVIGATION] Folder workflow selected.")

        if self.on_navigate:

            self.on_navigate("folder")

    def _handle_document_workflow(self):

        logger.debug("[NAVIGATION] Document workflow selected.")

        if self.on_navigate:

            self.on_navigate("document")

    def _handle_database_workflow(self):

        logger.debug("[NAVIGATION] Database workflow selected.")

        if self.on_navigate:

            self.on_navigate("database")
