"""
Project workflow page example.
"""

from __future__ import annotations

import customtkinter as ctk


class ProjectPage(ctk.CTkFrame):

    def __init__(self, master, on_back=None, on_next=None):
        super().__init__(master, fg_color="#0F172A")

        self.on_back = on_back
        self.on_next = on_next

        self.pack(fill="both", expand=True)

        # ──────────────────────────────────────────────────────────────────
        # HEADER
        # ──────────────────────────────────────────────────────────────────

        title = ctk.CTkLabel(
            self,
            text="STEP 2 OF 3",
            font=("Arial", 18, "bold"),
            text_color="#94A3B8",
        )
        title.pack(anchor="w", padx=40, pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Project Information",
            font=("Arial", 34, "bold"),
            text_color="white",
        )
        subtitle.pack(anchor="w", padx=40)

        # ──────────────────────────────────────────────────────────────────
        # FORM AREA
        # ──────────────────────────────────────────────────────────────────

        form_frame = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=20,
        )
        form_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30,
        )

        # PROJECT NAME

        project_label = ctk.CTkLabel(
            form_frame,
            text="Project Name",
            font=("Arial", 20),
        )
        project_label.pack(anchor="w", padx=30, pady=(30, 10))

        self.project_entry = ctk.CTkEntry(
            form_frame,
            height=60,
            font=("Arial", 22),
        )
        self.project_entry.pack(fill="x", padx=30)

        # PROJECT TYPE

        type_label = ctk.CTkLabel(
            form_frame,
            text="Project Type",
            font=("Arial", 20),
        )
        type_label.pack(anchor="w", padx=30, pady=(30, 10))

        self.project_type = ctk.CTkComboBox(
            form_frame,
            values=[
                "Internal",
                "Client",
                "Research",
            ],
            height=60,
            font=("Arial", 22),
        )
        self.project_type.pack(fill="x", padx=30)

        # ACTIVE CHECKBOX

        self.active_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Mark as Active",
            font=("Arial", 20),
        )
        self.active_checkbox.pack(anchor="w", padx=30, pady=30)

        # ──────────────────────────────────────────────────────────────────
        # FOOTER NAVIGATION
        # ──────────────────────────────────────────────────────────────────

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=40, pady=(0, 30))

        back_button = ctk.CTkButton(
            footer,
            text="BACK",
            width=180,
            height=60,
            command=self._back,
        )
        back_button.pack(side="left")

        next_button = ctk.CTkButton(
            footer,
            text="NEXT",
            width=180,
            height=60,
            fg_color="#2563EB",
            command=self._next,
        )
        next_button.pack(side="right")

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