"""
Enterprise login page.
"""

from __future__ import annotations
from PIL import Image
import customtkinter as ctk
import tkinter as tk  # <-- Imported for the BooleanVar state tracker
from datetime import datetime

from gui.widgets.buttons import make_button
from core.services.auth_service import AuthService
from gui.theme.colors import BACKGROUND, INPUT_BACKGROUND, BUTTON_SECONDARY
from gui.theme.layout import (
    INPUT_HEIGHT,
    INPUT_WIDTH,
    LOGO_HEIGHT,
    LOGO_WIDTH,
    PAD_MD,
    PAD_XS,
)
from core.utils.paths import get_asset_path
from core.utils.logger import logger
from core.services.auth_storage import (
    save_secure_token,
    save_local_username,
    load_local_username,
    clear_local_username,
    clear_secure_token,
    save_password,
    load_password,
)


class LoginPage(ctk.CTkFrame):

    def __init__(self, master, on_login):

        super().__init__(master)

        self.on_login = on_login
        self.auth_service = AuthService()
        # Loading images
        self.eye_open_img = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/eye-open-w.png")),
            dark_image=Image.open(get_asset_path("icons/eye-open-w.png")),
            size=(25, 25),
        )

        self.eye_closed_img = ctk.CTkImage(
            light_image=Image.open(get_asset_path("icons/eye-closed-w.png")),
            dark_image=Image.open(get_asset_path("icons/eye-closed-w.png")),
            size=(25, 25),
        )
        # Build UI
        self._build_layout()
        self._build_logo()
        self._build_form()
        self._build_login_button()
        self._build_footer()
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

            logger.debug(f"Error loading logo: {error}")

        self.title_label = ctk.CTkLabel(
            self.container,
            text="MONOLITH",
            font=("Inter", 34, "bold"),
        )

        self.title_label.pack(
            pady=(PAD_XS, 10),
        )
        self.subtitle_label = ctk.CTkLabel(
            self.container,
            text="Please sign in to continue",
            font=("Inter", 14),
            text_color="#94A3B8",
            fg_color="transparent",
        )

        self.subtitle_label.pack(
            pady=(0, 40),
        )

    # ──────────────────────────────────────────────────────────────
    # FORM
    # ──────────────────────────────────────────────────────────────

    def _build_form(self):

        self.error_label = ctk.CTkLabel(
            self.container,
            text="",
            text_color="red",
        )

        self.error_label.pack(
            pady=(10, 0),
        )

        self.email_label = ctk.CTkLabel(
            self.container,
            text="Email",
            font=("Inter", 13),
            text_color="#E2E8F0",
            fg_color="transparent",
        )

        self.email_label.pack(
            anchor="w",
            padx=40,
        )
        self.email_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Email",
            width=INPUT_WIDTH,
            height=INPUT_HEIGHT,
            fg_color=INPUT_BACKGROUND,  # "#303e4e",  # "#1E293B",
            font=("Inter", 14),
            border_width=0,
        )

        self.email_entry.pack(
            pady=(0, 10),
            padx=40,
        )

        # PASSWORD LABEL
        self.password_label = ctk.CTkLabel(
            self.container,
            text="Password",
            font=("Inter", 13),
            text_color="#E2E8F0",
            fg_color="transparent",
        )

        self.password_label.pack(
            anchor="w",
            padx=40,
            pady=(0, 0),
        )

        # PASSWORD FRAME
        self.password_frame = ctk.CTkFrame(
            self.container,
            fg_color=INPUT_BACKGROUND,  # "#303e4e",
            corner_radius=6,
        )

        self.password_frame.pack(
            padx=40,
            pady=(0, 10),
        )

        # PASSWORD ENTRY
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            show="•",
            width=INPUT_WIDTH - 60,
            height=INPUT_HEIGHT,
            font=("Inter", 13),
            border_width=0,
            fg_color="transparent",
        )

        self.password_entry.pack(side="left", padx=(10, 0))

        # PASSWORD VISIBILITY STATE
        self.password_visible = False

        # EYE BUTTON
        self.show_password_button = ctk.CTkButton(
            self.password_frame,
            text="",
            image=self.eye_open_img,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#334155",
            command=self.toggle_password_visibility,
        )

        self.show_password_button.pack(
            side="right",
            padx=5,
        )

        # Track checkbox state
        self.remember_me_var = tk.BooleanVar(value=False)

        # Styled Checkbox matching the slate dark/coral web mockup theme
        self.remember_checkbox = ctk.CTkCheckBox(
            self.container,
            text="Remember me",
            variable=self.remember_me_var,
            font=("Inter", 13),
            text_color="#94A3B8",  # Slate gray text
            fg_color=BUTTON_SECONDARY,  # Accent fill color when checked
            hover_color=BUTTON_SECONDARY,  # Deep red hover boundary state
            border_color=INPUT_BACKGROUND,  # "#334155",  # Subtle borders matching input text boxes
            corner_radius=2,
            checkbox_width=16,
            checkbox_height=16,
        )
        self.remember_checkbox.pack(padx=40, pady=(0, 10), anchor="w")

        saved_email = load_local_username()

        if saved_email:

            self.email_entry.insert(
                0,
                saved_email,
            )

            saved_password = load_password(saved_email)

            if saved_password:

                self.password_entry.insert(
                    0,
                    saved_password,
                )

            self.remember_me_var.set(True)

    def _build_login_button(self):

        self.login_button = make_button(
            master=self.container,
            text="Sign in",
            command=self.login,
            enable_border_hover=True,
            variant="secondary",
            size="md",
        )

        self.login_button.pack(
            pady=(0, 60),
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

    def _build_footer(self):

        self.footer_label = ctk.CTkLabel(
            self,
            text=f"© MONOLITH — {datetime.now().year}",
            font=("Inter Light", 10),
            # text_color=TEXT_MUTED,
            fg_color=BACKGROUND,
        )

        self.footer_label.place(
            relx=0.5,
            rely=0.98,
            anchor="s",
        )

    def toggle_password_visibility(self):

        self.password_visible = not self.password_visible

        if self.password_visible:

            self.password_entry.configure(show="")
            self.show_password_button.configure(image=self.eye_closed_img)

        else:

            self.password_entry.configure(show="•")
            self.show_password_button.configure(image=self.eye_open_img)

    def login(self):
        """
        Authenticate user.
        """

        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        remember_checked = self.remember_me_var.get()

        try:

            response = self.auth_service.login(
                email,
                password,
            )

            if response.user:

                logger.info(f"Login successful: {email}")

                session = response.session

                refresh_token = None

                if session:

                    refresh_token = session.refresh_token
                    if remember_checked:

                        save_local_username(email)

                        save_password(
                            email,
                            password,
                        )

                    else:

                        clear_local_username()
                        clear_secure_token(email)

                # ENTER APPLICATION
                self.on_login()

            else:

                self.error_label.configure(
                    text="Authentication failed",
                )

                logger.error("Authentication failed")

        except Exception as error:

            self.error_label.configure(
                text=str(error),
            )

            logger.error(f"An error occurred during login: {error}")
