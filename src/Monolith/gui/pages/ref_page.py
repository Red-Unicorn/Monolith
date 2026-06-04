"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.ref_page
DESCRIPTION:   Generated reference result page.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       1.1.0
================================================================================
"""

from __future__ import annotations

import customtkinter as ctk
from PIL import Image
import pyperclip
import secrets
import re

# ── Local Imports ─────────────────────────────────────────────────────────────
from gui.widgets.buttons import make_button
from gui.widgets.stepper import Stepper

from core.utils.paths import get_asset_path

from gui.theme.colors import (
    CARD_BG,
    TEXT,
    TEXT_MUTED,
)

# ──────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ──────────────────────────────────────────────────────────────────────────────

CONTENT_PADX = 40

SUCCESS_GREEN = "#34D399"
SUCCESS_BG = "#123C36"

SECTION_BG = "#1E293B"

BORDER = "#334155"


class RefPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        data: dict,
        on_back=None,
        on_dashboard=None,
    ):

        super().__init__(
            master,
            fg_color=CARD_BG,
        )

        # ─────────────────────────────────────────
        # CALLBACKS
        # ─────────────────────────────────────────

        self.on_back = on_back
        self.on_dashboard = on_dashboard

        # ─────────────────────────────────────────
        # DATA
        # ─────────────────────────────────────────

        self.data = data

        # SAFE FALLBACKS
        self.reference_number = data.get(
            "reference_number",
            "MON-000001",
        )

        self.clean_filename = data.get(
            "clean_filename",
            "generated_document.pdf",
        )

        # ─────────────────────────────────────────
        # PAGE
        # ─────────────────────────────────────────

        self.pack(
            fill="both",
            expand=True,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # BUILD
        self._load_icons()

        self._build_header()
        self._build_content()
        self._build_footer()

    # ─────────────────────────────────────────────
    # ICONS
    # ─────────────────────────────────────────────

    def _load_icons(self):

        self.copy_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/copy.png")),
            dark_image=Image.open(get_asset_path("icons/copy.png")),
            size=(20, 21),
        )

        self.success_icon = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/check-circle.png")),
            dark_image=Image.open(get_asset_path("icons/check-circle.png")),
            size=(40, 40),
        )

    # ─────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────

    def _build_header(self):

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=CONTENT_PADX,
            pady=(30, 25),
        )

        self.stepper = Stepper(
            self.header_frame,
            steps=[
                "Type",
                "Details",
                "Generated",
            ],
            current_step=3,
        )

        self.stepper.pack(
            fill="x",
        )

    # ─────────────────────────────────────────────
    # CONTENT
    # ─────────────────────────────────────────────

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
        )

        self.content_frame.grid_columnconfigure(0, weight=1)

        self._build_reference_section()
        self._build_filename_section()
        self._build_success_section()

    # ─────────────────────────────────────────────
    # REFERENCE SECTION
    # ─────────────────────────────────────────────

    def _build_reference_section(self):

        self.reference_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=SECTION_BG,
            corner_radius=14,
            border_width=1,
            border_color=BORDER,
            height=90,
        )

        self.reference_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.reference_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.reference_frame,
            text="Reference Number",
            text_color=TEXT,
            font=("Inter", 14, "bold"),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 0),
        )

        # Extract the exact string token drawn onto the user's viewport screen
        generated_ref = self.get_refnumber(self.data)

        value = ctk.CTkLabel(
            self.reference_frame,
            text=generated_ref,  # Keeps data points synchronized
            text_color=SUCCESS_GREEN,
            font=("Inter", 28, "bold"),
        )

        value.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15),
        )

        copy_button = ctk.CTkButton(
            self.reference_frame,
            text="",
            image=self.copy_icon,
            width=48,
            height=48,
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=10,
        )

        # Configure lambda passing BOTH the text variable and the button memory reference
        copy_button.configure(
            command=lambda b=copy_button: self._copy(generated_ref, b)
        )

        copy_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20,
        )
        # value = ctk.CTkLabel(
        #     self.reference_frame,
        #     text=self.get_refnumber(self.data),
        #     text_color=SUCCESS_GREEN,
        #     font=("Inter", 28, "bold"),
        # )

        # value.grid(
        #     row=1,
        #     column=0,
        #     sticky="w",
        #     padx=20,
        #     pady=(0, 15),
        # )

        # copy_button = ctk.CTkButton(
        #     self.reference_frame,
        #     text="",
        #     image=self.copy_icon,
        #     width=48,
        #     height=48,
        #     fg_color="#334155",
        #     hover_color="#475569",
        #     corner_radius=10,
        #     command=lambda: self._copy(self.reference_number),
        # )

        # copy_button.grid(
        #     row=0,
        #     column=1,
        #     rowspan=2,
        #     padx=20,
        # )

    # ─────────────────────────────────────────────
    # FILENAME SECTION
    # ─────────────────────────────────────────────

    def _build_filename_section(self):

        self.filename_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=SECTION_BG,
            corner_radius=14,
            border_width=1,
            border_color=BORDER,
            height=90,
        )

        self.filename_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.filename_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.filename_frame,
            text="Clean File Name",
            text_color=TEXT,
            font=("Inter", 14, "bold"),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 0),
        )
        # Extract the exact string token drawn onto the user's viewport screen
        generated_title = self.to_snake_case(self.data["project_name"])

        value = ctk.CTkLabel(
            self.filename_frame,
            text=generated_title,  # Keeps data points synchronized
            text_color=SUCCESS_GREEN,
            font=("Inter", 28, "bold"),
        )

        value.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15),
        )

        copy_button = ctk.CTkButton(
            self.filename_frame,
            text="",
            image=self.copy_icon,
            width=48,
            height=48,
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=10,
        )

        # Configure lambda passing BOTH the text variable and the button memory reference
        copy_button.configure(
            command=lambda b=copy_button: self._copy(generated_title, b)
        )

        copy_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20,
        )

        # value = ctk.CTkLabel(
        #     self.filename_frame,
        #     text=self.to_snake_case(self.data["project_name"]),
        #     text_color=SUCCESS_GREEN,
        #     font=("Inter", 22, "bold"),
        # )

        # value.grid(
        #     row=1,
        #     column=0,
        #     sticky="w",
        #     padx=20,
        #     pady=(0, 15),
        # )

        # copy_button = ctk.CTkButton(
        #     self.filename_frame,
        #     text="",
        #     image=self.copy_icon,
        #     width=48,
        #     height=48,
        #     fg_color="#334155",
        #     hover_color="#475569",
        #     corner_radius=10,
        #     command=lambda: self._copy(self.clean_filename),
        # )

        # copy_button.grid(
        #     row=0,
        #     column=1,
        #     rowspan=2,
        #     padx=20,
        # )

    # ─────────────────────────────────────────────
    # SUCCESS SECTION
    # ─────────────────────────────────────────────

    def _build_success_section(self):

        self.success_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=SUCCESS_BG,
            corner_radius=14,
            border_width=1,
            border_color="#1F5C4D",
            height=70,
        )

        self.success_frame.grid(
            row=2,
            column=0,
            sticky="ew",
        )

        icon = ctk.CTkLabel(
            self.success_frame,
            text="",
            image=self.success_icon,
        )

        icon.pack(
            side="left",
            padx=(18, 10),
            pady=14,
        )

        text_container = ctk.CTkFrame(
            self.success_frame,
            fg_color="transparent",
        )

        text_container.pack(
            side="left",
            pady=12,
        )

        title = ctk.CTkLabel(
            text_container,
            text="Successfully generated!",
            text_color="white",
            font=("Inter", 15, "bold"),
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_container,
            text="This reference number is unique.",
            text_color="#C7F9E5",
            font=("Inter", 12),
        )

        subtitle.pack(anchor="w")

    # ─────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────

    def _build_footer(self):

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=CONTENT_PADX,
            pady=(25, 35),
        )

        self.footer.grid_columnconfigure(0, weight=1)

        self.back_button = make_button(
            master=self.footer,
            text="Back",
            command=self._back,
            variant="primary",
            size="md",
        )

        self.back_button.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.create_button = make_button(
            master=self.footer,
            text="Create Another",
            command=self._dashboard,
            variant="secondary",
            size="md",
        )

        self.create_button.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # ─────────────────────────────────────────────
    # UTILITIES
    # ─────────────────────────────────────────────

    # def _copy(self, value: str):

    #     pyperclip.copy(value)
    # ─────────────────────────────────────────────
    # UTILITIES
    # ─────────────────────────────────────────────

    def _copy(self, value: str, button_widget: ctk.CTkButton):
        """Copies the target text to clipboard and flashes a confirmation state."""
        pyperclip.copy(value)

        # Preserve original state variables to allow safe reversion
        original_text = button_widget.cget("text")
        original_image = button_widget.cget("image")
        original_width = button_widget.cget("width")
        original_fg = button_widget.cget("fg_color")
        original_hover = button_widget.cget("hover_color")

        # Transform button state to indicate success
        button_widget.configure(
            text="Copied!",
            image="",  # Clear the copy icon temporarily
            width=60,  # Slightly widen to safely fit text bounds
            fg_color=SUCCESS_BG,  # Blend with your success green token palette
            hover_color=SUCCESS_BG,  # Prevent hover jitter while text is showing
            text_color=SUCCESS_GREEN,
            font=("Inter", 11, "bold"),
        )

        # Queue up the recovery layout state change after exactly 1500 milliseconds
        self.after(
            1500,
            lambda: button_widget.configure(
                text=original_text,
                image=original_image,
                width=original_width,
                fg_color=original_fg,
                hover_color=original_hover,
                text_color=TEXT,
            ),
        )

    def get_refnumber(self, data: dict) -> None:
        # FILTER DATA TO GET
        hex_chain = secrets.token_hex(2)
        refnumber = f"{data["country_code"]}-{data["sector_code"]}-{data["type_code"]}-{hex_chain.upper()}"
        return refnumber

    def to_snake_case(self, text: str) -> str:
        """
        Converts any string (camelCase, PascalCase, spaces, hyphens) into clean snake_case,
        ensuring every single word has its first letter capitalized (e.g., "John_Doe").
        """
        if not text:
            return ""

        # 1. Handle camelCase/PascalCase: Insert an underscore before any capital letter
        # that is preceded by a lowercase letter or number.
        s1 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

        # 2. Handle consecutive capitals (e.g., "PDFReader" -> "PDF_Reader")
        s2 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s1)

        # 3. Replace spaces, hyphens, and punctuation with a single underscore
        s3 = re.sub(r"[^a-zA-Z0-9]+", "_", s2)

        # 4. Clean up any trailing/leading underscores and split into raw words
        cleaned_string = s3.strip("_")
        words = cleaned_string.split("_")

        # 5. Capitalize the first letter of each individual word and join them back together
        # using the string `.capitalize()` method (safely handles any mixed casing leftover)
        return "_".join(word.capitalize() for word in words if word)

    # ─────────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────────

    def _back(self):

        if self.on_back:
            self.on_back()

    def _dashboard(self):

        if self.on_dashboard:
            self.on_dashboard()


# """
# ================================================================================
# PROJECT:       Monolith Application Engine
# MODULE:        gui.pages.ref_page
# DESCRIPTION:   Generated reference result page.
# AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
# LICENSE:       Proprietary – All rights reserved
# VERSION:       1.1.0
# ================================================================================
# """

# from __future__ import annotations

# import customtkinter as ctk
# from PIL import Image
# import pyperclip

# # ── Local Imports ─────────────────────────────────────────────────────────────
# from gui.widgets.buttons import make_button
# from gui.widgets.stepper import Stepper

# from core.utils.paths import get_asset_path

# from gui.theme.colors import (
#     CARD_BG,
#     TEXT,
#     TEXT_MUTED,
# )

# # ──────────────────────────────────────────────────────────────────────────────
# # DESIGN TOKENS
# # ──────────────────────────────────────────────────────────────────────────────

# CONTENT_PADX = 40

# SUCCESS_GREEN = "#34D399"
# SUCCESS_BG = "#123C36"

# SECTION_BG = "#1E293B"

# BORDER = "#334155"


# class RefPage(ctk.CTkFrame):

#     def __init__(
#         self,
#         master,
#         data: dict,
#         on_back=None,
#         on_create_another=None,
#     ):

#         super().__init__(
#             master,
#             fg_color=CARD_BG,
#         )

#         # ─────────────────────────────────────────
#         # CALLBACKS
#         # ─────────────────────────────────────────

#         self.on_back = on_back
#         self.on_create_another = on_create_another

#         # ─────────────────────────────────────────
#         # DATA
#         # ─────────────────────────────────────────

#         self.data = data

#         # SAFE FALLBACKS
#         self.reference_number = data.get(
#             "reference_number",
#             "MON-000001",
#         )

#         self.clean_filename = data.get(
#             "clean_filename",
#             "generated_document.pdf",
#         )

#         # ─────────────────────────────────────────
#         # PAGE
#         # ─────────────────────────────────────────

#         self.pack(
#             fill="both",
#             expand=True,
#         )

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         # BUILD
#         self._load_icons()

#         self._build_header()
#         self._build_content()
#         self._build_footer()

#     # ─────────────────────────────────────────────
#     # ICONS
#     # ─────────────────────────────────────────────

#     def _load_icons(self):

#         self.copy_icon = ctk.CTkImage(
#             light_image=Image.open(get_asset_path("icons/copy.png")),
#             dark_image=Image.open(get_asset_path("icons/copy.png")),
#             size=(20, 20),
#         )

#         self.success_icon = ctk.CTkImage(
#             light_image=Image.open(get_asset_path("icons/check-circle.png")),
#             dark_image=Image.open(get_asset_path("icons/check-circle.png")),
#             size=(22, 22),
#         )

#     # ─────────────────────────────────────────────
#     # HEADER
#     # ─────────────────────────────────────────────

#     def _build_header(self):

#         self.header_frame = ctk.CTkFrame(
#             self,
#             fg_color="transparent",
#         )

#         self.header_frame.grid(
#             row=0,
#             column=0,
#             sticky="ew",
#             padx=CONTENT_PADX,
#             pady=(30, 25),
#         )

#         self.stepper = Stepper(
#             self.header_frame,
#             steps=[
#                 "Type",
#                 "Details",
#                 "Generated",
#             ],
#             current_step=3,
#         )

#         self.stepper.pack(
#             fill="x",
#         )

#     # ─────────────────────────────────────────────
#     # CONTENT
#     # ─────────────────────────────────────────────

#     def _build_content(self):

#         self.content_frame = ctk.CTkFrame(
#             self,
#             fg_color="transparent",
#         )

#         self.content_frame.grid(
#             row=1,
#             column=0,
#             sticky="nsew",
#             padx=CONTENT_PADX,
#         )

#         self.content_frame.grid_columnconfigure(0, weight=1)

#         self._build_reference_section()
#         self._build_filename_section()
#         self._build_success_section()

#     # ─────────────────────────────────────────────
#     # REFERENCE SECTION
#     # ─────────────────────────────────────────────

#     def _build_reference_section(self):

#         self.reference_frame = ctk.CTkFrame(
#             self.content_frame,
#             fg_color=SECTION_BG,
#             corner_radius=14,
#             border_width=1,
#             border_color=BORDER,
#             height=90,
#         )

#         self.reference_frame.grid(
#             row=0,
#             column=0,
#             sticky="ew",
#             pady=(0, 18),
#         )

#         self.reference_frame.grid_columnconfigure(0, weight=1)

#         title = ctk.CTkLabel(
#             self.reference_frame,
#             text="Reference Number",
#             text_color=TEXT,
#             font=("Inter", 14, "bold"),
#         )

#         title.grid(
#             row=0,
#             column=0,
#             sticky="w",
#             padx=20,
#             pady=(15, 0),
#         )

#         value = ctk.CTkLabel(
#             self.reference_frame,
#             text=self.reference_number,
#             text_color=SUCCESS_GREEN,
#             font=("Inter", 28, "bold"),
#         )

#         value.grid(
#             row=1,
#             column=0,
#             sticky="w",
#             padx=20,
#             pady=(0, 15),
#         )

#         copy_button = ctk.CTkButton(
#             self.reference_frame,
#             text="",
#             image=self.copy_icon,
#             width=48,
#             height=48,
#             fg_color="#334155",
#             hover_color="#475569",
#             corner_radius=10,
#             command=lambda: self._copy(self.reference_number),
#         )

#         copy_button.grid(
#             row=0,
#             column=1,
#             rowspan=2,
#             padx=20,
#         )

#     # ─────────────────────────────────────────────
#     # FILENAME SECTION
#     # ─────────────────────────────────────────────

#     def _build_filename_section(self):

#         self.filename_frame = ctk.CTkFrame(
#             self.content_frame,
#             fg_color=SECTION_BG,
#             corner_radius=14,
#             border_width=1,
#             border_color=BORDER,
#             height=90,
#         )

#         self.filename_frame.grid(
#             row=1,
#             column=0,
#             sticky="ew",
#             pady=(0, 18),
#         )

#         self.filename_frame.grid_columnconfigure(0, weight=1)

#         title = ctk.CTkLabel(
#             self.filename_frame,
#             text="Clean File Name",
#             text_color=TEXT,
#             font=("Inter", 14, "bold"),
#         )

#         title.grid(
#             row=0,
#             column=0,
#             sticky="w",
#             padx=20,
#             pady=(15, 0),
#         )

#         value = ctk.CTkLabel(
#             self.filename_frame,
#             text=self.clean_filename,
#             text_color=SUCCESS_GREEN,
#             font=("Inter", 22, "bold"),
#         )

#         value.grid(
#             row=1,
#             column=0,
#             sticky="w",
#             padx=20,
#             pady=(0, 15),
#         )

#         copy_button = ctk.CTkButton(
#             self.filename_frame,
#             text="",
#             image=self.copy_icon,
#             width=48,
#             height=48,
#             fg_color="#334155",
#             hover_color="#475569",
#             corner_radius=10,
#             command=lambda: self._copy(self.clean_filename),
#         )

#         copy_button.grid(
#             row=0,
#             column=1,
#             rowspan=2,
#             padx=20,
#         )

#     # ─────────────────────────────────────────────
#     # SUCCESS SECTION
#     # ─────────────────────────────────────────────

#     def _build_success_section(self):

#         self.success_frame = ctk.CTkFrame(
#             self.content_frame,
#             fg_color=SUCCESS_BG,
#             corner_radius=14,
#             border_width=1,
#             border_color="#1F5C4D",
#             height=70,
#         )

#         self.success_frame.grid(
#             row=2,
#             column=0,
#             sticky="ew",
#         )

#         icon = ctk.CTkLabel(
#             self.success_frame,
#             text="",
#             image=self.success_icon,
#         )

#         icon.pack(
#             side="left",
#             padx=(18, 10),
#             pady=14,
#         )

#         text_container = ctk.CTkFrame(
#             self.success_frame,
#             fg_color="transparent",
#         )

#         text_container.pack(
#             side="left",
#             pady=12,
#         )

#         title = ctk.CTkLabel(
#             text_container,
#             text="Successfully generated!",
#             text_color="white",
#             font=("Inter", 15, "bold"),
#         )

#         title.pack(anchor="w")

#         subtitle = ctk.CTkLabel(
#             text_container,
#             text="This reference number is unique.",
#             text_color="#C7F9E5",
#             font=("Inter", 12),
#         )

#         subtitle.pack(anchor="w")

#     # ─────────────────────────────────────────────
#     # FOOTER
#     # ─────────────────────────────────────────────

#     def _build_footer(self):

#         self.footer = ctk.CTkFrame(
#             self,
#             fg_color="transparent",
#         )

#         self.footer.grid(
#             row=2,
#             column=0,
#             sticky="ew",
#             padx=CONTENT_PADX,
#             pady=(25, 35),
#         )

#         self.footer.grid_columnconfigure(0, weight=1)

#         self.back_button = make_button(
#             master=self.footer,
#             text="Back to Dashboard",
#             command=self._back,
#             variant="primary",
#             size="md",
#         )

#         self.back_button.grid(
#             row=0,
#             column=0,
#             sticky="w",
#         )

#         self.create_button = make_button(
#             master=self.footer,
#             text="Create Another",
#             command=self._create_another,
#             variant="secondary",
#             size="md",
#         )

#         self.create_button.grid(
#             row=0,
#             column=1,
#             sticky="e",
#         )

#     # ─────────────────────────────────────────────
#     # UTILITIES
#     # ─────────────────────────────────────────────

#     def _copy(self, value: str):

#         pyperclip.copy(value)

#     # ─────────────────────────────────────────────
#     # ACTIONS
#     # ─────────────────────────────────────────────

#     def _back(self):

#         if self.on_back:
#             self.on_back()

#     def _create_another(self):

#         if self.on_create_another:
#             self.on_create_another()
