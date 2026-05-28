import customtkinter as ctk
from gui.theme.layout import INPUT_HEIGHT, INPUT_WIDTH
from gui.theme.colors import INPUT_BG


def create_input_container(self, parent):
    frame = ctk.CTkFrame(
        parent, fg_color="#1E293B", height=INPUT_HEIGHT, width=INPUT_WIDTH
    )
    frame.pack_propagate(False)
    return frame
