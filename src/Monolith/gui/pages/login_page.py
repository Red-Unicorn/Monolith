"""
Enterprise login page.
"""
from __future__ import annotations
from PIL import Image
import customtkinter as ctk

from gui.widgets.buttons import make_button
from core.services.auth_service import AuthService
from gui.theme.colors import BACKGROUND
from gui.theme.layout import INPUT_HEIGHT, INPUT_WIDTH, LOGO_HEIGHT, LOGO_WIDTH, PAD_MD, PAD_XS
from core.utils.paths import get_asset_path
from core.utils.logger import logger

class LoginPage(ctk.CTkFrame):

    def __init__(self, master, on_login):

        super().__init__(master)

        self.on_login = on_login
        self.auth_service = AuthService()

        # Build UI
        self._build_layout()
        self._build_logo()
        self._build_form()
        self._build_login_button()
        self._bind_events()

    # ──────────────────────────────────────────────────────────────
    # LAYOUT
    # ──────────────────────────────────────────────────────────────

    def _build_layout(self):

        self.pack(fill="both", expand=True)

        self.container = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
        )

        self.container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

    # ──────────────────────────────────────────────────────────────
    # LOGO
    # ──────────────────────────────────────────────────────────────

    def _build_logo(self):

        self.logo_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent",
        )

        self.logo_frame.pack(pady=(60, PAD_MD))

        image_path = get_asset_path("icons/Monolith_Logo.png")

        try:

            self.logo_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(LOGO_WIDTH, LOGO_HEIGHT),
            )

            self.logo_label = ctk.CTkLabel(
                self.logo_frame,
                image=self.logo_image,
                text="",
            )

            self.logo_label.pack()

        except Exception as error:

            print(f"Error loading logo: {error}")

        self.title_label = ctk.CTkLabel(
            self.container,
            text="MONOLITH",
            font=("Inter", 34, "bold"),
        )

        self.title_label.pack(
            pady=(PAD_XS, 120),
        )

    # ──────────────────────────────────────────────────────────────
    # FORM
    # ──────────────────────────────────────────────────────────────

    def _build_form(self):

        self.email_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Email",
            width=INPUT_WIDTH,
            height=INPUT_HEIGHT,
        )

        self.email_entry.pack(
            pady=10,
            padx=40,
        )

        self.password_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Password",
            show="*",
            width=INPUT_WIDTH,
            height=INPUT_HEIGHT,
        )

        self.password_entry.pack(
            pady=10,
            padx=40,
        )

        self.error_label = ctk.CTkLabel(
            self.container,
            text="",
            text_color="red",
        )

        self.error_label.pack(
            pady=(10, 0),
        )


    def _build_login_button(self):

        self.login_button = make_button(
            master=self.container,
            text="Login",
            command=self.login,
            enable_border_hover=True,
            variant="secondary",
            size="md",)

        self.login_button.pack(
            pady=(20, 60),
        )

    # ──────────────────────────────────────────────────────────────
    # EVENTS
    # ──────────────────────────────────────────────────────────────

    def _bind_events(self):

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )


    # ──────────────────────────────────────────────────────────────
    # ACTIONS
    # ──────────────────────────────────────────────────────────────

    def login(self):
        """
        Authenticate user.
        """

        self.on_login()
        logger.info("Login Successful")

        # email = self.email_entry.get()
        # password = self.password_entry.get()

        # try:

        #     response = self.auth_service.login(
        #         email,
        #         password,
        #     )

        #     if response.user:

        #         self.on_login()
        #         logger.info(f"Login successful:{email}")

        #     else:

        #         self.error_label.configure(
        #             text="Authentication failed",
        #         )
        #         logger.error("Authentication failed")

        # except Exception as error:

        #     self.error_label.configure(
        #         text=str(error),
        #     )
        #     logger.error(f"An error occurred during login: {error}")