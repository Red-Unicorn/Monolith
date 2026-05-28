# gui/utils/labels.py

from __future__ import annotations
import customtkinter as ctk

from gui.theme.colors import BUTTON_SECONDARY, TEXT


def make_required_label(
    master,
    text: str,
    required: bool = True,
):
    """
    Create a label with optional red asterisk.
    """

    frame = ctk.CTkFrame(
        master,
        fg_color="transparent",
    )

    label = ctk.CTkLabel(
        frame,
        text=text,
        font=("Inter", 12),
        text_color=TEXT,  # "#E2E8F0",
    )

    label.pack(
        side="left",
    )

    if required:

        star = ctk.CTkLabel(
            frame,
            text="*",
            font=("Inter", 13, "bold"),
            text_color="#C72E2E",
        )

        star.pack(
            side="left",
        )

    return frame
