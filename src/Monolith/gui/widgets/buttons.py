import customtkinter as ctk
from gui.theme.colors import BUTTON_STYLES
from gui.theme.layout import BUTTON_SIZES


def make_button(
    master,
    text: str,
    command=None,
    variant: str = "primary",
    size: str = "md",
    enable_border_hover: bool = True,
    width: int | None = None,
    height: int | None = None,
    font=("Inter", 12, "normal"),
    text_color="white",
    corner_radius=12,
):
    """
    Flexible button factory:
    - supports presets (sm/md/lg)
    - allows custom sizing override
    """

    fg_color, hover_color = BUTTON_STYLES.get(variant, BUTTON_STYLES["primary"])

    # ── SIZE LOGIC ──────────────────────────────────────────────
    if width is not None and height is not None:
        final_width = width
        final_height = height
    else:
        final_width, final_height = BUTTON_SIZES.get(size, BUTTON_SIZES["md"])

    button = ctk.CTkButton(
        master=master,
        text=text,
        command=command,

        width=final_width,
        height=final_height,

        fg_color=fg_color,
        border_width=2,

        # hover_color=hover_color,
        border_color=fg_color,

        text_color=text_color,
        font=font,
        corner_radius=corner_radius,
    )

    if enable_border_hover:
        button.bind(
            "<Enter>", lambda event, b=button: b.configure(border_color=hover_color, border_width=2)
        )

        button.bind(
            "<Leave>", lambda event, b=button: b.configure(border_color=fg_color, border_width=0)
        )
    else:
        button.bind(
            "<Enter>", lambda event, b=button: b.configure(border_color=fg_color, border_width=0)
        )

        button.bind(
            "<Leave>", lambda event, b=button: b.configure(border_color=fg_color, border_width=0)
        )

    return button