"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.pages.home_page
DESCRIPTION:   Streamlined single-action home operational hub. Removed wizard
               pipelines and multi-frame trackers for step-by-step clarity.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       7.0.0
================================================================================
"""

from __future__ import annotations
from typing import Any, Optional
import customtkinter as ctk
from PIL import Image

# ── Design System Injections ──────────────────────────────────────────────────
from gui.widgets.buttons import make_button
from core.utils.paths import get_asset_path
from gui.theme.colors import BACKGROUND, TEXT_MUTED, TEXT_BIS, TEXT
from gui.theme.layout import APP_WIDTH, APP_HEIGHT




# ──────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ──────────────────────────────────────────────────────────────────────────────


class HomePage(ctk.CTkFrame):
    """
    Main wizard entry page.

    Presents the user with two large workflow choices:
    1. Project / Resource flow
    2. Document flow

    Designed for:
    - accessibility
    - large interaction targets
    - low cognitive load
    - future multi-step navigation
    """

    def __init__(self, master, on_navigate=None):
        super().__init__(master, fg_color=BACKGROUND)

        self.on_navigate = on_navigate

        # ──────────────────────────────────────────────────────────────────
        # PAGE LAYOUT
        # ──────────────────────────────────────────────────────────────────

        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)

        # ──────────────────────────────────────────────────────────────────
        # HEADER / STEP INDICATOR
        # ──────────────────────────────────────────────────────────────────

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.header_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=(0, 0),
        )

        self.step_label = ctk.CTkLabel(
            self.header_frame,
            text="STEP 1 OF 3",
            font=("Oswald", 18, "bold"),
            text_color=TEXT_MUTED,
        )
        self.step_label.pack(anchor="w")#,pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Create Reference Number for:",
            font=("PT Sans", 12, "bold"),
            text_color=TEXT,
        )
        self.title_label.pack(anchor="w")#, pady=(10, 0))

        # self.subtitle_label = ctk.CTkLabel(
        #     self.header_frame,
        #     text="Underping ?",
        #     font=("Arial", 12),
        #     text_color=MUTED,
        # )
        # self.subtitle_label.pack(anchor="w", pady=(10, 0))

        # ──────────────────────────────────────────────────────────────────
        # MAIN CONTENT
        # ──────────────────────────────────────────────────────────────────

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            # padx=20,
            pady=20,
            padx=60,
            # pady=(20, 20),
        )

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # ──────────────────────────────────────────────────────────────────
        # PROJECT / RESOURCE BUTTON
        # ──────────────────────────────────────────────────────────────────

        folder_icon = ctk.CTkImage(
        light_image=Image.open(get_asset_path("icons/folder.png")),
        dark_image=Image.open(get_asset_path("icons/folder.png")),
        size=(64, 64),
        )
        
        self.folder_button = make_button(
            master=self.content_frame,
            text="PROJECT/RESOURCE",
            command=self._handle_project_workflow,
            enable_border_hover=True,
            image=folder_icon,
            variant="primary",
            size="lg",)

        self.folder_button.grid(
            row=0,
            column=0,
            padx=(0, 20),
            # pady=20,
            sticky="nsew",
        )
        
        # self.project_button = ctk.CTkButton(
        #     self.content_frame,
        #     text="PROJECT / RESOURCE",
        #     font=("Arial", 10, "bold"),
        #     width=200,
        #     height=200,
        #     corner_radius=12,
        #     fg_color=PRIMARY,
        #     hover_color=PRIMARY_HOVER,
        #     text_color=TEXT,
        #     command=self._handle_project_workflow,
        # )

        # self.project_button.grid(
        #     row=0,
        #     column=0,
        #     padx=(0, 20),
        #     pady=20,
        #     sticky="nsew",
        # )

        # ──────────────────────────────────────────────────────────────────
        # DOCUMENT BUTTON
        # ──────────────────────────────────────────────────────────────────

        document_icon = ctk.CTkImage(
        light_image=Image.open(get_asset_path("icons/file.png")),
        dark_image=Image.open(get_asset_path("icons/file.png")),
        size=(64, 64),
        )

        self.document_button = make_button(
            master=self.content_frame,
            text="DOCUMENTS",
            command=self._handle_project_workflow,
            enable_border_hover=True,
            image=document_icon,
            variant="primary",
            size="lg",)
        
        # self.document_button = ctk.CTkButton(
        #     self.content_frame,
        #     text="DOCUMENT",
        #     font=("Arial", 10, "bold"),
        #     width=200,
        #     height=200,
        #     corner_radius=12,
        #     fg_color=SECONDARY,
        #     hover_color=SECONDARY_HOVER,
        #     text_color=TEXT,
        #     command=self._handle_document_workflow,
        # )

        self.document_button.grid(
            row=0,
            column=1,
            padx=(20, 0),
            # pady=20,
            sticky="nsew",
        )

    # ──────────────────────────────────────────────────────────────────────
    # ACTIONS
    # ──────────────────────────────────────────────────────────────────────

    def _handle_project_workflow(self) -> None:
        """
        Navigate to project/resource workflow.
        """
        print("[NAVIGATION] Project workflow selected.")

        if self.on_navigate:
            self.on_navigate("project")

    def _handle_document_workflow(self) -> None:
        """
        Navigate to document workflow.
        """
        print("[NAVIGATION] Document workflow selected.")

        if self.on_navigate:
            self.on_navigate("document")

# class HomePage(ctk.CTkFrame):
#     """
#     Unified Application View managing a single clean operational sheet.
#     Eliminates wizard stepper logic to track operations step-by-step manually.
#     """

#     def __init__(self, master: ctk.CTk) -> None:
#         super().__init__(master, fg_color="transparent")

#         # Core state tracking variable if you still want to log progress/steps
#         self.current_step = 0

#         # ── HOME SCREEN: TWO BUTTONS CENTERED AT 80% WIDTH ──────────────────
#         self.button_panel = ctk.CTkFrame(self, fg_color="transparent")
#         self.button_panel.pack(fill="both", expand=True, padx=30, pady=30)

#         button_width = int(APP_WIDTH * 0.8)
#         button_height = int(APP_HEIGHT * 0.8)
#         self.home_button_group = ctk.CTkFrame(
#             self.button_panel,
#             fg_color=BG_BLUE,
#             corner_radius=16,
#             border_width=1,
#             border_color=BG_BLUE,
#         )
#         self.home_button_group.place(relx=0.5, rely=0.5, anchor="center")

#         self.btn_secondary = ctk.CTkButton(
#             self.home_button_group,
#             text="Secondary Action",
#             width=button_width,
#             height=button_height,#48,
#             fg_color=BG_BLUE,
#             hover_color=BG_BLUE,
#             text_color=TEXT,
#             command=self._handle_secondary_action,
#         )
#         self.btn_secondary.grid(row=0, column=0, padx=(24, 12), pady=24)

#         self.btn_action = ctk.CTkButton(
#             self.home_button_group,
#             text="Primary Action",
#             width=button_width,
#             height=48,
#             fg_color=RU_BLUE,
#             hover_color=RU,
#             text_color=TEXT,
#             command=self._handle_action_trigger,
#         )
#         self.btn_action.grid(row=0, column=1, padx=(12, 24), pady=24)

#     # ── LOGIC DATA CONTROLLER PASS CHANNELS ───────────────────────────────────

#     def _handle_secondary_action(self) -> None:
#         """
#         Handle a second post-login action button click.
#         """
#         print("[ACTION] Secondary action clicked.")
#         self.lbl_q.configure(text="Secondary action triggered.")

#     def _handle_action_trigger(self) -> None:
#         """
#         Primary home action callback.
#         """
#         self.current_step += 1
#         print(f"[ACTION] Primary action clicked. step={self.current_step}")

#         if self.current_step == 1:
#             self.btn_action.configure(text="Action Confirmed")
#         else:
#             self.btn_action.configure(text="Primary Action")
#             self.current_step = 0


# """
# ================================================================================
# PROJECT:       Monolith Application Engine
# MODULE:        gui.pages.home_page
# DESCRIPTION:   Streamlined home operational hub built around an explicit multi-frame
#                stepper pipeline. Eliminates grid weight layout conflicts by
#                isolating card grids from dropdown list forms. Fully valid geometry
#                parameters only.
# AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
# LICENSE:       Proprietary – All rights reserved
# VERSION:       6.1.0
# ================================================================================
# """

# from __future__ import annotations
# from typing import Any, Dict, List, Optional
# import customtkinter as ctk
# from PIL import Image

# # ── Design System Injections, Tooltips, and Path Resolvers ────────────────────
# from gui.theme.colors import *
# from gui.widgets.tooltips import CTkToolTip
# from core.utils.paths import get_asset_path
# from gui.widgets.combobox_multiselect import CTkComboboxMultiSelect

# # Import data routing arrays
# from gui.pages.wizard_const import (
#     MONOLITH_MASTER_STEPS,
#     ANALYTICS_SUB_STEPS,
#     DATABASE_SUB_STEPS,
#     FIREWALL_SUB_STEPS,
# )

# __all__ = ["HomePage"]


# class HomePage(ctk.CTkFrame):
#     """
#     Unified Application View managing a 3-stage visual stepper workflow.
#     Uses independent sub-frame canvases to completely eliminate geometry manager bugs.
#     """

#     def __init__(self, master: ctk.CTk) -> None:
#         super().__init__(master, fg_color="transparent")

#         # Core workflow tracking variables
#         self.base_steps = MONOLITH_MASTER_STEPS
#         self.active_steps = list(self.base_steps)
#         self.current_step = 0
#         self.user_responses: Dict[int, Any] = {}

#         # UI Element pointer references
#         self.input_widget: Optional[
#             ctk.CTkFrame | ctk.CTkOptionMenu | CTkComboboxMultiSelect
#         ] = None
#         self.card_buttons: List[ctk.CTkButton] = []
#         self.stepper_indicators: List[ctk.CTkLabel] = []
#         self.stepper_labels: List[ctk.CTkLabel] = []

#         # ── FIXED VERTICAL PACK FRAMEWORK ─────────────────────────────────────
#         # Root layout uses pack exclusively to keep global zones separated cleanly.

#         # ── ZONE 1: VISUAL STEPPER TRACK METADATA BAR ──
#         self.stepper_track_frame = ctk.CTkFrame(self, fg_color="transparent")
#         self.stepper_track_frame.pack(fill="x", side="top", padx=30, pady=(25, 15))
#         self.stepper_track_frame.grid_rowconfigure(0, weight=0)
#         self.stepper_track_frame.grid_columnconfigure((0, 2, 4), weight=1)

#         self._instantiate_visual_stepper_nodes()

#         # ── ZONE 2: ACTIVE DYNAMIC CONTENT FRAMES (PRERENDERED SEPARATELY) ──
#         # By separating these into dedicated master frames, grid layout weights can never clash.
#         self.canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
#         self.canvas_frame.pack(fill="both", expand=True, padx=30, pady=10)

#         self.hub_deck_frame = ctk.CTkFrame(self.canvas_frame, fg_color="transparent")
#         self.form_sheet_frame = ctk.CTkFrame(
#             self.canvas_frame,
#             fg_color=CARD,
#             corner_radius=12,
#             border_width=1,
#             border_color=BORDER,
#         )

#         # ── ZONE 3: PERSISTENT FOOTER NAVIGATION CONTROL BAR ──
#         self.footer_bar = ctk.CTkFrame(self, fg_color="transparent")
#         self.footer_bar.pack(fill="x", side="bottom", padx=30, pady=(15, 30))

#         self.btn_next = ctk.CTkButton(
#             self.footer_bar,
#             text="Next Step",
#             fg_color=RU_BLUE,
#             hover_color=RU,
#             text_color=TEXT,
#             command=self._handle_next_navigation,
#         )
#         self.btn_back = ctk.CTkButton(
#             self.footer_bar,
#             text="Back",
#             fg_color="transparent",
#             text_color=TEXT_SECONDARY,
#             hover_color=CARD_HOVER,
#             command=self._handle_back_navigation,
#         )

#         # Global click focus listener safely closing multiselect panels
#         self.master.bind(
#             "<Button-1>", lambda e: self._evaluate_focus_escape(e), add="+"
#         )

#         # Initialize the baseline workflow pass
#         self._render_current_step()

#     # ── STEPPER CONTROLLER CONSTRUCTORS ───────────────────────────────────────

#     def _instantiate_visual_stepper_nodes(self) -> None:
#         """Draws the fixed milestone badges and text onto the stepper panel."""
#         step_definitions = ["1. Choose Vector", "2. Select Dropdowns", "3. Get Results"]

#         col_index = 0
#         for i, label_text in enumerate(step_definitions):
#             node_group = ctk.CTkFrame(self.stepper_track_frame, fg_color="transparent")
#             # 💡 FIX: Removed sticky="center". Leaving it blank forces natural default centering!
#             node_group.grid(row=0, column=col_index)

#             # Simulated Circle Bubble (Width == Height with half corner_radius)
#             indicator = ctk.CTkLabel(
#                 node_group,
#                 text=str(i + 1),
#                 font=("Inter", 11, "bold"),
#                 width=24,
#                 height=24,
#                 corner_radius=12,
#                 fg_color="#1E293B",
#                 text_color="#FFFFFF",
#             )
#             indicator.pack(side="left", padx=(0, 6))
#             self.stepper_indicators.append(indicator)

#             lbl = ctk.CTkLabel(
#                 node_group,
#                 text=label_text,
#                 font=("Inter", 12, "normal"),
#                 text_color=TEXT_SECONDARY,
#             )
#             lbl.pack(side="left")
#             self.stepper_labels.append(lbl)

#             if i < len(step_definitions) - 1:
#                 col_index += 1
#                 line_bar = ctk.CTkFrame(
#                     self.stepper_track_frame, height=2, fg_color="#334155"
#                 )
#                 line_bar.grid(row=0, column=col_index, sticky="ew", padx=12)

#             col_index += 1

#     def _update_visual_stepper_states(self) -> None:
#         """Evaluates workflow steps and sets badge styles to white outlines vs green."""
#         # Condition Maps
#         step_1_passed = 0 in self.user_responses
#         step_2_passed = len(self.user_responses) > 1 and self.current_step == 2

#         # ── CONFIGURING STEP 1 BUBBLE ──
#         if step_1_passed:
#             self.stepper_indicators[0].configure(
#                 fg_color="#22C55E", text_color="#FFFFFF"
#             )  # Active Emerald
#             self.stepper_labels[0].configure(
#                 text_color="#22C55E", font=("Inter", 12, "bold")
#             )
#         else:
#             self.stepper_indicators[0].configure(
#                 fg_color="#1E293B", text_color="#FFFFFF"
#             )
#             if self.current_step == 0:
#                 self.stepper_labels[0].configure(
#                     text_color="#FFFFFF", font=("Inter", 12, "bold")
#                 )

#         # ── CONFIGURING STEP 2 BUBBLE ──
#         if step_2_passed:
#             self.stepper_indicators[1].configure(
#                 fg_color="#22C55E", text_color="#FFFFFF"
#             )
#             self.stepper_labels[1].configure(
#                 text_color="#22C55E", font=("Inter", 12, "bold")
#             )
#         else:
#             self.stepper_indicators[1].configure(
#                 fg_color="#1E293B", text_color="#FFFFFF"
#             )
#             if self.current_step == 1:
#                 self.stepper_labels[1].configure(
#                     text_color="#FFFFFF", font=("Inter", 12, "bold")
#                 )
#             else:
#                 self.stepper_labels[1].configure(
#                     text_color=TEXT_SECONDARY, font=("Inter", 12, "normal")
#                 )

#         # ── CONFIGURING STEP 3 BUBBLE ──
#         if self.current_step == 2:
#             self.stepper_indicators[2].configure(
#                 fg_color="#1E293B", text_color="#FFFFFF"
#             )
#             self.stepper_labels[2].configure(
#                 text_color="#FFFFFF", font=("Inter", 12, "bold")
#             )
#         else:
#             self.stepper_indicators[2].configure(
#                 fg_color="#1E293B", text_color="#FFFFFF"
#             )
#             self.stepper_labels[2].configure(
#                 text_color=TEXT_SECONDARY, font=("Inter", 12, "normal")
#             )

#     # ── ROUTER CONTENT UPDATE PIPELINES ───────────────────────────────────────

#     def _render_current_step(self) -> None:
#         """Toggles layout panel states cleanly without mixing internal geometry tokens."""
#         self._update_visual_stepper_states()

#         # Unmount active frames out of geometry manager visibility loops
#         self.hub_deck_frame.pack_forget()
#         self.form_sheet_frame.pack_forget()

#         # Clear sub-widgets inside containers to refresh data values
#         for child in self.hub_deck_frame.winfo_children():
#             child.destroy()
#         for child in self.form_sheet_frame.winfo_children():
#             child.destroy()

#         self.input_widget = None
#         self.card_buttons.clear()

#         # Read step configurations
#         step_data = self.active_steps[self.current_step]

#         # Handle footer navigation visibility states
#         if self.current_step == 0:
#             self.btn_back.pack_forget()
#             self.btn_next.pack_forget()
#         else:
#             self.btn_next.pack(side="right", padx=(10, 0))
#             self.btn_back.pack(side="right")
#             self.btn_next.configure(
#                 text=(
#                     "Finish and Deploy"
#                     if self.current_step == len(self.active_steps) - 1
#                     else "Next Step"
#                 )
#             )

#         # ── RENDER CONDITION BRANCHES ─────────────────────────────────────────

#         # 💡 STEP 1 HUB: Draw the three large core vector buttons
#         if step_data["type"] == "cards":
#             self.hub_deck_frame.pack(fill="both", expand=True)
#             self.hub_deck_frame.grid_rowconfigure(0, weight=1)
#             self.hub_deck_frame.grid_columnconfigure((0, 1, 2), weight=1)

#             image_path = get_asset_path("icons/database.png")
#             try:
#                 card_img = ctk.CTkImage(
#                     light_image=Image.open(image_path), size=(64, 64)
#                 )
#             except Exception:
#                 card_img = None

#             for idx, option in enumerate(step_data["options"]):
#                 btn = ctk.CTkButton(
#                     self.hub_deck_frame,
#                     text=option,
#                     image=card_img,
#                     compound="top",
#                     font=("Inter", 14, "bold"),
#                     text_color=TEXT_SECONDARY,
#                     width=180,
#                     height=180,
#                     corner_radius=12,
#                     fg_color=RU_BLUE_LIGHT,
#                     hover_color=RU,
#                     border_width=2,
#                     border_color=RU_BLUE_LIGHT,
#                     border_spacing=0,
#                     anchor="n",
#                 )
#                 btn.grid(row=0, column=idx, padx=15, pady=20)
#                 btn.configure(command=lambda opt=option: self._handle_card_click(opt))

#                 btn.bind(
#                     "<Enter>",
#                     lambda _, b=btn: b.configure(
#                         fg_color=RU, border_color=BORDER_HOVER, text_color="#FFFFFF"
#                     ),
#                     add="+",
#                 )
#                 btn.bind(
#                     "<Leave>",
#                     lambda _, b=btn: b.configure(
#                         fg_color=RU_BLUE_LIGHT,
#                         border_color=RU_BLUE_LIGHT,
#                         text_color=TEXT_SECONDARY,
#                     ),
#                     add="+",
#                 )
#                 self.card_buttons.append(btn)

#         # 💡 STEP 2 & 3 FORMS: Draw clean vertical selection layouts
#         else:
#             self.form_sheet_frame.pack(fill="both", expand=True, pady=10)

#             lbl_q = ctk.CTkLabel(
#                 self.form_sheet_frame,
#                 text=step_data["question"],
#                 font=("Inter", 16, "bold"),
#                 text_color=TEXT,
#                 justify="left",
#             )
#             lbl_q.pack(anchor="w", padx=30, pady=(30, 5))

#             lbl_d = ctk.CTkLabel(
#                 self.form_sheet_frame,
#                 text=step_data["description"],
#                 font=("Inter", 12, "normal"),
#                 text_color=TEXT_SECONDARY,
#                 justify="left",
#                 wraplength=520,
#             )
#             lbl_d.pack(anchor="w", padx=30, pady=(0, 25))

#             prev_val = self.user_responses.get(self.current_step, None)
#             w_type = step_data["type"]

#             if w_type == "radio":
#                 radio_container = ctk.CTkFrame(
#                     self.form_sheet_frame, fg_color="transparent"
#                 )
#                 radio_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
#                 self.radio_var = ctk.StringVar(
#                     value=prev_val or step_data["options"][0]
#                 )
#                 for opt in step_data["options"]:
#                     rb = ctk.CTkRadioButton(
#                         radio_container,
#                         text=opt,
#                         variable=self.radio_var,
#                         value=opt,
#                         fg_color=RU,
#                         text_color=TEXT,
#                     )
#                     rb.pack(anchor="w", pady=6)
#                 self.input_widget = radio_container

#             elif w_type == "dropdown":
#                 self.dropdown_var = ctk.StringVar(
#                     value=prev_val or step_data["options"][0]
#                 )
#                 self.input_widget = ctk.CTkOptionMenu(
#                     self.form_sheet_frame,
#                     variable=self.dropdown_var,
#                     values=step_data["options"],
#                     fg_color=CARD_HOVER,
#                     button_color=RU_BLUE,
#                     button_hover_color=RU,
#                 )
#                 self.input_widget.pack(anchor="w", padx=30, pady=(0, 30))

#             elif w_type == "multiselect":
#                 saved_arr = prev_val if isinstance(prev_val, list) else []
#                 self.input_widget = CTkComboboxMultiSelect(
#                     self.form_sheet_frame, options=step_data["options"]
#                 )
#                 self.input_widget.pack(fill="x", anchor="w", padx=30, pady=(0, 30))
#                 if saved_arr:
#                     self.input_widget.set_selected(saved_arr)

#     # ── LOGIC DATA CONTROLLER PASS CHANNELS ───────────────────────────────────

#     def _handle_card_click(self, selected_hub: str) -> None:
#         """Forks database sub-steps instantly based on current card selections."""
#         self.user_responses[0] = selected_hub

#         if selected_hub == "Analytics Engine":
#             self.active_steps = MONOLITH_MASTER_STEPS + ANALYTICS_SUB_STEPS
#         elif selected_hub == "Database Clusters":
#             self.active_steps = MONOLITH_MASTER_STEPS + DATABASE_SUB_STEPS
#         elif selected_hub == "Network Firewall":
#             self.active_steps = MONOLITH_MASTER_STEPS + FIREWALL_SUB_STEPS

#         self.current_step = 1
#         self._render_current_step()

#     def _save_form_response(self) -> None:
#         """Extracts and writes state parameters into data registers safely."""
#         if self.current_step == 0 or not self.input_widget:
#             return

#         w_type = self.active_steps[self.current_step]["type"]
#         if w_type == "radio":
#             self.user_responses[self.current_step] = self.radio_var.get()
#         elif w_type == "dropdown":
#             self.user_responses[self.current_step] = self.dropdown_var.get()
#         elif w_type == "multiselect":
#             self.user_responses[self.current_step] = self.input_widget.get_selected()

#     def _handle_next_navigation(self) -> None:
#         self._save_form_response()
#         if self.current_step < len(self.active_steps) - 1:
#             self.current_step += 1
#             self._render_current_step()
#         else:
#             print(
#                 f"[DEPLOYMENT] Committing master operations matrix mapping: {self.user_responses}"
#             )
#             self.current_step = 0
#             self.user_responses.clear()
#             self.active_steps = list(self.base_steps)
#             self._render_current_step()

#     def _handle_back_navigation(self) -> None:
#         self._save_form_response()
#         if self.current_step > 0:
#             self.current_step -= 1
#             self._render_current_step()

#     def _evaluate_focus_escape(self, event: Any) -> None:
#         """Closes custom multiselect panels safely if user clicks outside boundaries."""
#         if (
#             self.input_widget
#             and isinstance(self.input_widget, CTkComboboxMultiSelect)
#             and self.input_widget.is_dropped
#         ):
#             x = event.x_root
#             w_x = self.input_widget.winfo_rootx()
#             if not (w_x <= x <= w_x + self.input_widget.winfo_width()):
#                 self.input_widget._close_dropdown()
#                 self.focus_set()
