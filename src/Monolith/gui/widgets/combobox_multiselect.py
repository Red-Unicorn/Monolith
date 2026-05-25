"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.widgets.combobox_multiselect
DESCRIPTION:   Enterprise combobox component with real-time text filtering
               and persistent multi-selection checkbox matrices.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       1.1.0
================================================================================
"""

from __future__ import annotations
from typing import Any, List, Dict, Optional
import customtkinter as ctk

# ── Local Design System Tokens ────────────────────────────────────────────────
from gui.theme.colors import CARD_HOVER, RU_BLUE, RU, TEXT, BORDER, TEXT_SECONDARY

__all__ = ["CTkComboboxMultiSelect"]


class CTkComboboxMultiSelect(ctk.CTkFrame):
    """
    Searchable text combobox displaying dynamic scrolling checklist sheets.
    """

    def __init__(
        self,
        master: Any,
        options: List[str],
        default_placeholder: str = "Search & Select Options...",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent")

        self.options: List[str] = options
        self.placeholder: str = default_placeholder
        self.is_dropped: bool = False

        # Track persistent Boolean selections for every item in the master List
        self.variables: Dict[str, ctk.BooleanVar] = {
            opt: ctk.BooleanVar(value=False) for opt in options
        }
        # Dictionary tracking the physical checkbox row element objects
        self.checkbox_widgets: Dict[str, ctk.CTkCheckBox] = {}

        # ── 1. THE SEARCHABLE COMBOBOX INPUT FIELD ────────────────────────────
        # Serves as both the user query input text area and the menu toggle anchor
        self.search_var: ctk.StringVar = ctk.StringVar()
        self.search_var.trace_add("write", self._execute_live_filter)

        self.entry_field: ctk.CTkEntry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text=self.placeholder,
            height=36,
            fg_color=CARD_HOVER,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=TEXT_SECONDARY,
        )
        self.entry_field.pack(fill="x", expand=True)

        # Bind click triggers directly into input field bounding surfaces
        self.entry_field.bind("<Button-1>", lambda _: self._open_dropdown())

        # ── 2. THE FLOATING COMPONENT DROPDOWN CONTAINER ──────────────────────
        self.dropdown_window: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(
            self, fg_color=CARD_HOVER, border_width=1, border_color=BORDER, height=140
        )

        # ── 3. GENERATE PERSISTENT CHECKBOX ENTRIES ───────────────────────────
        for option in self.options:
            cb = ctk.CTkCheckBox(
                self.dropdown_window,
                text=option,
                variable=self.variables[option],
                fg_color=RU,
                hover_color=RU_BLUE,
                text_color=TEXT,
                command=self._refresh_display_state,
                checkbox_height=18,
                checkbox_width=18,
                font=("Inter", 12, "normal"),
            )
            # Retain object instances to toggle packaging configurations on filter cycles
            self.checkbox_widgets[option] = cb
            cb.pack(anchor="w", fill="x", padx=10, pady=5)

    def _open_dropdown(self) -> None:
        """Mounts scrolling checklist frame sheet maps directly below text inputs."""
        if not self.is_dropped:
            self.dropdown_window.pack(fill="x", pady=(4, 0))
            self.is_dropped = True

            # Flush entry text to reveal all baseline choices when clicked open
            if self.search_var.get() == self._get_summary_string():
                self.search_var.set("")

    def _close_dropdown(self) -> None:
        """Unmounts checkbox arrays and flushes text summaries to the interface."""
        if self.is_dropped:
            self.dropdown_window.pack_forget()
            self.is_dropped = False
            self.search_var.set(self._get_summary_string())

    def _execute_live_filter(self, *args: Any) -> None:
        """
        Evaluates string inputs and matches item arrays.
        """
        # Safety bypass check: Skip filtering if the input matches our generated summary string
        current_query = self.search_var.get()
        if current_query == self._get_summary_string() or not self.is_dropped:
            return

        # Simple lowercase sub-string lookup
        query_normalized = current_query.strip().lower()

        for option, widget in self.checkbox_widgets.items():
            if not query_normalized or query_normalized in option.lower():
                # Remount matching options onto the scrollable frame layout track
                widget.pack(anchor="w", fill="x", padx=10, pady=5)
            else:
                # Remove non-matching items from view without breaking their selection state
                widget.pack_forget()

    def _get_summary_string(self) -> str:
        """Generates dynamic string mappings representing current selection weights."""
        checked_items = self.get_selected()
        if not checked_items:
            return ""
        if len(checked_items) <= 2:
            return ", ".join(checked_items)
        return f"{len(checked_items)} Environments Selected"

    def _refresh_display_state(self) -> None:
        """Updates internal states without breaking focus blocks."""
        # Keeps selection strings synchronized behind user clicks
        pass

    def get_selected(self) -> List[str]:
        """Returns flat List array representing currently checked text values."""
        return [opt for opt, var in self.variables.items() if var.get()]

    def set_selected(self, values: List[str]) -> None:
        """Programmatically forces toggle assignments based on explicit array inputs."""
        for opt, var in self.variables.items():
            var.set(opt in values)
        self.search_var.set(self._get_summary_string())
