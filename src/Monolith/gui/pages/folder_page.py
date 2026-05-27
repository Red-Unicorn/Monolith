"""
Folder workflow page example.
"""

from __future__ import annotations

import customtkinter as ctk
from gui.theme.colors import BACKGROUND, TEXT_MUTED, TEXT
from gui.theme.layout import INPUT_HEIGHT, INPUT_WIDTH
from gui.widgets.search_combobox import SearchComboBox
from core.utils.logger import logger
from core.utils.ref_number_generator import get_reference_values


class FolderPage(ctk.CTkFrame):

    def __init__(self, master, on_back=None, on_next=None, on_navigate=None):
        # self.country_values = get_reference_values("countries")
        # self.sector_values = get_reference_values("sectors")
        # self.source_type_values = get_reference_values("source_types")

        self.country_values = list(get_reference_values("countries").keys())
        self.sector_values = list(get_reference_values("sectors").keys())
        self.source_type_values = list(get_reference_values("source_types").keys())

        super().__init__(master, fg_color=BACKGROUND)

        self.on_navigate = on_navigate

        self.on_back = on_back
        self.on_next = on_next

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
            pady=(0, 0),
        )

        self.step_label = ctk.CTkLabel(
            self.header_frame,
            text="STEP 2 OF 3",
            font=("Oswald", 18, "bold"),
            text_color=TEXT_MUTED,
        )
        self.step_label.pack(anchor="w")  # ,pady=(0, 20))

        # self.title_label = ctk.CTkLabel(
        #     self.header_frame,
        #     text="Create Reference Number for:",
        #     font=("PT Sans", 12, "bold"),
        #     text_color=TEXT,
        # )
        # self.title_label.pack(anchor="w")  # , pady=(10, 0))
        # ──────────────────────────────────────────────────────────────────
        # HEADER
        # ──────────────────────────────────────────────────────────────────

        # title = ctk.CTkLabel(
        #     self,
        #     text="STEP 2 OF 3",
        #     font=("Arial", 18, "bold"),
        #     text_color="#94A3B8",
        # )
        # title.pack(anchor="w", padx=40, pady=(30, 10))

        # subtitle = ctk.CTkLabel(
        #     self,
        #     text="Project Information",
        #     font=("Arial", 34, "bold"),
        #     text_color="white",
        # )
        # subtitle.pack(anchor="w", padx=40)

        # ──────────────────────────────────────────────────────────────────
        # FORM AREA
        # ──────────────────────────────────────────────────────────────────

        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.form_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=40,
            pady=30,
        )

        # PROJECT NAME
        # This is an entry place to write the project name
        # project_name = ctk.CTkLabel(
        #     self.form_frame,
        #     text="Project Name",
        #     font=("Arial", 20),
        # )

        # project_name.pack(
        #     anchor="w",
        #     padx=30,
        #     pady=(30, 10),
        # )

        # self.project_entry = ctk.CTkEntry(
        #     self.form_frame,
        #     placeholder_text="Project Name",
        #     width=INPUT_WIDTH,
        #     height=INPUT_HEIGHT,
        # )

        # self.project_entry.pack(
        #     pady=10,
        #     padx=40,
        # )

        # COUNTRY BOX
        country_label = ctk.CTkLabel(
            self.form_frame,
            text="Country",
            font=("Arial", 20),
        )

        country_label.pack(
            anchor="w",
            padx=30,
            pady=(30, 10),
        )

        self.country_widget = SearchComboBox(
            self.form_frame,
            values=self.country_values,
            command=lambda code: self.verify_country_output(code),
        )

        self.country_widget.pack(
            fill="x",
            padx=30,
            pady=(0, 20),
        )
        # self.country_search = ctk.CTkEntry(
        #     self.form_frame,
        #     placeholder_text="Search country...",
        # )

        # self.country_search.pack(fill="x", padx=30)

        # self.country_combobox = ctk.CTkComboBox(
        #     self.form_frame,
        #     values=self.country_values,
        #     height=45,
        # )

        # self.country_combobox.pack(
        #     fill="x",
        #     padx=30,
        # )
        # project_label = ctk.CTkLabel(
        #     self.form_frame,
        #     text="Project Name",
        #     font=("Arial", 20),
        # )
        # project_label.pack(anchor="w", padx=30, pady=(30, 10))

        # self.project_entry = ctk.CTkEntry(
        #     self.form_frame,
        #     height=60,
        #     font=("Arial", 22),
        # )
        # self.project_entry.pack(fill="x", padx=30)

        # # PROJECT TYPE

        # type_label = ctk.CTkLabel(
        #     self.form_frame,
        #     text="Project Type",
        #     font=("Arial", 20),
        # )
        # type_label.pack(anchor="w", padx=30, pady=(30, 10))

        # self.project_type = ctk.CTkComboBox(
        #     self.form_frame,
        #     values=[
        #         "Internal",
        #         "Client",
        #         "Research",
        #     ],
        #     height=60,
        #     font=("Arial", 22),
        # )
        # self.project_type.pack(fill="x", padx=30)

        # # ACTIVE CHECKBOX

        # self.active_checkbox = ctk.CTkCheckBox(
        #     self.form_frame,
        #     text="Mark as Active",
        #     font=("Arial", 20),
        # )
        # self.active_checkbox.pack(anchor="w", padx=30, pady=30)

        # # ──────────────────────────────────────────────────────────────────
        # # FOOTER NAVIGATION
        # # ──────────────────────────────────────────────────────────────────

        # footer = ctk.CTkFrame(self, fg_color="transparent")
        # footer.pack(fill="x", padx=40, pady=(0, 30))

        # back_button = ctk.CTkButton(
        #     footer,
        #     text="BACK",
        #     width=180,
        #     height=60,
        #     command=self._back,
        # )
        # back_button.pack(side="left")

        # next_button = ctk.CTkButton(
        #     footer,
        #     text="NEXT",
        #     width=180,
        #     height=60,
        #     fg_color="#2563EB",
        #     command=self._next,
        # )
        # next_button.pack(side="right")

    def verify_country_output(self, selected_code):
        print(f"🔥 DEBUGLOG: Country selected! Next phase value is: {selected_code}")
        print(f"Datatype: {type(selected_code)} | Length: {len(selected_code)}")

    def _back(self):
        if self.on_back:
            self.on_back()

    def _next(self):
        data = {
            "project_name": self.project_entry.get(),
            "project_type": self.project_type.get(),
            "active": self.active_checkbox.get(),
        }

        print(data)

        if self.on_next:
            self.on_next(data)
