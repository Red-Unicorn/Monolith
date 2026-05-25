"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.wizard_page
DESCRIPTION:   Reusable stateful framework controlling dynamic question block updates.
               Handles local user data caches, interface redraw loops, and dispatches
               terminal evaluation schemas back to high-level system controllers.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       2.0.4
================================================================================
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import customtkinter as ctk

# ── Local Design Tokens Mapping Injections ────────────────────────────────────
from gui.theme.colors import *

__all__ = ["WizardPage"]


class WizardPage(ctk.CTkFrame):
    """
    Dynamic state tracking execution canvas layer drawing customized interactive questionnaire paths.
    """

    def __init__(
        self,
        master: Any,
        wizard_title: str,
        steps: List[Dict[str, Any]],
        on_complete_callback: Any,
        on_cancel_callback: Any,
    ) -> None:
        """
        Instantiate container grid weights and establish reactive layout frameworks.

        Parameters
        ----------
        master : Any
            The immediate hosting element canvas frame.
        wizard_title : str
            The tracking string headline displayed inside the primary view header block.
        steps : list[dict[str, Any]]
            Array of dictionary objects specifying runtime questions and layouts.
        on_complete_callback : Any
            Executable method pointer fired upon successful resolution of final steps.
        on_cancel_callback : Any
            Executable method pointer tracking exit loop structural sequences.
        """
        # Forward frame state rules safely to the core Tkinter layout pipeline
        super().__init__(master, fg_color="transparent")

        # Initialize internal state registry dictionaries
        self.steps: List[Dict[str, Any]] = steps
        self.current_step: int = 0
        self.user_responses: Dict[int, Any] = {}
        self.on_complete: Any = on_complete_callback
        self.on_cancel: Any = on_cancel_callback

        # Element pointer tracking fields
        self.input_widget: Optional[
            ctk.CTkFrame | ctk.CTkOptionMenu | ctk.CTkCheckBox
        ] = None

        # ── GRID MATRIX SPACE DISTRIBUTION ────────────────────────────────────
        # Configures structural row expansion maps so inputs float centered.
        self.grid_rowconfigure(
            0, weight=0
        )  # Row 0: Metadata Tracking Header Label Block
        self.grid_rowconfigure(
            1, weight=1
        )  # Row 1: Central Interactive Input Container
        self.grid_rowconfigure(2, weight=0)  # Row 2: Navigation Control Bar Footprint
        self.grid_columnconfigure(0, weight=1)

        # ── HEADER ELEMENT PACKS (ROW 0) ──────────────────────────────────────
        # Displays wizard context and progress string fractions tracking steps.
        self.header_label: ctk.CTkLabel = ctk.CTkLabel(
            self, text=wizard_title.upper(), font=("Inter", 20, "bold"), text_color=TEXT
        )
        self.header_label.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w")

        self.progress_label: ctk.CTkLabel = ctk.CTkLabel(
            self, text="", font=("Inter", 12, "normal"), text_color=TEXT_SECONDARY
        )
        self.progress_label.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="e")

        # ── CENTRAL CANVAS BOUNDARY CONTAINER (ROW 1) ─────────────────────────
        # Isolates active step fields behind an styled panel layout structure.
        self.canvas_frame: ctk.CTkFrame = ctk.CTkFrame(
            self, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER
        )
        self.canvas_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # Core prompt typography
        self.lbl_question: ctk.CTkLabel = ctk.CTkLabel(
            self.canvas_frame,
            text="",
            font=("Inter", 16, "bold"),
            text_color=TEXT,
            wraplength=500,
            justify="left",
        )
        self.lbl_question.pack(anchor="w", padx=30, pady=(30, 5))

        # Contextual metadata descriptors
        self.lbl_desc: ctk.CTkLabel = ctk.CTkLabel(
            self.canvas_frame,
            text="",
            font=("Inter", 12, "normal"),
            text_color=TEXT_SECONDARY,
            wraplength=500,
            justify="left",
        )
        self.lbl_desc.pack(anchor="w", padx=30, pady=(0, 25))

        # Local structural target frame hosting the dynamic input element
        self.input_container: ctk.CTkFrame = ctk.CTkFrame(
            self.canvas_frame, fg_color="transparent"
        )
        self.input_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # ── FOOTER NAVIGATION CONTROLS (ROW 2) ────────────────────────────────
        # Mounts functional execution steps allowing users to step backward or forward.
        self.footer_bar: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_bar.grid(row=2, column=0, padx=30, pady=(15, 30), sticky="ew")

        # Direct exit sequence trigger
        self.btn_cancel: ctk.CTkButton = ctk.CTkButton(
            self.footer_bar,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            hover_color=CARD_HOVER,
            command=self.on_cancel,
        )
        self.btn_cancel.pack(side="left")

        # Move forward sequence trigger
        self.btn_next: ctk.CTkButton = ctk.CTkButton(
            self.footer_bar,
            text="Next",
            fg_color=RU_BLUE,
            hover_color=RU,
            text_color=TEXT,
            command=self._next_step,
        )
        self.btn_next.pack(side="right", padx=(10, 0))

        # Step backward sequence trigger (Hidden dynamically on page index 0)
        self.btn_back: ctk.CTkButton = ctk.CTkButton(
            self.footer_bar,
            text="Back",
            fg_color="transparent",
            text_color=TEXT_SECONDARY,
            hover_color=CARD_HOVER,
            command=self._back_step,
        )
        self.btn_back.pack(side="right")

        # Execute initial interface print loop pass
        self._render_current_step()

    def _render_current_step(self) -> None:
        """
        Cleans up previous variable bindings and draws current active input layouts.
        """
        # ── SUB-ROUTE A: UPDATE BUTTON TEXT AND VISIBILITY STATES ─────────────
        if self.current_step == 0:
            self.btn_back.pack_forget()  # Remove element footprint from visibility array
        else:
            self.btn_back.pack(side="right")

        # Re-label final submission node to provide explicit user feedback
        if self.current_step == len(self.steps) - 1:
            self.btn_next.configure(text="Finish Setup")
        else:
            self.btn_next.configure(text="Next")

        # ── SUB-ROUTE B: ASSIGN STEP CONTENT DATA METADATA ───────────────────
        step_data = self.steps[self.current_step]
        self.progress_label.configure(
            text=f"Step {self.current_step + 1} of {len(self.steps)}"
        )
        self.lbl_question.configure(text=step_data["question"])
        self.lbl_desc.configure(text=step_data["description"])

        # ── SUB-ROUTE C: DESTROY OUTDATED COMPONENT ARRAYS ────────────────────
        if self.input_widget:
            self.input_widget.destroy()

        # Extract existing entry state maps if user is tracking backward from history loops
        prev_saved_value = self.user_responses.get(self.current_step, None)
        widget_type = step_data["type"]

        # ── SUB-ROUTE D: EXECUTE INPUT-TYPE GENERATION VECTOR ────────────────
        if widget_type == "radio":
            self.input_widget = ctk.CTkFrame(
                self.input_container, fg_color="transparent"
            )
            self.input_widget.pack(fill="both", expand=True)

            # Setup data value structures and link defaults
            self.radio_var = ctk.StringVar(
                value=prev_saved_value or step_data["options"][0]
            )

            for option in step_data["options"]:
                rb = ctk.CTkRadioButton(
                    self.input_widget,
                    text=option,
                    variable=self.radio_var,
                    value=option,
                    fg_color=RU,
                    hover_color=PRIMARY_HOVER,
                    text_color=TEXT,
                )
                rb.pack(anchor="w", pady=6)

        elif widget_type == "dropdown":
            self.dropdown_var = ctk.StringVar(
                value=prev_saved_value or step_data["options"][0]
            )
            self.input_widget = ctk.CTkOptionMenu(
                self.input_container,
                variable=self.dropdown_var,
                values=step_data["options"],
                fg_color=CARD_HOVER,
                button_color=RU_BLUE,
                button_hover_color=RU,
            )
            self.input_widget.pack(anchor="w", pady=10)

        elif widget_type == "checkbox":
            self.check_var = ctk.BooleanVar(
                value=prev_saved_value if prev_saved_value is not None else False
            )
            self.input_widget = ctk.CTkCheckBox(
                self.input_container,
                text=step_data["label"],
                variable=self.check_var,
                fg_color=RU,
                hover_color=PRIMARY_HOVER,
                text_color=TEXT,
            )
            self.input_widget.pack(anchor="w", pady=10)

    def _save_current_response(self) -> None:
        """
        Extract active parameters from widget components and store them in memory.
        """
        widget_type = self.steps[self.current_step]["type"]
        if widget_type == "radio":
            self.user_responses[self.current_step] = self.radio_var.get()
        elif widget_type == "dropdown":
            self.user_responses[self.current_step] = self.dropdown_var.get()
        elif widget_type == "checkbox":
            self.user_responses[self.current_step] = self.check_var.get()

    def _next_step(self) -> None:
        """
        Advance the questionnaire matrix or dispatch structural final payloads.
        """
        self._save_current_response()
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._render_current_step()
        else:
            # All steps passed, commit state dictionaries to main controller pipelines
            self.on_complete(self.user_responses)

    def _back_step(self) -> None:
        """
        Retreat backward one index phase while keeping current options saved in memory.
        """
        if self.current_step > 0:
            self._save_current_response()
            self.current_step -= 1
            self._render_current_step()
