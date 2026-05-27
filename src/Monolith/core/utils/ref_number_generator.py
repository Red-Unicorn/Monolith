"""Generator for creating unique reference numbers."""

## Tasks
# 1.fetch database for part of reference
# 2.Unify the references
# 3.Generate 4 digit hexadecimal
# 4.Combine all parts into a single reference number string
# 5.Ensure uniqueness by checking against existing references in the database
# 6.Implement error handling for potential collisions or database issues
## Function:
# 1.Get countries from database
# 2.Get product categories from database
# 3.Get current date from database
# 4.Get sectors from database
# 5.Generate random 4 digit hexadecimal

import sqlite3
from pathlib import Path
from core.utils.logger import logger
from core.utils.paths import find_project_root

DB_PATH = find_project_root("main.py") / "core" / "database" / "references.db"


def get_reference_values(table_name: str) -> dict[str, list[str]]:

    ALLOWED_TABLES = {
        "countries",
        "document_categories",
        "sectors",
        "source_types",
        "file_types",
    }

    if table_name not in ALLOWED_TABLES:
        logger.error("Invalid table name requested: %s", table_name)
        raise ValueError(f"Table '{table_name}' is not an allowed reference table.")

    # Connect to the SQLite database and fetch code, label, and optional description
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get available columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = {row[1] for row in cursor.fetchall()}

        has_description = "description" in columns

        description_column = "description" if has_description else "NULL AS description"

        query = f"""
            SELECT code, label, {description_column}
            FROM {table_name}
            ORDER BY label
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        items = {}

        for row in rows:
            items[row["label"]] = {
                "code": row["code"],
                "description": (row["description"] if has_description else None),
            }

        return items


################################
################################
# Data structure
# data = {
#     "codes": ["A1", "B2"],
#     "labels": ["Apple", "Banana"],
#     "descriptions": ["Red fruit", ""],
# }

# items = {}
# # Build a label → full info map
# for code, label, desc in zip(data["codes"], data["labels"], data["descriptions"]):
#     items[label] = {"code": code, "description": desc}

# # Create ComboBox
# import customtkinter as ctk

# combobox = ctk.CTkComboBox(master=app, values=list(items.keys()))
# combobox.pack()


# # Get code from selection
# def on_select(choice):
#     code = items[choice]["code"]
#     print("Selected code:", code)


# combobox.configure(command=on_select)


# # Attach tooltip to ComboBox selection
# def get_description():
#     choice = combobox.get()
#     return items.get(choice, {}).get("description", "")


# from gui.widgets.tooltips import ToolTip

# ToolTip(combobox, get_description)

# def get_ref():

#     # Step 1: Fetch data from the database
#     countries = fetch_countries_from_db()
#     product_categories = fetch_product_categories_from_db()
#     current_date = fetch_current_date_from_db()
#     sectors = fetch_sectors_from_db()

#     # Step 2: Unify the references (e.g., take first three letters of each)
#     country_code = unify_reference(countries)
#     category_code = unify_reference(product_categories)
#     date_code = unify_reference(current_date)
#     sector_code = unify_reference(sectors)

#     # Step 3: Generate a random 4-digit hexadecimal
#     random_hex = generate_random_hex(4)

#     # Step 4: Combine all parts into a single reference number string
#     reference_number = f"{country_code}-{category_code}-{date_code}-{sector_code}-{random_hex}"

#     # Step 5: Ensure uniqueness by checking against existing references in the database
#     while check_reference_exists_in_db(reference_number):
#         random_hex = generate_random_hex(4)
#         reference_number = f"{country_code}-{category_code}-{date_code}-{sector_code}-{random_hex}"

#     return reference_number
