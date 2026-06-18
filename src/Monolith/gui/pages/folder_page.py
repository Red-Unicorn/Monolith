"""
Enterprise-style project workflow form page with field validation.
"""

from __future__ import annotations

import customtkinter as ctk

from gui.theme.colors import BACKGROUND, CARD_BG

from core.utils.ref_number_generator import get_reference_values

from gui.widgets.search_combobox import SearchComboBox
from gui.widgets.custom_optionbox import CustomOptionMenu
from gui.widgets.red_asterix import make_required_label
from gui.widgets.stepper import Stepper

# from gui.widgets.image_provider import load_image
from gui.widgets.buttons import make_button
from config.settings import REGISTRY
from core.utils.logger import logger

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────

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
        Directly queries the centralized pre-loaded REGISTRY dictionary
        initialized at application boot sequence inside main.py.
        """
        if not country:
            return None

        # Import your shared data reference module
        from gui.widgets.image_provider import REGISTRY

        # Pull values directly out of your specified structural path configuration
        country_node = REGISTRY["countries"].get(country)
        if country_node:
            return country_node.get(
                "image"
            )  # Delivers the pre-loaded ctk.CTkImage instance object
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
        )

        self.country_combo = ctk.CTkOptionMenu(
            self.form_frame,
            values=self.country_values,  
            height=INPUT_HEIGHT,
            fg_color="#1E293B",
            button_color="#1E293B",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="#FFFFFF",
            # border_color="#334155",
            # max_results=20,
        )

        # self.country_combo = CustomOptionMenu(
        #     self.form_frame,
        #     values=self.country_values,  # ["Project", "Resource"],
        #     height=INPUT_HEIGHT,
        #     placeholder_text="Select country",
        #     image_provider=None,
        #     # max_results=20,
        # )
        # self.country_combo = SearchComboBox(
        #     self.form_frame,
        #     values=self.country_values,
        #     image_provider=self.country_image_provider,  # Points to REGISTRY direct query loop
        #     # value_mapper=lambda country: country_to_iso3(country),
        #     placeholder_text="Type any country...",
        #     height=INPUT_HEIGHT,
        #     fg_color=INPUT_BG,
        #     corner_radius=8,
        #     border_width=1,
        #     # command=self.verify_country_output,
        # )

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
        )

        self.sector_combo = ctk.CTkOptionMenu(
            self.form_frame,
            values=self.sector_values,  
            height=INPUT_HEIGHT,
            fg_color="#1E293B",
            button_color="#1E293B",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="#FFFFFF",
            # border_color="#334155",
            # max_results=20,
        )

        # self.sector_combo = CustomOptionMenu(
        #     self.form_frame,
        #     values=self.sector_values,  # ["Project", "Resource"],
        #     height=INPUT_HEIGHT,
        #     placeholder_text="Select sector",
        #     image_provider=None,
        #     # max_results=20,
        # )

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
            "Project/Resource Name",
        )

        project_label.grid(
            row=2,
            column=0,
            # columnspan=2,
            sticky="w",
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
            placeholder_text_color="#94A3B8",
        )

        self.project_entry.grid(
            row=3,
            column=0,
            # columnspan=2,
            sticky="ew",
            padx=(0, 18),
            pady=(0, 10),
        )

        type_label = make_required_label(
            self.form_frame,
            "Type",
        )

        type_label.grid(
            row=2,
            column=1,
            sticky="w",
        )

        self.optionmenu = CustomOptionMenu(
            self.form_frame,
            values=["Project", "Resource"],
            height=INPUT_HEIGHT,
            placeholder_text="Project/Resource",
            image_provider=None,
            max_results=2,
        )

        self.optionmenu.grid(
            row=3,
            column=1,
            # columnspan=1,
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
    # NAVIGATION
    # ─────────────────────────────────────────────────────────────

    def _back(self):
        if self.on_back:
            self.on_back()

    def _next(self):
        # 1. Reset field borders
        if hasattr(self.country_combo, "configure"):
            self.country_combo.configure(border_color=BORDER)
        if hasattr(self.sector_combo, "configure"):
            self.sector_combo.configure(border_color=BORDER)
        self.project_entry.configure(border_color=BORDER)

        # 2. Grab field tokens
        country_output = self.country_combo.get()
        sector_selection = self.sector_combo.get()
        project_name = self.project_entry.get().strip()
        type_selection = self.optionmenu.get()
        # 3. Check required parameters
        is_valid = True

        if not country_output:
            is_valid = False
            if hasattr(self.country_combo, "configure"):
                self.country_combo.configure(border_width=1, border_color=ACCENT)

        if not sector_selection:
            is_valid = False
            if hasattr(self.sector_combo, "configure"):
                self.sector_combo.configure(border_width=1, border_color=ACCENT)

        if not project_name:
            is_valid = False
            self.project_entry.configure(border_width=1, border_color=ACCENT)

        if not is_valid:
            logger.debug("[VALIDATION WARNING] Missing mandatory fields.")
            return

        country_code = REGISTRY["countries"][country_output]["code"]
        sector_code = REGISTRY["sectors"][sector_selection]["code"]

        type_code = None
        type_code = "PRO" if type_selection == "Project" else "RES"
        # Pack final synchronized structured payload
        data = {
            "country": country_output,  # Full name string (e.g. "United States")
            "country_code": (
                country_code.upper() if country_code else None
            ),  # Clean ISO code token (e.g. "USA")
            "sector": sector_selection,
            "sector_code": sector_code,
            "name": project_name,
            "type": type_selection,
            "type_code": type_code,
            "description": self.description_box.get("1.0", "end-1c"),
        }

        if self.on_next:
            self.on_next(data)
