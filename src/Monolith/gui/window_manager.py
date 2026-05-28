"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.window_manager
DESCRIPTION:   Central Window Navigation Controller. Single source of truth for
               application geometry transitions, screen scaling orchestration,
               and native system menu integration pipelines.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       1.1.0
================================================================================
"""

from __future__ import annotations

# ── Standard Library ──────────────────────────────────────────────────────────
from typing import Any, Optional
from tkinter import Menu  # Import traditional Tkinter Menu tools
import customtkinter as ctk
from PIL import Image
import keyring
import os
import json

# ── Local Design System Tokens and Page Modules ───────────────────────────────
from gui.theme.layout import (
    LOGIN_HEIGHT,
    LOGIN_WIDTH,
    APP_WIDTH,
    APP_HEIGHT,
    APP_EXTENDED_HEIGHT,
)
from gui.theme.colors import BACKGROUND
from gui.widgets.tooltips import CTkToolTip
from gui.pages.login_page import LoginPage
from gui.pages.home_page import HomePage
from gui.pages.folder_page import FolderPage
from gui.pages.database_page import DatabaseMonitorWindow
from core.utils.paths import get_asset_path
from core.services.auth_service import AuthService

__all__ = ["MonolithApp"]


class MonolithApp(ctk.CTk):
    """
    Primary runtime window coordinator managing app lifecycle geometry adjustments
    and multi-stage interface presentation spaces.
    """

    def __init__(self) -> None:
        """
        Instantiate parent widget attributes, configure structural styles,
        and attach native operating system dropdown menus.
        """
        super().__init__(fg_color=BACKGROUND)

        # Set unified framework rendering skin defaults
        ctk.set_appearance_mode("dark")
        self.title("Monolith")
        self.resizable(False, False)

        # Draw baseline configuration dimensions to hold login forms safely
        self.center_window(LOGIN_WIDTH, LOGIN_HEIGHT)

        ## THIS IS FOR AUTO-LOGIN
        # self.after(
        #     100,
        #     self._coordinate_app_entry,
        # )

        ## THIS IS FOR AUTO-FILLING
        ###########################
        self.after(
            100,
            self.start_login,
        )

        # ── SYSTEM NATIVE MENU BAR CONFIGURATIONS ─────────────────────────────
        # Create the master menu bar container linked to the root window layer
        self.menubar: Menu = Menu(self)
        self.configure(menu=self.menubar)

        # Instantiate cascading dropdown children
        self.file_menu: Menu = Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="New Project...", command=self.on_new_project)
        self.file_menu.add_command(label="Open Database", command=self.on_open_database)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit App", command=self.destroy)

        # Cascade file bundle onto the top host system application display tree
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def _coordinate_app_entry(self) -> None:
        """
        Attempt silent login using saved credentials.
        """

        from core.services.auth_storage import (
            load_local_username,
            get_secure_token,
            clear_local_username,
            clear_secure_token,
        )

        saved_email = load_local_username()

        # No saved email -> show login page
        if not saved_email:

            self.start_login()
            return

        secure_token = get_secure_token(saved_email)

        # No token found -> clear broken state and show login
        if not secure_token:

            clear_local_username()

            self.start_login()
            return

        auth_service = AuthService()

        is_valid = auth_service.validate_token(secure_token)

        if is_valid:

            print("[AUTH] Silent login successful")

            self.start_main_app()

        else:

            print("[AUTH] Stored session expired")

            clear_secure_token(saved_email)
            clear_local_username()

            self.start_login()

    # ── DROPDOWN ACTION MENU COMMAND TRACKS ───────────────────────────────────

    def on_new_project(self) -> None:
        """Dispatches operational updates when user invokes new project configurations."""
        print("[MENU] Menu Triggered: Navigating to Project Wizard...")

    # Update the following method inside your MonolithApp class block:
    def on_open_database(self) -> None:
        """
        Instantiates and renders a standalone independent TopLevel window
        hosting our database query console logs.
        """
        print(
            "[MENU] Menu Triggered: Spawning independent Database Monitor Workspace..."
        )

        # Check if window instance already exists and is open to prevent duplicate spamming
        if hasattr(self, "db_window") and self.db_window.winfo_exists():
            self.db_window.lift()  # Bring existing window to front focus
            self.db_window.focus_set()
        else:
            # Instantiate the dedicated standalone monitor window element
            self.db_window = DatabaseMonitorWindow(master=self)

    # ── CORE NAVIGATION ELEMENT LIFECYCLE SEQUENCES ───────────────────────────

    def start_login(self) -> None:
        """
        Mount authentication panel forms directly onto the current frame workspace.
        """
        self.login_page: LoginPage = LoginPage(
            self,
            on_login=self.start_main_app,
        )
        self.login_page.pack(
            fill="both",
            expand=True,
        )

    def start_main_app(self) -> None:
        """
        Teardown active authentication contexts and dynamically instantiate
        the primary home page layout dashboard workspace.
        """
        # 1. Clean up and purge the login interface completely from memory
        if hasattr(self, "login_page") and self.login_page:
            self.login_page.destroy()

        # 2. Scale application window parameters to load home space bounds safely
        # Note: We read constants imported directly out of layout theme files
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.center_window(APP_WIDTH, APP_HEIGHT)

        # REFACTORING
        self.page_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.page_container.pack(
            fill="both",
            expand=True,
        )

        self.current_page = None

        self.show_home_page()

        ### OLD VERSION
        # 3. Instantiate the core homepage deck passing self as the host manager
        # self.home_page: HomePage = HomePage(master=self)

        # 4. Mount the layout securely into active root coordinates
        # self.home_page.pack(fill="both", expand=True, padx=10, pady=10)

    # ── DYNAMIC DRAW GEOMETRY TRANSFORMERS ────────────────────────────────────

    def toggle_window_drawer(self, open_drawer: bool) -> None:
        """
        Dynamically adjusts the physical window borders to show or hide the panel drawer.

        Parameters
        ----------
        open_drawer : bool
            True sets the extended telemetry canvas; False restores the compact baseline.
        """
        # Capture current screen placement offsets to avoid visual jumping across re-renders
        current_x = self.winfo_x()
        current_y = self.winfo_y()

        if open_drawer:
            # Expand window vertical heights to fit incoming database stream tables
            self.geometry(f"{APP_WIDTH}x{APP_EXTENDED_HEIGHT}+{current_x}+{current_y}")
        else:
            # Shrink-wrap borders back down to normal dashboard proportions
            self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{current_x}+{current_y}")

    def center_window(self, width: int, height: int) -> None:
        """
        Flushes layout tasks and centers the window configuration parameters perfectly.
        """
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_page(self, page_name: str) -> None:
        """
        Display selected page frame layer context.
        """
        if hasattr(self, "pages") and page_name in self.pages:
            self.pages[page_name].tkraise()

    def switch_page(self, page_class, **kwargs) -> None:
        """
        Destroy current page and mount a new one.
        """

        if self.current_page is not None:
            self.current_page.destroy()

        self.current_page = page_class(
            master=self.page_container,
            **kwargs,
        )

        self.current_page.pack(
            fill="both",
            expand=True,
        )

    def show_home_page(self) -> None:
        """
        Display home page.
        """

        self.switch_page(
            HomePage,
            on_navigate=self.handle_home_navigation,
        )

    def handle_home_navigation(self, destination: str) -> None:
        """
        Handle navigation events emitted by HomePage.
        """

        if destination == "folder":

            self.switch_page(
                FolderPage,
                on_back=self.show_home_page,
                on_next=self.handle_project_next,
            )

        elif destination == "document":

            print("[NAVIGATION] Document workflow not implemented.")

    def handle_project_next(self, data: dict) -> None:
        """
        Receive project workflow data.
        """

        print("[PROJECT DATA]")
        print(data)
