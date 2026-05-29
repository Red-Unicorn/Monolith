"""
Enterprise-style project workflow form page.
"""

from __future__ import annotations

import customtkinter as ctk

from gui.theme.colors import BACKGROUND, CARD_BG

from core.utils.ref_number_generator import get_reference_values
from core.utils.misc import (
    country_to_iso2,
    country_to_iso3,
)

from gui.widgets.search_combobox import SearchComboBox
from gui.widgets.red_asterix import make_required_label
from gui.widgets.stepper import Stepper
from gui.widgets.image_provider import load_image
from gui.widgets.buttons import make_button

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────

# CARD_BG = "#111827"

INPUT_BG = "#1E293B"

TEXT = "#E5E7EB"
TEXT_MUTED = "#94A3B8"

ACCENT = "#EF4444"

BORDER = "#334155"

INPUT_HEIGHT = 44


class FolderPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        on_back=None,
        on_next=None,
    ):

        super().__init__(
            master,
            fg_color=BACKGROUND,
        )

        self.pack(
            fill="both",
            expand=True,
        )

        self.on_back = on_back
        self.on_next = on_next

        # ─────────────────────────────────────────
        # DATA
        # ─────────────────────────────────────────

        self.country_values = list(get_reference_values("countries").keys())

        self.sector_values = list(get_reference_values("sectors").keys())

        # ─────────────────────────────────────────
        # GRID
        # ─────────────────────────────────────────

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # BUILD UI
        self._build_card()

    # ─────────────────────────────────────────────────────────────
    # IMAGE PROVIDERS
    # ─────────────────────────────────────────────────────────────

    def country_image_provider(self, country: str):
        """
        Generic provider used by SearchComboBox.
        Returns a CTkImage or None.
        """

        if not country:
            return None

        iso2 = country_to_iso2(country)

        # IMPORTANT FIX:
        # country_to_iso2() can return ""
        # which caused:
        # flags/png/.png
        if not iso2:
            return None

        try:

            return load_image(
                f"flags/png/{iso2.lower()}.png",
                size=(20, 14),
            )

        except Exception:
            return None

    # ─────────────────────────────────────────────────────────────
    # CARD
    # ─────────────────────────────────────────────────────────────

    def _build_card(self):

        self.card = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            corner_radius=0,
        )

        self.card.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.card.grid_columnconfigure(0, weight=1)
        # self.card.grid_rowconfigure(1, weight=0)

        self._build_header()
        self._build_form()
        self._build_footer()

    # ─────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────

    def _build_header(self):

        self.header_frame = ctk.CTkFrame(
            self.card,
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
                "Type",
                "Details",
                "Generated",
            ],
            current_step=2,
        )

        self.stepper.pack(
            fill="x",
        )

    # ─────────────────────────────────────────────────────────────
    # FORM
    # ─────────────────────────────────────────────────────────────

    def _build_form(self):

        self.form_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent",
        )

        self.form_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=40,
        )

        self.form_frame.grid_columnconfigure(0, weight=2)
        self.form_frame.grid_columnconfigure(1, weight=1)

        # ─────────────────────────────────────────
        # COUNTRY
        # ─────────────────────────────────────────

        country_label = make_required_label(
            self.form_frame,
            "Country of Origin",
        )

        country_label.grid(
            row=0,
            column=0,
            sticky="w",
            # pady=(0, 8),
        )

        self.country_combo = SearchComboBox(
            self.form_frame,
            values=self.country_values,
            # GENERIC IMAGE SYSTEM
            image_provider=self.country_image_provider,
            # WHAT .get() RETURNS
            value_mapper=lambda country: country_to_iso3(country),
            placeholder_text="Type any country...",
            height=INPUT_HEIGHT,
            fg_color=INPUT_BG,
            corner_radius=8,
            command=self.verify_country_output,
        )

        self.country_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 18),
            pady=(0, 10),
        )

        # ─────────────────────────────────────────
        # SECTOR
        # ─────────────────────────────────────────

        sector_label = make_required_label(
            self.form_frame,
            "Sector",
        )

        sector_label.grid(
            row=0,
            column=1,
            sticky="w",
            # pady=(0, 8),
        )

        self.sector_combo = SearchComboBox(
            self.form_frame,
            values=self.sector_values,
            height=INPUT_HEIGHT,
            placeholder_text="Select Project's sector",
            # OPTIONAL:
            # no images for sectors for now
            image_provider=None,
        )

        self.sector_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )

        # ─────────────────────────────────────────
        # PROJECT NAME
        # ─────────────────────────────────────────

        project_label = make_required_label(
            self.form_frame,
            "Project Name",
        )

        project_label.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            # pady=(0, 8),
        )

        self.project_entry = ctk.CTkEntry(
            self.form_frame,
            height=INPUT_HEIGHT,
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=0,
            corner_radius=8,
            font=("Inter", 14),
            placeholder_text="Digital Banking Platform",
            placeholder_text_color="#94A3B8",  # "#9CA3AF",
        )

        self.project_entry.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 10),
        )

        # ─────────────────────────────────────────
        # DESCRIPTION
        # ─────────────────────────────────────────

        self._create_label(
            text="Description (max 200 chars.)",
            row=4,
            column=0,
            columnspan=2,
            # pady=(10, 0),
        )

        self.description_container = ctk.CTkFrame(
            self.form_frame,
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=0,
            corner_radius=8,
            height=100,
        )

        self.description_container.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 20),
        )

        self.description_container.grid_columnconfigure(0, weight=1)
        self.description_container.grid_rowconfigure(0, weight=0)

        self.description_box = ctk.CTkTextbox(
            self.description_container,
            fg_color="transparent",
            border_width=0,
            activate_scrollbars=False,
            font=("Inter", 12),
            text_color=TEXT,
            height=100,
        )

        self.description_box.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=12,
            pady=(10, 10),
        )

        self.counter_label = ctk.CTkLabel(
            self.description_container,
            text="0 / 200",
            text_color=TEXT_MUTED,
            font=("Inter", 8),
        )

        self.counter_label.place(
            relx=0.985,
            rely=0.985,
            anchor="se",
        )

        self.description_box.bind(
            "<KeyRelease>",
            self._update_counter,
        )

    # ─────────────────────────────────────────────────────────────
    # LABEL HELPER
    # ─────────────────────────────────────────────────────────────

    def _create_label(
        self,
        text,
        row,
        column,
        columnspan=1,
    ):

        label = ctk.CTkLabel(
            self.form_frame,
            text=text,
            text_color=TEXT,
            font=("Inter", 12),
        )

        label.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="w",
            pady=(0, 0),
        )

    # ─────────────────────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────────────────────

    def _build_footer(self):

        self.footer = ctk.CTkFrame(
            self.card,
            fg_color="transparent",
        )

        self.footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=40,
            pady=(15, 35),
        )

        self.footer.grid_columnconfigure(0, weight=1)

        # CANCEL
        self.cancel_button = make_button(
            master=self.footer,
            text="Previous",
            command=self._back,
            enable_border_hover=True,
            variant="primary",
            size="md",
        )

        # self.cancel_button.pack(
        #     pady=(0, 60),
        # )
        # self.cancel_button = ctk.CTkButton(
        #     self.footer,
        #     text="Previous",
        #     width=150,
        #     height=48,
        #     fg_color="transparent",
        #     border_width=1,
        #     border_color="#475569",
        #     hover_color="#1E293B",
        #     corner_radius=10,
        #     font=("Inter", 15, "bold"),
        #     command=self._back,
        # )

        self.cancel_button.grid(
            row=0,
            column=0,
            sticky="w",
        )

        # NEXT
        self.next_button = make_button(
            master=self.footer,
            text="Next",
            command=self._next,
            enable_border_hover=True,
            variant="secondary",
            size="md",
        )

        # self.next_button = ctk.CTkButton(
        #     self.footer,
        #     text="Next",
        #     width=150,
        #     height=48,
        #     fg_color=ACCENT,
        #     hover_color="#DC2626",
        #     corner_radius=10,
        #     font=("Inter", 15, "bold"),
        #     command=self._next,
        # )

        self.next_button.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # ─────────────────────────────────────────────────────────────
    # EVENTS
    # ─────────────────────────────────────────────────────────────

    def _update_counter(self, event=None):

        text = self.description_box.get(
            "1.0",
            "end-1c",
        )

        if len(text) > 200:

            self.description_box.delete(
                "1.0 + 200 chars",
                "end",
            )

            text = self.description_box.get(
                "1.0",
                "end-1c",
            )

        self.counter_label.configure(text=f"{len(text)} / 200")

    # ─────────────────────────────────────────────────────────────
    # DEBUG
    # ─────────────────────────────────────────────────────────────

    def verify_country_output(self, selected_code):

        print(f"Country selected: {selected_code}")

    # ─────────────────────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────────────────────

    def _back(self):

        if self.on_back:
            self.on_back()

    def _next(self):

        data = {
            "country": self.country_combo.get(),
            "sector": self.sector_combo.get(),
            "project_name": self.project_entry.get(),
            "description": self.description_box.get(
                "1.0",
                "end-1c",
            ),
        }

        print(data)

        if self.on_next:
            self.on_next(data)
