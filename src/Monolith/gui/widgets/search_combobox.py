from __future__ import annotations

import customtkinter as ctk
from PIL import Image
from core.utils.misc import country_to_iso2, country_to_iso3
from core.utils.paths import get_asset_path


class SearchComboBox(ctk.CTkFrame):
    """
    Searchable combobox widget with placeholder text, a dedicated dropdown arrow,
    and returns ISO-2 country codes upon extraction.
    """

    def __init__(
        self,
        master,
        values: list[str],
        width: int = 300,
        height: int = 40,
        max_results: int = 8,
        command=None,
        **kwargs,
    ):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)

        self.values = values
        self.filtered_values = []
        self.command = command
        self.max_results = max_results

        # Internal state tracking variables
        self.dropdown_window = None
        self.flag_images = []
        self.selected_country_code = ""  # Strictly holds the clean ISO-2 string
        self.placeholder_text = "Type any country"

        # ─────────────────────────────────────────────────────────────
        # INPUT CONTAINER AREA (Houses elements horizontally)
        # ─────────────────────────────────────────────────────────────
        self.input_container = ctk.CTkFrame(
            self,
            width=width,
            height=height,
            fg_color="#1D2A3A",
            border_color="#334155",
            border_width=1,
            corner_radius=6,
        )
        self.input_container.pack(fill="x")
        self.input_container.pack_propagate(False)

        # Static Flag Display Label (Left side)
        self.input_flag_label = ctk.CTkLabel(self.input_container, text="", width=0)
        self.input_flag_label.pack(side="left", padx=(0, 0))

        # Core Text Entry Field
        self.entry = ctk.CTkEntry(
            self.input_container,
            height=height - 4,
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            text_color="#94A3B8",  # Initial placeholder color state
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(2, 4))

        # Insert the initial placeholder text structure
        self.entry.insert(0, self.placeholder_text)

        # Dropdown Arrow Indicator Toggle Button (Right side)
        self.arrow_button = ctk.CTkButton(
            self.input_container,
            text="▼",
            width=28,
            height=height - 4,
            fg_color="transparent",
            text_color="#94A3B8",
            hover_color="#2B394A",
            font=("Inter", 11),
            command=self._toggle_dropdown_arrow,
        )
        self.arrow_button.pack(side="right", padx=(0, 4))

        # ─────────────────────────────────────────────────────────────
        # EVENT BINDINGS
        # ─────────────────────────────────────────────────────────────
        self.entry.bind("<KeyRelease>", self._filter_values)
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

    # ─────────────────────────────────────────────────────────────────
    # PLACEHOLDER ACTIONS
    # ─────────────────────────────────────────────────────────────────
    def _clear_placeholder(self, event=None):
        """Clears default text instantly when the user clicks inside to type."""
        current_text = self.entry.get()
        if current_text == self.placeholder_text:
            self.entry.delete(0, "end")
            self.entry.configure(
                text_color="#FFFFFF"
            )  # Switch to bright active text color

    def _restore_placeholder(self, event=None):
        """Restores placeholder string if the user leaves the box empty."""
        # Slight deferral loop allows click-selections to complete before hiding elements
        self.after(150, self._check_and_restore)

    def _check_and_restore(self):
        if not self.entry.get().strip():
            self.entry.delete(0, "end")
            self.entry.insert(0, self.placeholder_text)
            self.entry.configure(text_color="#94A3B8")
            self.input_flag_label.pack_forget()  # Unpack the flag if empty
            self.selected_country_code = ""
        self._hide_dropdown()

    # ─────────────────────────────────────────────────────────────────
    # DROPDOWN TOGGLE CONTROL
    # ─────────────────────────────────────────────────────────────────
    def _toggle_dropdown_arrow(self):
        """Opens full list dropdown when clicking the arrow, or hides it if open."""
        if self.dropdown_window:
            self._hide_dropdown()
        else:
            self.entry.focus_set()
            # If entry contains placeholder text, pass all unfiltered options down
            current_val = self.entry.get()
            if current_val == self.placeholder_text or not current_val.strip():
                self.filtered_values = self.values[: self.max_results]
            else:
                self.filtered_values = [
                    v
                    for v in self.values
                    if v.lower().startswith(current_val.lower().strip())
                ][: self.max_results]

            if self.filtered_values:
                self._show_dropdown()

    # ─────────────────────────────────────────────────────────────────
    # FILTER VALUES
    # ─────────────────────────────────────────────────────────────────
    def _filter_values(self, event=None):
        query = self.entry.get().lower().strip()

        if not query or query == self.placeholder_text.lower():
            self.filtered_values = []
            self._hide_dropdown()
            return

        self.filtered_values = [
            value for value in self.values if value.lower().startswith(query)
        ]
        self.filtered_values = self.filtered_values[: self.max_results]

        if self.filtered_values:
            self._show_dropdown()
        else:
            self._hide_dropdown()

    # ─────────────────────────────────────────────────────────────────
    # DROPDOWN LAYOUT ENGINE
    # ─────────────────────────────────────────────────────────────────
    def _show_dropdown(self):
        self._hide_dropdown()

        self.dropdown_window = ctk.CTkToplevel(self)
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.attributes("-topmost", True)

        x = self.input_container.winfo_rootx()
        y = self.input_container.winfo_rooty() + self.input_container.winfo_height()
        width = self.input_container.winfo_width()

        self.dropdown_window.geometry(f"{width}x180+{x}+{y}")

        self.results_frame = ctk.CTkScrollableFrame(
            self.dropdown_window, fg_color="#1E293B"
        )
        self.results_frame.pack(fill="both", expand=True)

        self._update_results()

    def _hide_dropdown(self):
        if self.dropdown_window:
            try:
                self.dropdown_window.destroy()
            except Exception:
                pass
            self.dropdown_window = None

    def _update_results(self):
        if not hasattr(self, "results_frame"):
            return

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for value in self.filtered_values:
            row = ctk.CTkFrame(
                self.results_frame, fg_color="transparent", corner_radius=6
            )
            row.pack(fill="x", padx=4, pady=2)

            row.bind("<Enter>", lambda e, r=row: r.configure(fg_color="#334155"))
            row.bind("<Leave>", lambda e, r=row: r.configure(fg_color="transparent"))

            iso2 = country_to_iso2(value)
            flag_image = self._load_flag(iso2)
            self.flag_images.append(flag_image)

            flag_label = ctk.CTkLabel(row, text="", image=flag_image, width=24)
            flag_label.pack(side="left", padx=(10, 4), pady=6)

            label = ctk.CTkLabel(
                row, text=value, font=("Inter", 14), anchor="w", text_color="#FFFFFF"
            )
            label.pack(side="left", padx=6, pady=8)

            # Click selection mappings
            row.bind("<Button-1>", lambda e, v=value: self._select_value(v))
            label.bind("<Button-1>", lambda e, v=value: self._select_value(v))
            flag_label.bind("<Button-1>", lambda e, v=value: self._select_value(v))

    def _load_flag(self, code: str):
        path = get_asset_path(f"flags/png/{code.lower()}.png")
        return ctk.CTkImage(Image.open(path), size=(20, 14))

    # ─────────────────────────────────────────────────────────────────
    # SELECT VALUE
    # ─────────────────────────────────────────────────────────────────
    def _select_value(self, value: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.entry.configure(text_color="#FFFFFF")

        # Extract code directly into internal tracking slot state variable
        iso2 = country_to_iso2(value).upper()
        self.selected_country_code = country_to_iso3(value).upper()
        # Render internal inline flag element close to text layout border
        flag_image = self._load_flag(iso2)
        self.input_flag_label.configure(image=flag_image, width=24)
        self.input_flag_label.pack(side="left", padx=(8, 0))

        self._hide_dropdown()

        if self.command:

            self.command(
                self.selected_country_code
            )  # Bubbles the code upstream instead of full string name

    # ─────────────────────────────────────────────────────────────────
    # PUBLIC API LAYERS
    # ─────────────────────────────────────────────────────────────────
    def get(self) -> str:
        """Returns the clean ISO-2 country code (e.g., 'FR') instead of full text string."""
        return self.selected_country_code

    def set(self, value: str):
        """Allows code-driven updates via full name strings."""
        self._select_value(value)
