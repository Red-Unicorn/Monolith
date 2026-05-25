"""
================================================================================
PROJECT:       Monolith Application Engine
MODULE:        gui.constants.wizard_data
DESCRIPTION:   Centralized immutable storage array for multi-tier wizard question
               payload structures. Maps explicit platform schema fields to driving
               runtime evaluation objects.
AUTHOR:        Red Unicorn (Intl') Holding Group – Core Engineering Team
LICENSE:       Proprietary – All rights reserved
VERSION:       1.2.0
CHANGELOG:     - 1.0.0: Initial base map setup
               - 1.1.0: Migrated layout tracking to flat design matrix strings
               - 1.2.0: Enhanced system diagnostic node arrays
================================================================================
"""

from __future__ import annotations
from typing import Any, Dict, List

# ── MASTER MONOLITH ROUTING SCHEMA ────────────────────────────────────────────
# Step 1 is the core hub card picker. Choosing an item instantly forks the
# rest of the wizard to load relevant questionnaire sub-tracks.

MONOLITH_MASTER_STEPS: List[Dict[str, Any]] = [
    {
        "question": "SELECT OPERATIONAL VECTOR HUB",
        "description": "Initialize workspace pipelines by choosing an operational core module channel.",
        "type": "cards",  # 💡 NEW: Triggers the main 3-card grid interface
        "options": ["Analytics Engine", "Database Clusters", "Network Firewall"],
    }
]

# ── SUBSIDIARY DATA BLOCK TRACKS ──────────────────────────────────────────────
# These get appended dynamically depending on which card the user clicks in Step 1.

ANALYTICS_SUB_STEPS = [
    {
        "question": "What is your primary analytical data target?",
        "description": "Select the core metric stream you wish to isolate for Monolith tracking data.",
        "type": "radio",
        "options": [
            "Realtime Network Latency",
            "Database Operational Load",
            "User Auth Event Logs",
        ],
    },
    {
        "question": "Assign regional cluster access boundaries",
        "description": "Select all target operations environments this security vector may intercept.",
        "type": "multiselect",
        "options": [
            "North America East",
            "European Core (Frankfurt)",
            "Asia Pacific South",
        ],
    },
]

DATABASE_SUB_STEPS = [
    {
        "question": "Identify target database shard node target",
        "description": "Establishes local socket connection maps to encrypted database endpoints.",
        "type": "radio",
        "options": ["Primary Core Cluster (EU)", "Failover Secondary Redundancy (US)"],
    }
]

FIREWALL_SUB_STEPS = [
    {
        "question": "Configure incoming packet inspection security rules",
        "description": "Locks down localized application shell listening vector boundaries.",
        "type": "dropdown",
        "options": [
            "Strict Mode (Block All Unsigned Vectors)",
            "Permissive Developer Routing Profile",
        ],
    }
]
