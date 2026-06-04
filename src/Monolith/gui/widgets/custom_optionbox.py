from __future__ import annotations

import customtkinter as ctk
from PIL import Image


class CustomOptionMenu(ctk.CTkFrame):
    """
    Customized OptionMenu styled selection widget.
    Maintains design aesthetics while restricting input to strict list selection.
    """

    def __init__(
        self,
        master,
        values: list[str],
        width: int = 300,
        height: int = 42,
        max_results: int = 200,
        placeholder_text: str = "Select",
        command=None,
        image_provider=None,
        value_mapper=None,
        corner_radius: int = 8,
        dropdown_height: int = 220,
        **kwargs,
    ):
        self.corner_radius = kwargs.pop("corner_radius", 8)
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)

        # DATA MAPPINGS
        self.values = values
        self.filtered_values = values  # Always defaults to the full choice array
        self.command = command
        self.image_provider = image_provider
        self.value_mapper = value_mapper
        self.corner_radius = corner_radius
        self.max_results = max_results
        self.dropdown_height = dropdown_height
        self.placeholder_text = placeholder_text
        self.selected_value = ""

        self.dropdown_window = None
        self.image_cache = []

        # ─────────────────────────────────────────
        # MAIN CONTAINER
        # ─────────────────────────────────────────
        self.input_container = ctk.CTkFrame(
            self,
            width=width,
            height=height,
            fg_color="#1E293B",
            border_color="#334155",
            border_width=0,  # Set to 1 to cleanly frame the locked option field
            corner_radius=self.corner_radius,
        )
        self.input_container.pack(fill="x", pady=1)
        self.input_container.pack_propagate(False)

        # LEFT IMAGE
        self.left_image_label = ctk.CTkLabel(
            self.input_container,
            text="",
            width=0,
        )
        self.left_image_label.pack(side="left", padx=(10, 0))

        # ENTRY (Conformed to act as a strict Read-Only Selection Display Box)
        self.entry = ctk.CTkEntry(
            self.input_container,
            fg_color="transparent",
            bg_color="transparent",
            border_width=0,
            corner_radius=8,
            height=height - 4,
            text_color="#94A3B8",
            font=("Inter", 14),
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(4, 4))

        # Inject placeholder text first, then lock the entry down
        self.entry.insert(0, self.placeholder_text)
        self.entry.configure(state="readonly")

        # DROPDOWN ARROW BUTTON
        self.arrow_button = ctk.CTkButton(
            self.input_container,
            text="▼",
            width=34,
            height=height - 6,
            fg_color="transparent",
            hover_color="#273449",
            text_color="#94A3B8",
            font=("Inter", 12, "bold"),
            corner_radius=self.corner_radius,
            command=self._toggle_dropdown,
        )
        self.arrow_button.pack(side="right", padx=(0, 4))

        # UNIFIED SELECTION CLICK TRIGGERS
        # Clicking anywhere on the text field or container wrapper triggers the dropdown list
        self.input_container.bind("<Button-1>", lambda e: self._toggle_dropdown())
        self.entry.bind("<Button-1>", lambda e: self._toggle_dropdown())
        self.left_image_label.bind("<Button-1>", lambda e: self._toggle_dropdown())

    # ─────────────────────────────────────────
    # DROPDOWN CONTROL ENGINE
    # ─────────────────────────────────────────
    def _toggle_dropdown(self):
        if self.dropdown_window:
            self._hide_dropdown()
        else:
            self._open_dropdown()

    def _open_dropdown(self, event=None):
        # Always slice options cleanly up to the allowed max bounds limits
        self.filtered_values = self.values[: self.max_results]
        if self.filtered_values:
            self._show_dropdown()

    # ─────────────────────────────────────────
    # DROPDOWN WINDOW GEOMETRY CONTROL
    # ─────────────────────────────────────────
    def _show_dropdown(self):
        if not self.filtered_values:
            self._hide_dropdown()
            return

        self.update_idletasks()

        if not self.dropdown_window:
            self.dropdown_window = ctk.CTkToplevel(self)
            self.dropdown_window.overrideredirect(True)
            self.dropdown_window.attributes("-topmost", True)

        # ─── DYNAMIC HEIGHT CALCULATION WITH A 10-ITEM CAP ───
        # 1. Count how many items we are actually trying to display
        actual_items_count = len(self.filtered_values)

        # 2. Calculate the perfect height for the current items (38px per row + 8px padding)
        dynamic_height = (actual_items_count * 38) + 8

        # 3. Calculate the absolute ceiling height for exactly 10 items Max
        max_allowed_height = (10 * 38) + 8  # Equals 388px

        # 4. Use python's min() to shrink-wrap small lists, but cap large lists at 10 items
        final_dropdown_height = min(dynamic_height, max_allowed_height)

        # Draw alignment locations matching the parent entry bar
        x = self.input_container.winfo_rootx()
        y = self.input_container.winfo_rooty() + self.input_container.winfo_height()
        width = self.input_container.winfo_width()

        if width <= 1:
            width = 300

        # Pass our newly calculated final_dropdown_height into the window geometry
        self.dropdown_window.geometry(f"{width}x{final_dropdown_height}+{x}+{y}")
        self.dropdown_window.deiconify()

        if hasattr(self, "results_frame"):
            self.results_frame.destroy()

        self.results_frame = ctk.CTkScrollableFrame(
            self.dropdown_window,
            fg_color="#1E293B",
            corner_radius=self.corner_radius,
            border_width=1,
            border_color="#334155",
        )
        self.results_frame.pack(fill="both", expand=True)

        self._build_results()

    def _hide_dropdown(self):
        if self.dropdown_window:
            try:
                self.dropdown_window.destroy()
            except Exception:
                pass
            self.dropdown_window = None

    # ─────────────────────────────────────────
    # SELECTION ELEMENT CONVERTERS
    # ─────────────────────────────────────────
    def _build_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for value in self.filtered_values:
            row = ctk.CTkFrame(
                self.results_frame,
                fg_color="transparent",
                corner_radius=self.corner_radius,
                height=38,
            )
            row.pack(fill="x", padx=4, pady=2)
            row.pack_propagate(False)

            row.bind("<Enter>", lambda e, r=row: r.configure(fg_color="#334155"))
            row.bind("<Leave>", lambda e, r=row: r.configure(fg_color="transparent"))

            image = None
            if self.image_provider:
                image = self.image_provider(value)
                if image:
                    self.image_cache.append(image)

            if image:
                image_label = ctk.CTkLabel(row, text="", image=image, width=20)
                image_label.pack(side="left", padx=(10, 4))
                image_label.bind("<Button-1>", lambda e, v=value: self._select_value(v))

            label = ctk.CTkLabel(
                row, text=value, anchor="w", text_color="#FFFFFF", font=("Inter", 14)
            )
            label.pack(side="left", padx=8)

            row.bind("<Button-1>", lambda e, v=value: self._select_value(v))
            label.bind("<Button-1>", lambda e, v=value: self._select_value(v))

    @staticmethod
    def load_image(path: str, size=(20, 14)):
        return ctk.CTkImage(Image.open(path), size=size)

    # ─────────────────────────────────────────
    # VALUE COMMITMENT MUTATORS
    # ─────────────────────────────────────────
    def _select_value(self, value: str):
        # We must temporarily switch state to normal to edit the entry programmatically
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.entry.configure(
            text_color="#FFFFFF", state="readonly"
        )  # Re-lock to read-only state

        if self.image_provider:
            image = self.image_provider(value)
            if image:
                self.left_image_label.configure(image=image, width=20)
            else:
                self.left_image_label.configure(image=None, width=0)

        # Output resolution converters
        self.selected_value = self.value_mapper(value) if self.value_mapper else value
        self._hide_dropdown()

        if self.command:
            self.command(self.selected_value)

    # ─────────────────────────────────────────
    # PUBLIC API CONSTRAINTS
    # ─────────────────────────────────────────
    def get(self):
        return self.selected_value

    def set(self, value: str):
        self._select_value(value)
