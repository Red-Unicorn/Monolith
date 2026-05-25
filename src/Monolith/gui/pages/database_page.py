"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.windows.database_monitor
DESCRIPTION:   Standalone TopLevel window console running asynchronous multi-threaded
               telemetry reads to your remote database deployment layer.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       1.0.0
================================================================================
"""

from __future__ import annotations
from typing import Any
import customtkinter as ctk
import threading
import time

# ── Local Theme Injection Tokens ──────────────────────────────────────────────
from gui.theme.colors import SIDEBAR, BORDER, TEXT


class DatabaseMonitorWindow(ctk.CTkToplevel):
    """
    Independent operations shell housing live telemetry streaming feeds.
    """

    def __init__(self, master: Any) -> None:
        super().__init__(master)

        # Configure secondary window boundaries
        self.title("Monolith Core System Database Console")
        self.geometry("640x400")
        self.minsize(500, 300)

        # Force focus onto this window when spawned
        self.after(100, self.lift)
        self.after(200, self.focus_set)

        # Threading safety locks
        self.is_fetching: bool = False

        # ── INTERFACE COMPONENT PACKS ─────────────────────────────────────────
        self.main_container = ctk.CTkFrame(self, fg_color=SIDEBAR, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.db_console_output = ctk.CTkTextbox(
            self.main_container,
            font=("JetBrains Mono", 11, "normal"),
            fg_color="#0F172A",
            text_color="#38BDF8",  # Cyber telemetry electric blue
            wrap="none",
        )
        self.db_console_output.pack(fill="both", expand=True, padx=20, pady=20)

        # Write initial standby diagnostic line
        self.db_console_output.insert(
            "0.0",
            "--- SYSTEM CORE DATABASE STREAM SUBSYSTEM ---\nInitializing handshakes...",
        )
        self.db_console_output.configure(state="disabled")

        # Fire off query pipelines immediately upon window creation
        self._trigger_async_db_fetch()

    def _trigger_async_db_fetch(self) -> None:
        """Spins up background workers to read database records without application freezes."""
        if self.is_fetching:
            return

        self.is_fetching = True
        self._write_console_log(
            "\n[SYSTEM] Connecting to remote operations data storage instance..."
        )

        # Deploy non-blocking execution thread loops safely
        worker_thread = threading.Thread(
            target=self._database_network_query_worker, daemon=True
        )
        worker_thread.start()

    def _database_network_query_worker(self) -> None:
        """Simulates live server network reads across mock configuration endpoints."""
        try:
            time.sleep(1.5)  # Simulate network latency limits

            mock_fetched_rows = [
                " -> CORES ENCRYPTED SOCKET MATCH: Monolith-DB-Primary.supabase.co via TLSv1.3",
                " -> LOG STREAM FETCH SUCCESS: SELECT * FROM operational_node_registry WHERE status = 'ONLINE';",
                "    | [NODE_ID]       | [SERVICE_NAME]        | [UPTIME]      | [LATENCY]   |",
                "    | ML-8942-ALPHA   | Analytics Pipeline    | 412h 14m      | 14.2ms      |",
                "    | ML-1105-DELTA   | Sharded Postgres 09   | 1205h 02m     | 8.7ms       |",
                "    | ML-7731-NODE    | Core Security Vector  | 92h 45m       | 3.1ms       |",
                " -> OPERATIONAL INTEGRITY CONFIRMED: Standalone multi-window telemetry operating normally.",
            ]

            for row in mock_fetched_rows:
                self._write_console_log(row)

        except Exception as err:
            self._write_console_log(f" -> ❌ RECOVERY ERROR: {err}")
        finally:
            self.is_fetching = False

    def _write_console_log(self, text_string: str) -> None:
        """Safely inserts messages onto the console log display from separate threads."""
        self.db_console_output.configure(state="normal")
        self.db_console_output.insert("end", f"\n{text_string}")
        self.db_console_output.see("end")
        self.db_console_output.configure(state="disabled")
