"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.database_page
DESCRIPTION:   Supabase-backed remote grid database viewer component.
================================================================================
"""

from __future__ import annotations

import os
import customtkinter as ctk
from supabase import create_client, Client

# Injected Design Framework Tokens
from gui.theme.colors import BACKGROUND, CARD_BG
from gui.widgets.buttons import make_button

# Config Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-anon-key")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

# Design System Styling Rules
INPUT_BG = "#1E293B"
TEXT_MAIN = "#F3F4F6"
TEXT_MUTED = "#9CA3AF"

# ──────────────────────────────────────────────────────────────────────────────
# DATABASE LAYER UTILITIES
# ──────────────────────────────────────────────────────────────────────────────


def fetch_records(
    search_query: str = "",
    record_type: str = "All Types",
    country: str = "All Countries",
):
    if not supabase:
        # Mock fallback data structured precisely to mirror the screenshot if client connection isn't configured
        return [
            {
                "ref_number": "FR-BNK-PRJ-A1B2",
                "type": "Project",
                "name_title": "Digital Banking Platform",
                "country": "France",
                "added_by": "John Doe",
                "date_added": "2024-05-20 10:15",
            },
            {
                "ref_number": "US-ITS-RES-C3D4",
                "type": "Resource",
                "name_title": "Cybersecurity Toolkit",
                "country": "United States",
                "added_by": "Jane Smith",
                "date_added": "2024-05-20 09:42",
            },
            {
                "ref_number": "20240520-DOC-LGL-FR-BNK-0001",
                "type": "Document",
                "name_title": "Client_Agreement",
                "country": "France",
                "added_by": "John Doe",
                "date_added": "2024-05-20 11:02",
            },
            {
                "ref_number": "DE-MAN-PRJ-E5F6",
                "type": "Project",
                "name_title": "Factory Expansion",
                "country": "Germany",
                "added_by": "Mike Brown",
                "date_added": "2024-05-19 16:33",
            },
        ]

    query = supabase.table("records").select(
        "ref_number, type, name_title, country, added_by, date_added"
    )

    if record_type != "All Types":
        query = query.eq("type", record_type)
    if country != "All Countries":
        query = query.eq("country", country)
    if search_query.strip():
        search_str = f"%{search_query}%"
        query = query.or_(
            f"ref_number.ilike.{search_str},name_title.ilike.{search_str}"
        )

    query = query.order("date_added", descending=True)

    try:
        return query.execute().data
    except Exception as e:
        print(f"[DATABASE ERROR] Connection failure: {e}")
        return []


# ──────────────────────────────────────────────────────────────────────────────
# PRIMARY PAGE VIEW FRAME
# ──────────────────────────────────────────────────────────────────────────────


class DatabaseViewer(ctk.CTkFrame):
    def __init__(self, master, on_back=None):
        super().__init__(master, fg_color=BACKGROUND)
        self.on_back = on_back

        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Row content table receives layout scaling

        self._build_toolbar()
        self._build_table_headers()
        self._build_scrollable_table()
        self._build_footer()

        self.refresh_data()

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 10))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search anything...",
            fg_color=INPUT_BG,
            width=280,
            height=38,
            border_width=0,
        )
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

        self.type_filter = ctk.CTkOptionMenu(
            toolbar,
            values=["All Types", "Project", "Resource", "Document"],
            fg_color=INPUT_BG,
            button_color=INPUT_BG,
            height=38,
            width=140,
            command=lambda v: self.refresh_data(),
        )
        self.type_filter.pack(side="left", padx=6)

        self.country_filter = ctk.CTkOptionMenu(
            toolbar,
            values=["All Countries", "France", "United States", "Germany", "UAE"],
            fg_color=INPUT_BG,
            button_color=INPUT_BG,
            height=38,
            width=150,
            command=lambda v: self.refresh_data(),
        )
        self.country_filter.pack(side="left", padx=6)

    def _build_table_headers(self):
        headers_frame = ctk.CTkFrame(self, fg_color="transparent")
        headers_frame.grid(row=1, column=0, sticky="ew", padx=45, pady=(15, 5))

        headers = [
            "Ref. Number",
            "Type",
            "Name / Title",
            "Country",
            "Added By",
            "Date Added",
        ]
        weights = [22, 12, 30, 16, 14, 18]

        for i, (text, weight) in enumerate(zip(headers, weights)):
            headers_frame.grid_columnconfigure(i, weight=weight)
            lbl = ctk.CTkLabel(
                headers_frame,
                text=text,
                text_color=TEXT_MUTED,
                font=("Inter", 12, "bold"),
                anchor="w",
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=5)

    def _build_scrollable_table(self):
        self.table_canvas = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.table_canvas.grid(row=2, column=0, sticky="nsew", padx=30, pady=0)

        self.row_weights = [22, 12, 30, 16, 14, 18]
        for i, w in enumerate(self.row_weights):
            self.table_canvas.grid_columnconfigure(i, weight=w)

    def refresh_data(self):
        for widget in self.table_canvas.winfo_children():
            widget.destroy()

        records = fetch_records(
            search_query=self.search_entry.get(),
            record_type=self.type_filter.get(),
            country=self.country_filter.get(),
        )

        for row_idx, data in enumerate(records):
            row_bg = CARD_BG if row_idx % 2 == 0 else "transparent"

            # Wrap rows inside full width sub-frames to handle structured background coloring neatly
            row_strip = ctk.CTkFrame(
                self.table_canvas, fg_color=row_bg, corner_radius=4, height=40
            )
            row_strip.grid(row=row_idx, column=0, columnspan=6, sticky="ew", pady=2)
            row_strip.grid_propagate(False)

            for i, w in enumerate(self.row_weights):
                row_strip.grid_columnconfigure(i, weight=w)

            ordered_keys = [
                "ref_number",
                "type",
                "name_title",
                "country",
                "added_by",
                "date_added",
            ]
            for col_idx, key in enumerate(ordered_keys):
                val = str(data.get(key, ""))
                if key == "date_added" and "T" in val:
                    val = val.replace("T", " ")[:16]

                cell_lbl = ctk.CTkLabel(
                    row_strip,
                    text=val,
                    text_color=TEXT_MAIN,
                    font=("Inter", 13),
                    anchor="w",
                )
                cell_lbl.grid(row=0, column=col_idx, sticky="nsew", padx=10)

        self.counter_label.configure(text=f"Total: {len(records)} records")

    def _build_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(15, 25))

        if self.on_back:
            self.back_button = make_button(
                master=footer_frame,
                text="← Back to Dashboard",
                command=self.on_back,
                variant="secondary",
                size="md",
            )
            self.back_button.pack(side="left", padx=(5, 15))

        self.counter_label = ctk.CTkLabel(
            footer_frame,
            text="Total: 0 records",
            text_color=TEXT_MUTED,
            font=("Inter", 13),
        )
        self.counter_label.pack(side="left", padx=5)

        self.excel_btn = make_button(
            master=footer_frame, text="Export Excel", variant="primary", size="md"
        )
        self.excel_btn.pack(side="right", padx=5)

        self.csv_btn = make_button(
            master=footer_frame, text="Export CSV", variant="secondary", size="md"
        )
        self.csv_btn.pack(side="right", padx=5)


# ──────────────────────────────────────────────────────────────────────────────
# OPTIONAL BACKWARDS COMPATIBILITY TOPLEVEL WINDOW
# ──────────────────────────────────────────────────────────────────────────────


class DatabaseMonitorWindow(ctk.CTkToplevel):
    """Fallback handler interface if menu calls demand an isolated floating layout window frame."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Database Monitor Context Layer")
        self.geometry("950x550")
        self.configure(fg_color=BACKGROUND)

        # Instantiates internal structural data grid component pointing locally inside window context layer
        self.viewer = DatabaseViewer(self, on_back=self.destroy)


# """
# ================================================================================
# PROJECT:       Monolith Application Engine
# MODULE:        gui.windows.database_monitor
# DESCRIPTION:   Standalone TopLevel window console running asynchronous multi-threaded
#                telemetry reads to your remote database deployment layer.
# AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
# LICENSE:       Proprietary – All rights reserved
# VERSION:       1.0.0
# ================================================================================
# """

# from __future__ import annotations
# from typing import Any
# import customtkinter as ctk
# import threading
# import time

# # ── Local Theme Injection Tokens ──────────────────────────────────────────────
# from gui.theme.colors import SIDEBAR, BORDER, TEXT


# class DatabaseMonitorWindow(ctk.CTkToplevel):
#     """
#     Independent operations shell housing live telemetry streaming feeds.
#     """

#     def __init__(self, master: Any) -> None:
#         super().__init__(master)

#         # Configure secondary window boundaries
#         self.title("Monolith Core System Database Console")
#         self.geometry("640x400")
#         self.minsize(500, 300)

#         # Force focus onto this window when spawned
#         self.after(100, self.lift)
#         self.after(200, self.focus_set)

#         # Threading safety locks
#         self.is_fetching: bool = False

#         # ── INTERFACE COMPONENT PACKS ─────────────────────────────────────────
#         self.main_container = ctk.CTkFrame(self, fg_color=SIDEBAR, corner_radius=0)
#         self.main_container.pack(fill="both", expand=True)

#         self.db_console_output = ctk.CTkTextbox(
#             self.main_container,
#             font=("JetBrains Mono", 11, "normal"),
#             fg_color="#0F172A",
#             text_color="#38BDF8",  # Cyber telemetry electric blue
#             wrap="none",
#         )
#         self.db_console_output.pack(fill="both", expand=True, padx=20, pady=20)

#         # Write initial standby diagnostic line
#         self.db_console_output.insert(
#             "0.0",
#             "--- SYSTEM CORE DATABASE STREAM SUBSYSTEM ---\nInitializing handshakes...",
#         )
#         self.db_console_output.configure(state="disabled")

#         # Fire off query pipelines immediately upon window creation
#         self._trigger_async_db_fetch()

#     def _trigger_async_db_fetch(self) -> None:
#         """Spins up background workers to read database records without application freezes."""
#         if self.is_fetching:
#             return

#         self.is_fetching = True
#         self._write_console_log(
#             "\n[SYSTEM] Connecting to remote operations data storage instance..."
#         )

#         # Deploy non-blocking execution thread loops safely
#         worker_thread = threading.Thread(
#             target=self._database_network_query_worker, daemon=True
#         )
#         worker_thread.start()

#     def _database_network_query_worker(self) -> None:
#         """Simulates live server network reads across mock configuration endpoints."""
#         try:
#             time.sleep(1.5)  # Simulate network latency limits

#             mock_fetched_rows = [
#                 " -> CORES ENCRYPTED SOCKET MATCH: Monolith-DB-Primary.supabase.co via TLSv1.3",
#                 " -> LOG STREAM FETCH SUCCESS: SELECT * FROM operational_node_registry WHERE status = 'ONLINE';",
#                 "    | [NODE_ID]       | [SERVICE_NAME]        | [UPTIME]      | [LATENCY]   |",
#                 "    | ML-8942-ALPHA   | Analytics Pipeline    | 412h 14m      | 14.2ms      |",
#                 "    | ML-1105-DELTA   | Sharded Postgres 09   | 1205h 02m     | 8.7ms       |",
#                 "    | ML-7731-NODE    | Core Security Vector  | 92h 45m       | 3.1ms       |",
#                 " -> OPERATIONAL INTEGRITY CONFIRMED: Standalone multi-window telemetry operating normally.",
#             ]

#             for row in mock_fetched_rows:
#                 self._write_console_log(row)

#         except Exception as err:
#             self._write_console_log(f" -> ❌ RECOVERY ERROR: {err}")
#         finally:
#             self.is_fetching = False

#     def _write_console_log(self, text_string: str) -> None:
#         """Safely inserts messages onto the console log display from separate threads."""
#         self.db_console_output.configure(state="normal")
#         self.db_console_output.insert("end", f"\n{text_string}")
#         self.db_console_output.see("end")
#         self.db_console_output.configure(state="disabled")
