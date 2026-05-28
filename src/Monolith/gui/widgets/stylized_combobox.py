from __future__ import annotations

import customtkinter as ctk

INPUT_BG = "#1E293B"
BORDER = "#334155"
TEXT = "#E5E7EB"
TEXT_MUTED = "#94A3B8"


class StyledComboBox(ctk.CTkComboBox):

    def __init__(
        self,
        master,
        values,
        width=None,
        height=48,
        **kwargs,
    ):

        super().__init__(
            master,
            values=values,
            width=width,
            height=height,
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            button_color=INPUT_BG,
            button_hover_color=INPUT_BG,
            dropdown_fg_color=INPUT_BG,
            dropdown_hover_color="#273449",
            dropdown_text_color=TEXT,
            text_color=TEXT,
            font=("Inter", 14),
            corner_radius=10,
            state="readonly",
            **kwargs,
        )

        self.set(values[0] if values else "")
