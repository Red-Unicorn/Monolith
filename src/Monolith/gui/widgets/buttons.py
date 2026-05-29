import customtkinter as ctk

from gui.theme.colors import BUTTON_STYLES
from gui.theme.layout import BUTTON_SIZES


def make_button(
    master,
    text: str,
    command=None,
    variant: str = "primary",
    size: str = "md",
    image=None,
    compound="left",
    enable_border_hover: bool = True,
    width: int | None = None,
    height: int | None = None,
    font=("Inter", 12, "normal"),
    text_color="white",
    corner_radius=12,
    anchor: str = "center",
    border_spacing: int = 10,
):

    fg_color, border_color, hover_color = BUTTON_STYLES.get(
        variant,
        BUTTON_STYLES["primary"],
    )

    # SIZE
    default_width, default_height = BUTTON_SIZES.get(
        size,
        BUTTON_SIZES["md"],
    )

    final_width = width if width is not None else default_width
    final_height = height if height is not None else default_height
    # if width is not None and height is not None:

    #     final_width = width
    #     final_height = height

    # else:

    #     final_width, final_height = BUTTON_SIZES.get(
    #         size,
    #         BUTTON_SIZES["md"],
    #     )

    # IMPORTANT:
    # keep SAME border width at all times
    # to avoid hover "jump"
    button = ctk.CTkButton(
        master=master,
        text=text,
        command=command,
        width=final_width,
        height=final_height,
        fg_color=fg_color,
        hover=False,  # disable default hover
        border_width=2,
        border_color=fg_color,
        text_color=text_color,
        font=font,
        corner_radius=corner_radius,
        image=image,
        compound=compound,
        anchor=anchor,
        border_spacing=border_spacing,
    )

    # CUSTOM HOVER
    if enable_border_hover:

        button.bind(
            "<Enter>",
            lambda event, b=button: b.configure(
                fg_color=hover_color,
                border_color=border_color,
            ),
        )

        button.bind(
            "<Leave>",
            lambda event, b=button: b.configure(
                fg_color=fg_color,
                border_color=fg_color,
            ),
        )

    else:

        button.bind(
            "<Enter>",
            lambda event, b=button: b.configure(
                fg_color=hover_color,
            ),
        )

        button.bind(
            "<Leave>",
            lambda event, b=button: b.configure(
                fg_color=fg_color,
            ),
        )

    return button


# import customtkinter as ctk
# from gui.theme.colors import BUTTON_STYLES
# from gui.theme.layout import BUTTON_SIZES


# def make_button(
#     master,
#     text: str,
#     command=None,
#     variant: str = "primary",
#     size: str = "md",
#     image=None,
#     compound="top",
#     enable_border_hover: bool = True,
#     width: int | None = None,
#     height: int | None = None,
#     font=("Inter", 12, "normal"),
#     text_color="white",
#     corner_radius=12,
# ):
#     """
#     Flexible button factory:
#     - supports presets (sm/md/lg)
#     - allows custom sizing override
#     """

#     fg_color, border_color, hover_color = BUTTON_STYLES.get(variant, BUTTON_STYLES["primary"])

#     # ── SIZE LOGIC ──────────────────────────────────────────────
#     if width is not None and height is not None:
#         final_width = width
#         final_height = height
#     else:
#         final_width, final_height = BUTTON_SIZES.get(size, BUTTON_SIZES["md"])

#     button = ctk.CTkButton(
#         master=master,
#         text=text,
#         command=command,

#         width=final_width,
#         height=final_height,

#         fg_color=fg_color,
#         border_width=2,

#         hover_color=hover_color,
#         border_color=fg_color,

#         text_color=text_color,
#         font=font,
#         corner_radius=corner_radius,
#         image=image,
#         compound=compound,
#     )

#     if enable_border_hover:
#         button.bind(
#             "<Enter>", lambda event, b=button: b.configure(fg_color=hover_color, border_color=border_color, border_width=2)
#         )

#         button.bind(
#             "<Leave>", lambda event, b=button: b.configure(fg_color=fg_color, border_color=fg_color, border_width=0)
#         )
#     else:
#         button.bind(
#             "<Enter>", lambda event, b=button: b.configure(fg_color=hover_color, border_color=fg_color, border_width=0)
#         )

#         button.bind(
#             "<Leave>", lambda event, b=button: b.configure(fg_color=fg_color, border_color=fg_color, border_width=0)
#         )

#     return button
