# from __future__ import annotations
# import customtkinter as ctk
# from PIL import Image


# class SearchComboBox(ctk.CTkFrame):
#     """
#     Rebuilt Searchable Combobox with reliable dynamic rendering,
#     strict corner radius adherence, and live image lookups from REGISTRY.
#     """

#     def __init__(
#         self,
#         master,
#         values: list[str],
#         width: int = 300,
#         height: int = 42,
#         max_results: int = 100,
#         placeholder_text: str = "Select",
#         command=None,
#         image_provider=None,
#         value_mapper=None,
#         dropdown_height: int = 220,
#         **kwargs,
#     ):
#         self.corner_radius = kwargs.pop("corner_radius", 8)
#         kwargs.setdefault("fg_color", "transparent")
#         super().__init__(master, **kwargs)

#         # Config Configuration Mappings
#         self.values = values
#         self.filtered_values = []
#         self.command = command
#         self.image_provider = image_provider
#         self.value_mapper = value_mapper
#         self.max_results = max_results
#         self.dropdown_height = dropdown_height
#         self.placeholder_text = placeholder_text
#         self.selected_value = ""

#         # Window & Optimization Tracking States
#         self.dropdown_window = None
#         self.image_cache = []
#         self._debounce_id = None

#         # ─────────────────────────────────────────
#         # MAIN INPUT BAR CONTAINER
#         # ─────────────────────────────────────────
#         self.input_container = ctk.CTkFrame(
#             self,
#             width=width,
#             height=height,
#             fg_color="#1E293B",
#             border_color="#334155",
#             border_width=1,
#             corner_radius=self.corner_radius,
#         )
#         self.input_container.pack(fill="x", pady=1)
#         self.input_container.pack_propagate(False)

#         # Left Image Slot (Displays active selection flag inside main header frame)
#         self.left_image_label = ctk.CTkLabel(self.input_container, text="", width=0)
#         self.left_image_label.pack(side="left", padx=(12, 0))

#         # Feature 1: ComboBox editable entry field
#         self.entry = ctk.CTkEntry(
#             self.input_container,
#             fg_color="transparent",
#             bg_color="transparent",
#             border_width=0,
#             corner_radius=0,
#             height=height - 4,
#             text_color="#94A3B8",
#             font=("Inter", 14),
#         )
#         self.entry.pack(side="left", fill="both", expand=True, padx=(4, 4))
#         self.entry.insert(0, self.placeholder_text)

#         # Feature 1: Toggle arrow dropdown button
#         self.arrow_button = ctk.CTkButton(
#             self.input_container,
#             text="▼",
#             width=34,
#             height=height - 6,
#             fg_color="transparent",
#             hover_color="#273449",
#             text_color="#94A3B8",
#             font=("Inter", 12, "bold"),
#             corner_radius=self.corner_radius,
#             command=self._toggle_dropdown,
#         )
#         self.arrow_button.pack(side="right", padx=(0, 4))

#         # Event Structural Loops
#         self.entry.bind("<Button-1>", self._open_dropdown)
#         self.entry.bind("<KeyRelease>", self._on_key_release)
#         self.entry.bind("<FocusIn>", self._clear_placeholder)
#         self.entry.bind("<FocusOut>", self._restore_placeholder)

#     # ─────────────────────────────────────────
#     # PLACEHOLDER BALANCING
#     # ─────────────────────────────────────────
#     def _clear_placeholder(self, event=None):
#         if self.entry.get() == self.placeholder_text:
#             self.entry.delete(0, "end")
#             self.entry.configure(text_color="#FFFFFF")

#     def _restore_placeholder(self, event=None):
#         self.after(120, self._restore_if_empty)

#     def _restore_if_empty(self):
#         if not self.entry.get().strip():
#             self.entry.delete(0, "end")
#             self.entry.insert(0, self.placeholder_text)
#             self.entry.configure(text_color="#94A3B8")
#             self.left_image_label.configure(image=None, width=0)
#             self.selected_value = ""
#         self._hide_dropdown()

#     # ─────────────────────────────────────────
#     # SMOOTH TYPING FILTER
#     # ─────────────────────────────────────────
#     def _on_key_release(self, event=None):
#         """Triggers search instantly on typing, preserving text input focus continuity."""
#         if event and event.keysym in (
#             "Shift_L",
#             "Shift_R",
#             "Control_L",
#             "Control_R",
#             "Caps_Lock",
#             "Left",
#             "Right",
#             "Up",
#             "Down",
#             "Escape",
#         ):
#             return

#         # Debounce the sorting/filtering calculation loop to keep typing smooth
#         if self._debounce_id:
#             self.after_cancel(self._debounce_id)
#         self._debounce_id = self.after(100, self._filter_values)

#     # ─────────────────────────────────────────
#     # DROPDOWN ACTIONS
#     # ─────────────────────────────────────────
#     def _toggle_dropdown(self):
#         if self.dropdown_window:
#             self._hide_dropdown()
#         else:
#             self._open_dropdown()

#     def _open_dropdown(self, event=None):
#         current = self.entry.get().strip()
#         if not current or current == self.placeholder_text:
#             self.filtered_values = self.values[: self.max_results]
#         else:
#             self.filtered_values = [
#                 val for val in self.values if current.lower() in val.lower()
#             ][: self.max_results]
#         self._show_dropdown()

#     def _filter_values(self):
#         """Fix 2: Recalculates sub-matches on keystrokes and backspaces smoothly."""
#         query = self.entry.get().strip().lower()

#         if not query or query == self.placeholder_text.lower():
#             self.filtered_values = self.values[: self.max_results]
#         else:
#             self.filtered_values = [val for val in self.values if query in val.lower()][
#                 : self.max_results
#             ]

#         # Force render the updated list window state immediately
#         self._show_dropdown()

#     def _show_dropdown(self):
#         if not self.filtered_values:
#             self._hide_dropdown()
#             return

#         self.update_idletasks()

#         # Fix 1: Create window with special focus-retention flags
#         if not self.dropdown_window:
#             self.dropdown_window = ctk.CTkToplevel(self)
#             self.dropdown_window.withdraw()  # Temporarily withdraw to prevent sudden jump flashes
#             self.dropdown_window.overrideredirect(True)

#             # Prevent the window from stealing primary typing focus focus
#             self.dropdown_window.tk.call(
#                 "wm", "attributes", self.dropdown_window._w, "-topmost", True
#             )
#             self.dropdown_window.configure(takefocus=False)

#             # Close dropdown window if user clicks elsewhere entirely
#             self.dropdown_window.bind("<FocusOut>", lambda e: self._hide_dropdown())

#         x = self.input_container.winfo_rootx()
#         y = self.input_container.winfo_rooty() + self.input_container.winfo_height()
#         width = self.input_container.winfo_width()

#         if width <= 1:
#             width = 300

#         self.dropdown_window.geometry(f"{width}x{self.dropdown_height}+{x}+{y}")
#         self.dropdown_window.deiconify()  # Safely bring window visibility back online

#         if hasattr(self, "results_frame"):
#             self.results_frame.destroy()

#         self.results_frame = ctk.CTkScrollableFrame(
#             self.dropdown_window,
#             fg_color="#1E293B",
#             corner_radius=self.corner_radius,
#             border_width=1,
#             border_color="#334155",
#         )
#         self.results_frame.pack(fill="both", expand=True)

#         self._build_results()

#     @staticmethod
#     def load_image(path: str, size=(20, 14)):
#         return ctk.CTkImage(Image.open(path), size=size)

#     def _hide_dropdown(self):
#         if self.dropdown_window:
#             try:
#                 self.dropdown_window.destroy()
#             except Exception:
#                 pass
#             self.dropdown_window = None
#             self.image_cache.clear()

#     # ─────────────────────────────────────────
#     # DYNAMIC RENDER PIPELINE
#     # ─────────────────────────────────────────
#     def _build_results(self):
#         self.image_cache.clear()

#         for value in self.filtered_values:
#             row = ctk.CTkFrame(
#                 self.results_frame,
#                 fg_color="transparent",
#                 corner_radius=self.corner_radius,
#                 height=38,
#             )
#             row.pack(fill="x", padx=4, pady=2)
#             row.pack_propagate(False)

#             row.bind("<Enter>", lambda e, r=row: r.configure(fg_color="#334155"))
#             row.bind("<Leave>", lambda e, r=row: r.configure(fg_color="transparent"))

#             image = None
#             if self.image_provider:
#                 image = self.image_provider(value)
#                 if image:
#                     self.image_cache.append(image)

#             if image:
#                 img_label = ctk.CTkLabel(row, text="", image=image)
#                 img_label.pack(side="left", padx=(10, 4))
#                 img_label.bind("<Button-1>", lambda e, v=value: self._select_value(v))

#             txt_label = ctk.CTkLabel(
#                 row, text=value, anchor="w", text_color="#FFFFFF", font=("Inter", 14)
#             )
#             txt_label.pack(side="left", padx=8)

#             row.bind("<Button-1>", lambda e, v=value: self._select_value(v))
#             txt_label.bind("<Button-1>", lambda e, v=value: self._select_value(v))

#     # ─────────────────────────────────────────
#     # SELECTION PROCESSING
#     # ─────────────────────────────────────────
#     def _select_value(self, value: str):
#         self.entry.delete(0, "end")
#         self.entry.insert(0, value)
#         self.entry.configure(text_color="#FFFFFF")

#         if self.image_provider:
#             image = self.image_provider(value)
#             if image:
#                 self.left_image_label.configure(image=image, width=20)
#             else:
#                 self.left_image_label.configure(image=None, width=0)

#         self.selected_value = self.value_mapper(value) if self.value_mapper else value
#         self._hide_dropdown()

#         if self.command:
#             self.command(self.selected_value)

#     def get(self):
#         return self.selected_value

#     def set(self, value: str):
#         self._select_value(value)


# # from __future__ import annotations

# # import customtkinter as ctk
# # from PIL import Image
# # from config.settings import REGISTRY


# # class SearchComboBox(ctk.CTkFrame):
# #     """
# #     Optimized Reusable searchable combobox.
# #     """

# #     def __init__(
# #         self,
# #         master,
# #         values: list[str],
# #         width: int = 300,
# #         height: int = 42,
# #         max_results: int = 150,  # Lowered slightly for smoother rendering
# #         placeholder_text: str = "Select",
# #         command=None,
# #         image_provider=None,
# #         value_mapper=None,
# #         dropdown_height: int = 220,
# #         **kwargs,
# #     ):
# #         self.corner_radius = kwargs.pop("corner_radius", 8)
# #         kwargs.setdefault("fg_color", "transparent")
# #         super().__init__(master, **kwargs)

# #         # DATA
# #         self.values = values
# #         self.filtered_values = []
# #         self.command = command
# #         self.image_provider = image_provider
# #         self.value_mapper = value_mapper
# #         self.max_results = max_results
# #         self.dropdown_height = dropdown_height
# #         self.placeholder_text = placeholder_text
# #         self.selected_value = ""

# #         # UI State Variables
# #         self.dropdown_window = None
# #         self.image_cache = []
# #         self._debounce_id = None  # To manage character delay timing
# #         self.pool_widgets = []  # Caches UI elements inside the dropdown

# #         # ─────────────────────────────────────────
# #         # MAIN CONTAINER
# #         # ─────────────────────────────────────────
# #         self.input_container = ctk.CTkFrame(
# #             self,
# #             width=width,
# #             height=height,
# #             fg_color="#1E293B",
# #             border_color="#334155",
# #             border_width=0,
# #             corner_radius=self.corner_radius,
# #         )
# #         self.input_container.pack(fill="x", pady=1)
# #         self.input_container.pack_propagate(False)

# #         # LEFT IMAGE
# #         self.left_image_label = ctk.CTkLabel(self.input_container, text="", width=0)
# #         self.left_image_label.pack(side="left", padx=(10, 0))

# #         # ENTRY
# #         self.entry = ctk.CTkEntry(
# #             self.input_container,
# #             fg_color="transparent",
# #             bg_color="transparent",
# #             border_width=0,
# #             corner_radius=0,
# #             height=height - 4,
# #             text_color="#94A3B8",
# #             font=("Inter", 14),
# #         )
# #         self.entry.pack(side="left", fill="both", expand=True, padx=(0, 4))
# #         self.entry.insert(0, self.placeholder_text)

# #         # ARROW BUTTON
# #         self.arrow_button = ctk.CTkButton(
# #             self.input_container,
# #             text="▼",
# #             width=34,
# #             height=height - 6,
# #             fg_color="transparent",
# #             hover_color="#273449",
# #             text_color="#94A3B8",
# #             font=("Inter", 12, "bold"),
# #             corner_radius=0,
# #             command=self._toggle_dropdown,
# #         )
# #         self.arrow_button.pack(side="right", padx=(0, 4))

# #         # EVENTS
# #         self.entry.bind("<Button-1>", self._open_dropdown)
# #         self.entry.bind(
# #             "<KeyRelease>", self._on_key_release
# #         )  # Routed through debouncer
# #         self.entry.bind("<FocusIn>", self._clear_placeholder)
# #         self.entry.bind("<FocusOut>", self._restore_placeholder)

# #     # ─────────────────────────────────────────
# #     # PLACEHOLDER DEFAULTS
# #     # ─────────────────────────────────────────
# #     def _clear_placeholder(self, event=None):
# #         if self.entry.get() == self.placeholder_text:
# #             self.entry.delete(0, "end")
# #             self.entry.configure(text_color="#FFFFFF")

# #     def _restore_placeholder(self, event=None):
# #         self.after(120, self._restore_if_empty)

# #     def _restore_if_empty(self):
# #         if not self.entry.get().strip():
# #             self.entry.delete(0, "end")
# #             self.entry.insert(0, self.placeholder_text)
# #             self.entry.configure(text_color="#94A3B8")
# #             self.left_image_label.configure(image=None, width=0)
# #             self.selected_value = ""
# #         self._hide_dropdown()

# #     # ─────────────────────────────────────────
# #     # DEBOUNCING MECHANISM
# #     # ─────────────────────────────────────────
# #     def _on_key_release(self, event=None):
# #         """Prevents computational stutter by delaying filtering until typing halts."""
# #         if self._debounce_id:
# #             self.after_cancel(self._debounce_id)
# #         self._debounce_id = self.after(150, self._filter_values)

# #     # ─────────────────────────────────────────
# #     # DROPDOWN LIFECYCLE
# #     # ─────────────────────────────────────────
# #     def _toggle_dropdown(self):
# #         if self.dropdown_window:
# #             self._hide_dropdown()
# #         else:
# #             self._open_dropdown()

# #     def _open_dropdown(self, event=None):
# #         current = self.entry.get().strip()
# #         if not current or current == self.placeholder_text:
# #             self.filtered_values = self.values[: self.max_results]
# #         else:
# #             self.filtered_values = [
# #                 val for val in self.values if current.lower() in val.lower()
# #             ][: self.max_results]

# #         if self.filtered_values:
# #             self._show_dropdown()

# #     def _filter_values(self):
# #         query = self.entry.get().strip().lower()
# #         if not query or query == self.placeholder_text.lower():
# #             self.filtered_values = self.values[: self.max_results]
# #             self._show_dropdown()
# #             return

# #         self.filtered_values = [val for val in self.values if query in val.lower()][
# #             : self.max_results
# #         ]

# #         if self.filtered_values:
# #             self._show_dropdown()
# #         else:
# #             self._hide_dropdown()

# #     def _show_dropdown(self):
# #         if not self.dropdown_window:
# #             self.dropdown_window = ctk.CTkToplevel(self)
# #             self.dropdown_window.overrideredirect(True)
# #             self.dropdown_window.attributes("-topmost", True)

# #             self.results_frame = ctk.CTkScrollableFrame(
# #                 self.dropdown_window,
# #                 fg_color="#1E293B",
# #                 corner_radius=self.corner_radius,
# #             )
# #             self.results_frame.pack(fill="both", expand=True)

# #             # Instantiate the component objects inside our pool once
# #             self._prebuild_widget_pool()

# #         # Recalculate Geometry constraints
# #         x = self.input_container.winfo_rootx()
# #         y = self.input_container.winfo_rooty() + self.input_container.winfo_height()
# #         width = self.input_container.winfo_width()
# #         self.dropdown_window.geometry(f"{width}x{self.dropdown_height}+{x}+{y}")

# #         self._update_results()

# #     def _hide_dropdown(self):
# #         if self.dropdown_window:
# #             try:
# #                 self.dropdown_window.destroy()
# #             except Exception:
# #                 pass
# #             self.dropdown_window = None
# #             self.pool_widgets.clear()
# #             self.image_cache.clear()  # Dump pointer memory instantly

# #     # ─────────────────────────────────────────
# #     # OPTIMIZED WIDGET REUSE (POOLING)
# #     # ─────────────────────────────────────────
# #     def _prebuild_widget_pool(self):
# #         """Constructs UI containers upfront to mitigate allocation stutters."""
# #         self.pool_widgets = []
# #         for _ in range(self.max_results):
# #             row = ctk.CTkFrame(
# #                 self.results_frame,
# #                 fg_color="transparent",
# #                 corner_radius=self.corner_radius,
# #                 height=38,
# #             )
# #             row.pack_propagate(False)

# #             img_label = ctk.CTkLabel(row, text="", width=0)
# #             img_label.pack(side="left", padx=(10, 4))

# #             txt_label = ctk.CTkLabel(
# #                 row, text="", anchor="w", text_color="#FFFFFF", font=("Inter", 14)
# #             )
# #             txt_label.pack(side="left", padx=8)

# #             # Store references to modify fields in-place
# #             self.pool_widgets.append(
# #                 {"row": row, "img_label": img_label, "txt_label": txt_label}
# #             )

# #     def _update_results(self):
# #         """Alters existing data values and structural layouts instead of redefining components."""
# #         self.image_cache.clear()  # Drop images from former lookup state
# #         total_filtered = len(self.filtered_values)

# #         for i in range(self.max_results):
# #             meta = self.pool_widgets[i]

# #             if i < total_filtered:
# #                 value = self.filtered_values[i]

# #                 # Assign dynamic closures safely
# #                 meta["row"].bind(
# #                     "<Enter>", lambda e, r=meta["row"]: r.configure(fg_color="#334155")
# #                 )
# #                 meta["row"].bind(
# #                     "<Leave>",
# #                     lambda e, r=meta["row"]: r.configure(fg_color="transparent"),
# #                 )
# #                 meta["row"].bind("<Button-1>", lambda e, v=value: self._select_value(v))
# #                 meta["txt_label"].bind(
# #                     "<Button-1>", lambda e, v=value: self._select_value(v)
# #                 )
# #                 meta["img_label"].bind(
# #                     "<Button-1>", lambda e, v=value: self._select_value(v)
# #                 )

# #                 # Inject text
# #                 meta["txt_label"].configure(text=value)

# #                 # Fetch images from pre-loaded REGISTRY values
# #                 image = None
# #                 if self.image_provider:
# #                     image = self.image_provider(value)
# #                     if image:
# #                         self.image_cache.append(image)

# #                 if image:
# #                     meta["img_label"].configure(image=image, width=20)
# #                     meta["img_label"].pack(side="left", padx=(10, 4))
# #                 else:
# #                     meta["img_label"].configure(image=None, width=0)
# #                     meta["img_label"].pack_forget()

# #                 # Display the structural rows
# #                 meta["row"].pack(fill="x", padx=4, pady=2)
# #             else:
# #                 # Remove extra rows from view without destroying them
# #                 meta["row"].pack_forget()

# #     # ─────────────────────────────────────────
# #     # SELECTION & GETTERS
# #     # ─────────────────────────────────────────
# #     def _select_value(self, value: str):
# #         self.entry.delete(0, "end")
# #         self.entry.insert(0, value)
# #         self.entry.configure(text_color="#FFFFFF")

# #         if self.image_provider:
# #             image = self.image_provider(value)
# #             if image:
# #                 self.left_image_label.configure(image=image, width=20)

# #         self.selected_value = self.value_mapper(value) if self.value_mapper else value
# #         self._hide_dropdown()

# #         if self.command:
# #             self.command(self.selected_value)

# #     def get(self):
# #         return self.selected_value

# #     def set(self, value: str):
# #         self._select_value(value)


from __future__ import annotations

import customtkinter as ctk
from PIL import Image


class SearchComboBox(ctk.CTkFrame):
    """
    Reusable searchable combobox.

    FEATURES
    ─────────────────────────────────────────
    • Searchable dropdown
    • Can behave like normal combobox
    • Optional images support
    • Reusable for:
        - countries / flags
        - file types
        - categories
        - icons
        - anything else
    • Works without images
    • Returns raw selected value by default
    • Optional value mapping support
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
        border_width: int = 0,
        **kwargs,
    ):

        self.corner_radius = kwargs.pop("corner_radius", corner_radius)

        kwargs.setdefault("fg_color", "transparent")

        super().__init__(master, **kwargs)

        # DATA
        self.values = values
        self.filtered_values = []
        self.command = command
        self.border_width = border_width
        self.image_provider = image_provider
        self.value_mapper = value_mapper
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
            border_width=0,  # 1,
            corner_radius=8,
        )

        self.input_container.pack(fill="x", pady=1)
        self.input_container.pack_propagate(False)

        # LEFT IMAGE
        self.left_image_label = ctk.CTkLabel(
            self.input_container,
            text="",
            width=0,
        )

        self.left_image_label.pack(
            side="left",
            padx=(10, 0),
        )

        # ENTRY
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
        # self.entry = ctk.CTkEntry(
        #     self.input_container,
        #     fg_color="transparent",
        #     border_width=0,
        #     height=height - 4,
        #     text_color="#94A3B8",
        #     font=("Inter", 14),
        #     corner_radius=self.corner_radius,
        # )

        self.entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 4),
        )

        self.entry.insert(0, self.placeholder_text)

        # ARROW
        self.arrow_button = ctk.CTkButton(
            self.input_container,
            text="▼",
            width=34,
            height=height - 6,
            fg_color="transparent",
            hover_color="#273449",
            text_color="#94A3B8",
            font=("Inter", 12, "bold"),
            corner_radius=0,
            # corner_radius=self.corner_radius,
            command=self._toggle_dropdown,
        )

        self.arrow_button.pack(
            side="right",
            padx=(0, 4),
        )

        # EVENTS
        self.entry.bind("<Button-1>", self._open_dropdown)
        self.entry.bind("<KeyRelease>", self._filter_values)

        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

    # ─────────────────────────────────────────
    # PLACEHOLDER
    # ─────────────────────────────────────────

    def _clear_placeholder(self, event=None):

        if self.entry.get() == self.placeholder_text:

            self.entry.delete(0, "end")

            self.entry.configure(
                text_color="#FFFFFF",
            )

    def _restore_placeholder(self, event=None):

        self.after(
            120,
            self._restore_if_empty,
        )

    def _restore_if_empty(self):

        if not self.entry.get().strip():

            self.entry.delete(0, "end")

            self.entry.insert(
                0,
                self.placeholder_text,
            )

            self.entry.configure(
                text_color="#94A3B8",
            )

            self.left_image_label.configure(
                image=None,
                width=0,
            )

            self.selected_value = ""

        self._hide_dropdown()

    # ─────────────────────────────────────────
    # DROPDOWN CONTROL
    # ─────────────────────────────────────────

    def _toggle_dropdown(self):

        if self.dropdown_window:

            self._hide_dropdown()

        else:

            self._open_dropdown()

    def _open_dropdown(self, event=None):

        current = self.entry.get().strip()

        # SHOW ALL
        if not current or current == self.placeholder_text:

            self.filtered_values = self.values[: self.max_results]

        else:

            self.filtered_values = [
                value for value in self.values if current.lower() in value.lower()
            ][: self.max_results]

        if self.filtered_values:

            self._show_dropdown()

    # ─────────────────────────────────────────
    # FILTER
    # ─────────────────────────────────────────

    def _filter_values(self, event=None):

        query = self.entry.get().strip().lower()

        # EMPTY = show all
        if not query or query == self.placeholder_text.lower():

            self.filtered_values = self.values[: self.max_results]

            self._show_dropdown()

            return

        # FILTER
        self.filtered_values = [
            value for value in self.values if query in value.lower()
        ][: self.max_results]

        if self.filtered_values:

            self._show_dropdown()

        else:

            self._hide_dropdown()

    # ─────────────────────────────────────────
    # DROPDOWN WINDOW
    # ─────────────────────────────────────────

    def _show_dropdown(self):

        self._hide_dropdown()

        self.dropdown_window = ctk.CTkToplevel(self)

        self.dropdown_window.overrideredirect(True)

        self.dropdown_window.attributes(
            "-topmost",
            True,
        )

        x = self.input_container.winfo_rootx()

        y = self.input_container.winfo_rooty() + self.input_container.winfo_height()

        width = self.input_container.winfo_width()

        self.dropdown_window.geometry(f"{width}x{self.dropdown_height}+{x}+{y}")

        self.results_frame = ctk.CTkScrollableFrame(
            self.dropdown_window,
            fg_color="#1E293B",
            corner_radius=self.corner_radius,
        )

        self.results_frame.pack(
            fill="both",
            expand=True,
        )

        self._build_results()

    def _hide_dropdown(self):

        if self.dropdown_window:

            try:
                self.dropdown_window.destroy()

            except Exception:
                pass

            self.dropdown_window = None

    # ─────────────────────────────────────────
    # RESULTS
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

            row.pack(
                fill="x",
                padx=4,
                pady=2,
            )

            row.pack_propagate(False)

            row.bind(
                "<Enter>",
                lambda e, r=row: r.configure(fg_color="#334155"),
            )

            row.bind(
                "<Leave>",
                lambda e, r=row: r.configure(fg_color="transparent"),
            )

            # OPTIONAL IMAGE
            image = None

            if self.image_provider:

                image = self.image_provider(value)

                if image:

                    self.image_cache.append(image)

            if image:

                image_label = ctk.CTkLabel(
                    row,
                    text="",
                    image=image,
                    width=20,
                )

                image_label.pack(
                    side="left",
                    padx=(10, 4),
                )

                image_label.bind(
                    "<Button-1>",
                    lambda e, v=value: self._select_value(v),
                )

            label = ctk.CTkLabel(
                row,
                text=value,
                anchor="w",
                text_color="#FFFFFF",
                font=("Inter", 14),
            )

            label.pack(
                side="left",
                padx=8,
            )

            # CLICK EVENTS
            row.bind(
                "<Button-1>",
                lambda e, v=value: self._select_value(v),
            )

            label.bind(
                "<Button-1>",
                lambda e, v=value: self._select_value(v),
            )

    # ─────────────────────────────────────────
    # IMAGE LOADER
    # ─────────────────────────────────────────

    @staticmethod
    def load_image(
        path: str,
        size=(20, 14),
    ):

        return ctk.CTkImage(
            Image.open(path),
            size=size,
        )

    # ─────────────────────────────────────────
    # SELECT VALUE
    # ─────────────────────────────────────────

    def _select_value(self, value: str):

        self.entry.delete(0, "end")

        self.entry.insert(0, value)

        self.entry.configure(
            text_color="#FFFFFF",
        )

        # LEFT IMAGE
        if self.image_provider:

            image = self.image_provider(value)

            if image:

                self.left_image_label.configure(
                    image=image,
                    width=20,
                )
            else:
                self.left_image_label.configure(image=None, width=0)
                self.left_image_label.pack_forget()

        # RAW OR MAPPED VALUE
        if self.value_mapper:

            self.selected_value = self.value_mapper(value)

        else:

            self.selected_value = value

        self._hide_dropdown()

        if self.command:

            self.command(
                self.selected_value,
            )

    # ─────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────

    def get(self):

        return self.selected_value

    def set(self, value: str):

        self._select_value(value)
