To implement a step-by-step questionnaire behind each button, you need a **Wizard Pattern**. Instead of multiplying your files or spawning messy popup windows, the cleanest architectural approach is to design a single, reusable `WizardPage` frame.

When a user clicks one of your primary hub buttons (like the Analytics Engine), your master window manager will swap the view to this wizard, passing in a custom array of question data.

Here is the production-grade architecture to build this, utilizing a state tracking index to handle step-by-step navigation smoothly.

---

### Step 1: Define Your Question Data Structure

First, map out the data schema for your wizards. Each wizard requires an array of step objects containing a question, helper text, input style, and configuration choices.

```python
# gui/constants/wizard_data.py

ANALYTICS_WIZARD_STEPS = [
    {
        "question": "What is your primary analytical data target?",
        "description": "Select the core metric stream you wish to isolate for Monolith tracking data.",
        "type": "radio",
        "options": ["Realtime Network Latency", "Database Operational Load", "User Auth Event Logs"]
    },
    {
        "question": "Select your preferred date-range aggregation window",
        "description": "Larger metrics scale blocks require additional processing pipelines.",
        "type": "dropdown",
        "options": ["Last 24 Hours", "7-Day History Matrix", "30-Day Snapshot Archive"]
    },
    {
        "question": "Enable hardware-accelerated rendering models?",
        "description": "Optimizes live charts directly on your host machine GPU threads.",
        "type": "checkbox",
        "label": "Activate local acceleration pipelines"
    }
]

```

---

### Step 2: Create the Reusable Wizard Interface Frame

This dynamic frame class tracks the current active question index (`self.current_step`), renders the correct input widget type on the fly, and manages the state transitions of the **Back**, **Next**, and **Finish** navigation buttons.

```python
"""
================================================================================
Module:        gui.pages.wizard_page
Description:   Reusable multi-step sequential wizard interface for data collection.
Author:        Red Unicorn (Intl') Holding Group
Version:       1.0.0
================================================================================
"""

from __future__ import annotations
from typing import Any, dict, list
import customtkinter as ctk
from gui.theme.colors import *

class WizardPage(ctk.CTkFrame):
    def __init__(self, master: Any, wizard_title: str, steps: list[dict[str, Any]], on_complete_callback: Any, on_cancel_callback: Any) -> None:
        super().__init__(master, fg_color="transparent")
        
        self.steps = steps
        self.current_step = 0
        self.user_responses: dict[int, Any] = {}
        self.on_complete = on_complete_callback
        self.on_cancel = on_cancel_callback
        
        # UI State variables
        self.input_widget: Any = None
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Central Question Canvas Zone
        self.grid_rowconfigure(2, weight=0)  # Footer Control Bar
        self.grid_columnconfigure(0, weight=1)
        
        # ── HEADER ROW ──
        self.header_label = ctk.CTkLabel(self, text=wizard_title.upper(), font=("Inter", 20, "bold"), text_color=TEXT)
        self.header_label.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="w")
        
        self.progress_label = ctk.CTkLabel(self, text="", font=("Inter", 12, "normal"), text_color=TEXT_SECONDARY)
        self.progress_label.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="e")
        
        # ── CENTRAL QUESTION CANVAS ──
        self.canvas_frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
        self.canvas_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_question = ctk.CTkLabel(self.canvas_frame, text="", font=("Inter", 16, "bold"), text_color=TEXT, wraplength=500, justify="left")
        self.lbl_question.pack(anchor="w", padx=30, pady=(30, 5))
        
        self.lbl_desc = ctk.CTkLabel(self.canvas_frame, text="", font=("Inter", 12, "normal"), text_color=TEXT_SECONDARY, wraplength=500, justify="left")
        self.lbl_desc.pack(anchor="w", padx=30, pady=(0, 25))
        
        # Interactive Content Slot Container
        self.input_container = ctk.CTkFrame(self.canvas_frame, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # ── FOOTER ROW NAVIGATION ──
        self.footer_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_bar.grid(row=2, column=0, padx=30, pady=(15, 30), sticky="ew")
        
        self.btn_cancel = ctk.CTkButton(self.footer_bar, text="Cancel", fg_color="transparent", border_width=1, border_color=BORDER, text_color=TEXT, hover_color=CARD_HOVER, command=self.on_cancel)
        self.btn_cancel.pack(side="left")
        
        self.btn_next = ctk.CTkButton(self.footer_bar, text="Next", fg_color=RU_BLUE, hover_color=RU, text_color=TEXT, command=self._next_step)
        self.btn_next.pack(side="right", padx=(10, 0))
        
        self.btn_back = ctk.CTkButton(self.footer_bar, text="Back", fg_color="transparent", text_color=TEXT_SECONDARY, hover_color=CARD_HOVER, command=self._back_step)
        self.btn_back.pack(side="right")
        
        # Initial Render Pass
        self._render_current_step()

    def _render_current_step(self) -> None:
        """Clears the previous input slot and draws the current question layout states."""
        # 1. Update Navigation Button Visibilities
        self.btn_back.pack_forget() if self.current_step == 0 else self.btn_back.pack(side="right")
        self.btn_next.configure(text="Finish Setup" if self.current_step == len(self.steps) - 1 else "Next")
        
        # 2. Update Step Strings
        step_data = self.steps[self.current_step]
        self.progress_label.configure(text=f"Step {self.current_step + 1} of {len(self.steps)}")
        self.lbl_question.configure(text=step_data["question"])
        self.lbl_desc.configure(text=step_data["description"])
        
        # 3. Purge old input widget allocations
        if self.input_widget:
            self.input_widget.destroy()
            
        # 4. Generate the corresponding target widget mapping block
        widget_type = step_data["type"]
        prev_saved_value = self.user_responses.get(self.current_step, None)
        
        if widget_type == "radio":
            self.input_widget = ctk.CTkFrame(self.input_container, fg_color="transparent")
            self.input_widget.pack(fill="both", expand=True)
            self.radio_var = ctk.StringVar(value=prev_saved_value or step_data["options"][0])
            for option in step_data["options"]:
                rb = ctk.CTkRadioButton(self.input_widget, text=option, variable=self.radio_var, value=option, fg_color=RU, hover_color=PRIMARY_HOVER, text_color=TEXT)
                rb.pack(anchor="w", pady=6)
                
        elif widget_type == "dropdown":
            self.dropdown_var = ctk.StringVar(value=prev_saved_value or step_data["options"][0])
            self.input_widget = ctk.CTkOptionMenu(self.input_container, variable=self.dropdown_var, values=step_data["options"], fg_color=CARD_HOVER, button_color=RU_BLUE, button_hover_color=RU)
            self.input_widget.pack(anchor="w", pady=10)
            
        elif widget_type == "checkbox":
            self.check_var = ctk.BooleanVar(value=prev_saved_value if prev_saved_value is not None else False)
            self.input_widget = ctk.CTkCheckBox(self.input_container, text=step_data["label"], variable=self.check_var, fg_color=RU, hover_color=PRIMARY_HOVER, text_color=TEXT)
            self.input_widget.pack(anchor="w", pady=10)

    def _save_current_response(self) -> None:
        """Saves current interactive parameters into state dictionary indexes."""
        widget_type = self.steps[self.current_step]["type"]
        if widget_type == "radio":
            self.user_responses[self.current_step] = self.radio_var.get()
        elif widget_type == "dropdown":
            self.user_responses[self.current_step] = self.dropdown_var.get()
        elif widget_type == "checkbox":
            self.user_responses[self.current_step] = self.check_var.get()

    def _next_step(self) -> None:
        self._save_current_response()
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._render_current_step()
        else:
            # All items collected, execute routing out to database or logic engine
            self.on_complete(self.user_responses)

    def _back_step(self) -> None:
        if self.current_step > 0:
            self._save_current_response()
            self.current_step -= 1
            self._render_current_step()

```

---

### Step 3: Connect Buttons to Trigger the Wizard View

To open the wizard frame from your main home layout workspace, pass click routes into your primary buttons inside `gui/pages/home_page.py`.

Your master view controller (usually `window_manager.py`) should manage mounting and unmounting these frames. Here is how you bind the logic cleanly:

```python
        # Update your button instantiation inside gui/pages/home_page.py to call a load routine
        self.btn_left.configure(command=lambda: self.launch_setup_wizard("Analytics Engine Workspace", ANALYTICS_WIZARD_STEPS))

    def launch_setup_wizard(self, title: str, step_data: list[dict]) -> None:
        """Unmounts current view layout structures and instantiates a localized wizard chain."""
        # Hide home elements smoothly
        self.grid_forget()
        
        # Instantiate wizard on top of the parent context canvas
        self.active_wizard = WizardPage(
            master=self.master, # Mounts straight to Main App Window
            wizard_title=title,
            steps=step_data,
            on_complete_callback=self.handle_wizard_submission,
            on_cancel_callback=self.restore_home_dashboard
        )
        self.active_wizard.pack(fill="both", expand=True, padx=40, pady=40)

    def handle_wizard_submission(self, final_payload: dict[int, Any]) -> None:
        """Fires when user hits 'Finish Setup' on the final structural wizard step."""
        print(f"[ENGINE] Processing wizard responses data stack vector: {final_payload}")
        # Insert your Supabase pipeline hooks or system configurations calls here!
        self.restore_home_dashboard()

    def restore_home_dashboard(self) -> None:
        """Tears down wizard canvas tracks and restores primary home hub buttons view grid."""
        if hasattr(self, 'active_wizard'):
            self.active_wizard.pack_forget()
            self.active_wizard.destroy()
        
        # Remount the primary home grids layout maps
        self.grid(row=0, column=0, sticky="nsew")

```

### Why this design pattern rules:

1. **Dynamic Scaling:** You can support completely distinct questionnaires for all 4 buttons by creating separate list structures (e.g., `DATABASE_WIZARD_STEPS`, `FIREWALL_WIZARD_STEPS`). The script renders them perfectly using the exact same frame object.
2. **State Caching:** If a user runs through Step 1 and Step 2, hits **Back**, and then hits **Next** again, `self.user_responses` remembers what they selected, maintaining a highly responsive experience without dropping structural parameters on redrawing steps.