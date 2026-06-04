# database_viewer.py
import customtkinter as ctk
from database import fetch_records

# Design Tokens matching your screenshot
BG_COLOR = "#111827"  # Very dark slate background
CARD_BG = "#1F2937"  # Lighter slate row backgrounds
INPUT_BG = "#1E293B"  # Dropdowns and entry background
TEXT_MAIN = "#F3F4F6"  # White/Off-white main text
TEXT_MUTED = "#9CA3AF"  # Silver/Gray labels


class DatabaseViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_COLOR)
        self.pack(fill="both", expand=True)

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # The table rows expand

        self._build_toolbar()
        self._build_table_headers()
        self._build_scrollable_table()
        self._build_footer()

        # Load the initial data state
        self.refresh_data()

    # ─────────────────────────────────────────────────────────────
    # TOOLBAR (Filters & Search)
    # ─────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Global Search
        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search anything...",
            fg_color=INPUT_BG,
            width=250,
            height=36,
            border_width=0,
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

        # Types Dropdown
        self.type_filter = ctk.CTkOptionMenu(
            toolbar,
            values=["All Types", "Project", "Resource", "Document"],
            fg_color=INPUT_BG,
            button_color=INPUT_BG,
            height=36,
            command=lambda v: self.refresh_data(),
        )
        self.type_filter.pack(side="left", padx=5)

        # Countries Dropdown
        self.country_filter = ctk.CTkOptionMenu(
            toolbar,
            values=["All Countries", "France", "United States", "Germany", "UAE"],
            fg_color=INPUT_BG,
            button_color=INPUT_BG,
            height=36,
            command=lambda v: self.refresh_data(),
        )
        self.country_filter.pack(side="left", padx=5)

    # ─────────────────────────────────────────────────────────────
    # TABLE HEADERS
    # ─────────────────────────────────────────────────────────────
    def _build_table_headers(self):
        headers_frame = ctk.CTkFrame(self, fg_color="transparent")
        headers_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(15, 5))

        headers = [
            "Ref. Number",
            "Type",
            "Name / Title",
            "Country",
            "Added By",
            "Date Added",
        ]
        # Match column proportions roughly based on screenshot
        weights = [2, 1, 3, 1.5, 1.5, 2]

        for i, (text, weight) in enumerate(zip(headers, weights)):
            headers_frame.grid_columnconfigure(i, weight=int(weight * 10))
            lbl = ctk.CTkLabel(
                headers_frame,
                text=text,
                text_color=TEXT_MUTED,
                font=("Inter", 12, "bold"),
                anchor="w",
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=5)

    # ─────────────────────────────────────────────────────────────
    # SCROLLABLE ROWS CONTAINER
    # ─────────────────────────────────────────────────────────────
    def _build_scrollable_table(self):
        self.table_canvas = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.table_canvas.grid(row=2, column=0, sticky="nsew", padx=20, pady=0)

        # Dynamic weights configuration inside scrollable frame
        self.row_weights = [2, 1, 3, 1.5, 1.5, 2]
        for i, w in enumerate(self.row_weights):
            self.table_canvas.grid_columnconfigure(i, weight=int(w * 10))
