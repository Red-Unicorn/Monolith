"""
================================================================================
Module:        gui.components.tooltips
Description:   Dynamic, non-blocking floating overlay components for macOS UI.
Author:        Red Unicorn (Intl') Holding Group
License:       Proprietary – All rights reserved
Version:       1.0.0
================================================================================
"""

from __future__ import annotations
from typing import Optional, Union, Any
import customtkinter as ctk
import tkinter as tk

__all__ = ["CTkToolTip"]


class CTkToolTip:
    """
    A lightweight, asynchronous tooltip overlay framework for CustomTkinter.

    Tracks pointer movement relative to parent widget bounding fields to
    safely spawn and tear down native borderless micro-windows.
    """

    def __init__(
        self, widget: Union[ctk.CTkButton, ctk.CTkLabel, ctk.CTkFrame], text: str
    ) -> None:
        """
        Initialize the runtime state binding configuration for a tooltip target.

        Parameters
        ----------
        widget : Union[ctk.CTkButton, ctk.CTkLabel, ctk.CTkFrame]
            The UI instance targeted for pointer event interception.
        text : str
            The explicit context string bound to the display layer.
        """
        self.widget: Union[ctk.CTkButton, ctk.CTkLabel, ctk.CTkFrame] = widget
        self.text: str = text
        self.tooltip_window: Optional[ctk.CTkToplevel] = None

        # Bind core platform lifecycle events for pointer interception
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event: Optional[tk.Event] = None) -> None:
        """
        Intercept platform mouse enter events to construct and anchor the floating window.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            The low-level Tk system event object containing layout coordinates.
        """
        # Guard clause to protect against multi-render frames or empty strings
        if self.tooltip_window or not self.text:
            return

        # Compute absolute layout coordinate matrix offsets relative to hardware cursor
        x: int = self.widget.winfo_pointerx() + 15
        y: int = self.widget.winfo_pointery() + 10

        # Instantiate isolated top-level window frame over the master canvas
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.configure(fg_color="#1F1F1F")

        # Enforce non-stealing behavior for focus loops under macOS Aqua layer architecture
        if self.widget.winfo_toplevel().tk.call("tk", "windowingsystem") == "aqua":
            self.tooltip_window.attributes("-type", "tooltip")

        # Package structural rendering text inside the micro-frame container
        label: ctk.CTkLabel = ctk.CTkLabel(
            self.tooltip_window,
            text=self.text,
            corner_radius=4,
            fg_color="#1F1F1F",
            text_color="#FFFFFF",
            font=("Inter", 12),
            padx=8,
            pady=4,
        )
        label.pack()

    def hide_tooltip(self, event: Optional[tk.Event] = None) -> None:
        """
        Intercept platform leave loops to drop down and clear active memory stacks.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            The core Tk pointer event signaling cross-boundary displacement.
        """
        # Purge references from layout frames to stabilize memory structures
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# Second Version of tooltip
class ToolTip:
    def __init__(self, widget, text_getter):
        self.widget = widget
        self.text_getter = text_getter
        self.tip = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        text = self.text_getter()
        if not text:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tip,
            text=text,
            bg="black",
            fg="white",
            padx=6,
            pady=4
        )
        label.pack()

    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None