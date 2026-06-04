"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.window_manager
DESCRIPTION:   Central Window Navigation Controller
================================================================================
"""

from __future__ import annotations

from tkinter import Menu
import customtkinter as ctk

from gui.theme.layout import (
    LOGIN_HEIGHT,
    LOGIN_WIDTH,
    APP_WIDTH,
    APP_HEIGHT,
)

from gui.theme.colors import BACKGROUND

from gui.pages.login_page import LoginPage
from gui.pages.home_page import HomePage
from gui.pages.folder_page import FolderPage
from gui.pages.ref_page import RefPage
from gui.pages.doc_page import DocPage
from gui.pages.database_page import DatabaseViewer, DatabaseMonitorWindow


class MonolithApp(ctk.CTk):

    def __init__(self) -> None:
        super().__init__(fg_color=BACKGROUND)

        # ---------------------------------------------------------
        # GLOBAL WINDOW CONFIG
        # ---------------------------------------------------------
        ctk.set_appearance_mode("dark")
        self.title("Monolith")
        self.resizable(False, False)
        self.center_window(LOGIN_WIDTH, LOGIN_HEIGHT)

        # ---------------------------------------------------------
        # MENU BAR
        # ---------------------------------------------------------
        self.menubar = Menu(self)
        self.configure(menu=self.menubar)

        self.file_menu = Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="New Project...", command=self.on_new_project)
        self.file_menu.add_command(
            label="Open Database Window", command=self.on_open_database
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit App", command=self.destroy)

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # ---------------------------------------------------------
        # START LOGIN
        # ---------------------------------------------------------
        self.after(100, self.start_login)

    # =============================================================
    # LOGIN
    # =============================================================
    def start_login(self) -> None:
        self.login_page = LoginPage(
            self,
            on_login=self.start_main_app,
        )
        self.login_page.pack(fill="both", expand=True)

    # =============================================================
    # MAIN APP
    # =============================================================
    def start_main_app(self) -> None:
        if hasattr(self, "login_page"):
            self.login_page.destroy()

        self.center_window(APP_WIDTH, APP_HEIGHT)

        self.page_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.page_container.pack(fill="both", expand=True)

        self.current_page = None
        self.show_home_page()

    # =============================================================
    # PAGE SWITCHING
    # =============================================================
    def switch_page(self, page_class, **kwargs) -> None:
        if self.current_page is not None:
            self.current_page.destroy()

        self.current_page = page_class(
            master=self.page_container,
            **kwargs,
        )
        self.current_page.pack(fill="both", expand=True)

    # =============================================================
    # HOME PAGE
    # =============================================================
    def show_home_page(self) -> None:
        self.switch_page(
            HomePage,
            on_navigate=self.handle_home_navigation,
        )

    # =============================================================
    # HOME NAVIGATION
    # =============================================================
    def handle_home_navigation(self, destination: str) -> None:
        if destination == "folder":
            self.show_folder_page()
        elif destination == "document":
            self.show_doc_page()
        elif destination == "database":
            self.show_database_page()

    # =============================================================
    # FOLDER PAGE
    # =============================================================
    def show_folder_page(self) -> None:
        self.switch_page(
            FolderPage,
            on_back=self.show_home_page,
            on_next=self.show_ref_page,
        )

    # =============================================================
    # REF PAGE
    # =============================================================
    def show_ref_page(self, data: dict) -> None:
        self.switch_page(
            RefPage,
            data=data,
            on_back=self.show_folder_page,
            on_dashboard=self.show_home_page,
        )

    # =============================================================
    # DOCUMENT PAGE
    # =============================================================
    def show_doc_page(self) -> None:
        self.switch_page(
            DocPage,
            on_back=self.show_home_page,
            on_next=self.show_ref_page,
        )

    # =============================================================
    # DATABASE FULL WORKSPACE PAGE
    # =============================================================
    def show_database_page(self) -> None:
        """Mounts the database grid interface directly in the main view area."""
        self.switch_page(
            DatabaseViewer,
            on_back=self.show_home_page,
        )

    # =============================================================
    # MENU ACTIONS
    # =============================================================
    def on_new_project(self) -> None:
        print("[MENU] New Project")

    def on_open_database(self) -> None:
        if hasattr(self, "db_window") and self.db_window.winfo_exists():
            self.db_window.lift()
            self.db_window.focus_set()
        else:
            self.db_window = DatabaseMonitorWindow(master=self)

    # =============================================================
    # WINDOW HELPERS
    # =============================================================
    def center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


# """
# ================================================================================
# PROJECT:       Monolith Application Engine
# MODULE:        gui.window_manager
# DESCRIPTION:   Central Window Navigation Controller
# ================================================================================
# """

# from __future__ import annotations

# from tkinter import Menu
# import customtkinter as ctk

# from gui.theme.layout import (
#     LOGIN_HEIGHT,
#     LOGIN_WIDTH,
#     APP_WIDTH,
#     APP_HEIGHT,
# )

# from gui.theme.colors import BACKGROUND

# from gui.pages.login_page import LoginPage
# from gui.pages.home_page import HomePage
# from gui.pages.folder_page import FolderPage
# from gui.pages.ref_page import RefPage
# from gui.pages.database_page import DatabaseMonitorWindow
# from gui.pages.doc_page import DocPage


# class MonolithApp(ctk.CTk):

#     def __init__(self) -> None:
#         super().__init__(fg_color=BACKGROUND)

#         # ---------------------------------------------------------
#         # GLOBAL WINDOW CONFIG
#         # ---------------------------------------------------------
#         ctk.set_appearance_mode("dark")
#         self.title("Monolith")
#         self.resizable(False, False)
#         self.center_window(LOGIN_WIDTH, LOGIN_HEIGHT)

#         # ---------------------------------------------------------
#         # MENU BAR
#         # ---------------------------------------------------------
#         self.menubar = Menu(self)
#         self.configure(menu=self.menubar)

#         self.file_menu = Menu(self.menubar, tearoff=False)
#         self.file_menu.add_command(label="New Project...", command=self.on_new_project)
#         self.file_menu.add_command(label="Open Database", command=self.on_open_database)
#         self.file_menu.add_separator()
#         self.file_menu.add_command(label="Exit App", command=self.destroy)

#         self.menubar.add_cascade(label="File", menu=self.file_menu)

#         # ---------------------------------------------------------
#         # START LOGIN
#         # ---------------------------------------------------------
#         self.after(100, self.start_login)

#     # =============================================================
#     # LOGIN
#     # =============================================================
#     def start_login(self) -> None:
#         self.login_page = LoginPage(
#             self,
#             on_login=self.start_main_app,
#         )
#         self.login_page.pack(fill="both", expand=True)

#     # =============================================================
#     # MAIN APP
#     # =============================================================
#     def start_main_app(self) -> None:
#         if hasattr(self, "login_page"):
#             self.login_page.destroy()

#         self.center_window(APP_WIDTH, APP_HEIGHT)

#         self.page_container = ctk.CTkFrame(
#             self,
#             fg_color="transparent",
#         )
#         self.page_container.pack(fill="both", expand=True)

#         self.current_page = None
#         self.show_home_page()

#     # =============================================================
#     # PAGE SWITCHING
#     # =============================================================
#     def switch_page(self, page_class, **kwargs) -> None:
#         if self.current_page is not None:
#             self.current_page.destroy()

#         self.current_page = page_class(
#             master=self.page_container,
#             **kwargs,
#         )
#         self.current_page.pack(fill="both", expand=True)

#     # =============================================================
#     # HOME PAGE
#     # =============================================================
#     def show_home_page(self) -> None:
#         self.switch_page(
#             HomePage,
#             on_navigate=self.handle_home_navigation,
#         )

#     # =============================================================
#     # HOME NAVIGATION
#     # =============================================================
#     def handle_home_navigation(self, destination: str) -> None:
#         if destination in ("folder"):
#             self.show_folder_page()
#         elif destination in ("document"):
#             self.show_doc_page()

#     # =============================================================
#     # FOLDER PAGE
#     # =============================================================
#     def show_folder_page(self) -> None:
#         self.switch_page(
#             FolderPage,
#             on_back=self.show_home_page,
#             on_next=self.show_ref_page,
#         )

#     # =============================================================
#     # REF PAGE
#     # =============================================================
#     def show_ref_page(self, data: dict) -> None:
#         self.switch_page(
#             RefPage,
#             data=data,
#             on_back=self.show_folder_page,
#             on_dashboard=self.show_home_page,
#         )

#     # =============================================================
#     # DOCUMENT PAGE
#     # =============================================================
#     def show_doc_page(self) -> None:
#         self.switch_page(
#             DocPage,
#             on_back=self.show_home_page,
#             on_next=self.show_ref_page,
#         )

#     # =============================================================
#     # MENU ACTIONS
#     # =============================================================
#     def on_new_project(self) -> None:
#         print("[MENU] New Project")

#     def on_open_database(self) -> None:
#         if hasattr(self, "db_window") and self.db_window.winfo_exists():
#             self.db_window.lift()
#             self.db_window.focus_set()
#         else:
#             self.db_window = DatabaseMonitorWindow(master=self)

#     # =============================================================
#     # WINDOW HELPERS
#     # =============================================================
#     def center_window(self, width: int, height: int) -> None:
#         self.update_idletasks()
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()

#         x = (screen_width // 2) - (width // 2)
#         y = (screen_height // 2) - (height // 2)
#         self.geometry(f"{width}x{height}+{x}+{y}")
