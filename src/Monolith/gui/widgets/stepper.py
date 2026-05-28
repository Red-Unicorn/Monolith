"""
Reusable enterprise workflow stepper.
"""

from __future__ import annotations

import customtkinter as ctk
from gui.theme.layout import STEP_SIZE
from gui.theme.colors import ACCENT, TEXT, TEXT_MUTED, LINE, PRIMARY_RED


class Stepper(ctk.CTkFrame):

    def __init__(
        self,
        master,
        steps: list[str],
        current_step: int = 1,
        *args,
        **kwargs,
    ):

        super().__init__(
            master,
            fg_color="transparent",
            *args,
            **kwargs,
        )

        self.steps = steps
        self.current_step = current_step

        self._build()

    # ─────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────

    def _build(self):

        total = len(self.steps)

        for i in range(total):

            self.grid_columnconfigure(i * 2, weight=0)

            if i < total - 1:
                self.grid_columnconfigure((i * 2) + 1, weight=1)

        for index, title in enumerate(self.steps):

            step_number = index + 1

            active = step_number == self.current_step

            step = self._create_step(
                number=str(step_number),
                text=title,
                active=active,
            )

            step.grid(
                row=0,
                column=index * 2,
                sticky="w",
            )

            # CONNECTOR LINE

            if index < total - 1:

                line = ctk.CTkFrame(
                    self,
                    height=2,
                    fg_color=LINE,
                    corner_radius=100,
                )

                line.grid(
                    row=0,
                    column=(index * 2) + 1,
                    sticky="ew",
                    padx=22,
                )

    # ─────────────────────────────────────────────
    # STEP
    # ─────────────────────────────────────────────

    def _create_step(
        self,
        number: str,
        text: str,
        active: bool = False,
    ):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        # PERFECT CIRCLE

        circle = ctk.CTkFrame(
            frame,
            width=STEP_SIZE,
            height=STEP_SIZE,
            corner_radius=STEP_SIZE // 2,
            fg_color=PRIMARY_RED if active else "#CBD5E1",  # ACCENT
            border_color=TEXT,
            border_width=2,
        )

        circle.pack_propagate(False)

        circle.pack(
            side="left",
        )

        # CENTERED NUMBER

        number_label = ctk.CTkLabel(
            circle,
            text=number,
            font=("Inter", 15, "bold"),
            text_color="white" if active else "#111827",
        )

        number_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        # TITLE

        title_label = ctk.CTkLabel(
            frame,
            text=text,
            font=("Inter", 15, "bold"),
            text_color=ACCENT if active else TEXT_MUTED,
        )

        title_label.pack(
            side="left",
            padx=(12, 0),
        )

        return frame
