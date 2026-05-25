For a professional-scale CustomTkinter application like Monolith, you should structure the project like a real desktop software product, not as a single-script GUI.

A clean architecture gives you:

* maintainability
* scalability
* easier debugging
* separation of concerns
* reusable widgets
* cleaner database integration
* packaging readiness

# Recommended Enterprise Structure

```text
Monolith/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── assets/
│   ├── icons/
│   │   ├── logo.png
│   │   ├── app.ico
│   │   ├── dashboard.png
│   │   ├── project.png
│   │   └── ...
│   │
│   ├── images/
│   │   ├── splash.png
│   │   └── backgrounds/
│   │
│   └── fonts/
│
├── config/
│   ├── settings.py
│   ├── mappings.py
│   ├── constants.py
│   └── database.py
│
├── core/
│   ├── database/
│   │   ├── supabase_client.py
│   │   ├── repositories/
│   │   │   ├── reference_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── project_repository.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── reference_service.py
│   │   ├── export_service.py
│   │   ├── duplicate_service.py
│   │   └── logging_service.py
│   │
│   ├── generators/
│   │   ├── project_generator.py
│   │   ├── document_generator.py
│   │   └── filename_generator.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── resource.py
│   │   └── document.py
│   │
│   └── utils/
│       ├── validators.py
│       ├── formatters.py
│       ├── clipboard.py
│       ├── threading_utils.py
│       └── date_utils.py
│
├── gui/
│   ├── app_window.py
│   ├── login_page.py
│   ├── splash_screen.py
│   │
│   ├── pages/
│   │   ├── dashboard_page.py
│   │   ├── database_page.py
│   │   ├── project_page.py
│   │   ├── resource_page.py
│   │   ├── document_page.py
│   │   ├── settings_page.py
│   │   └── users_page.py
│   │
│   ├── widgets/
│   │   ├── sidebar.py
│   │   ├── topbar.py
│   │   ├── searchable_dropdown.py
│   │   ├── statistics_card.py
│   │   ├── database_table.py
│   │   ├── wizard_header.py
│   │   ├── hover_button.py
│   │   └── confirmation_dialog.py
│   │
│   └── theme/
│       ├── colors.py
│       ├── fonts.py
│       ├── layout.py
│       └── styles.py
│
├── documentation/
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── DATABASE.md
│   ├── API.md
│   └── ARCHITECTURE.md
│
├── exports/
│   ├── csv/
│   ├── excel/
│   └── pdf/
│
├── logs/
│   └── monolith.log
│
└── tests/
    ├── test_generators.py
    ├── test_database.py
    ├── test_auth.py
    └── test_utils.py
```

# What Each Folder Does

## `assets/`

Contains:

* icons
* splash screens
* images
* fonts

Never hardcode images into code.

---

# `config/`

Contains configuration only.

Example:

```python
SUPABASE_URL
WINDOW_SIZES
COLORS
SECTOR_CODES
DOCUMENT_TYPES
```

No logic should be here.

---

# `core/`

This is the BUSINESS LOGIC layer.

The GUI should NEVER directly talk to Supabase.

Instead:

```text
GUI
→ Services
→ Repository
→ Database
```

This is extremely important for clean architecture.

---

# `models/`

Represents data objects.

Example:

```python
class Project:
```

Used to structure application data cleanly.

---

# `services/`

Contains application logic.

Example:

```python
generate_reference()
check_duplicates()
authenticate_user()
export_csv()
```

This is where MOST logic belongs.

---

# `repositories/`

Handles database communication ONLY.

Example:

```python
insert_project()
fetch_documents()
search_reference()
```

This separates SQL/database from business logic.

---

# `gui/`

Contains ONLY interface code.

Never put:

* SQL
* Supabase logic
* heavy business logic

inside GUI files.

---

# `widgets/`

Reusable UI components.

Example:

* sidebar
* database table
* searchable dropdown
* statistic cards

This is how professional GUI apps are built.

---

# `theme/`

Centralized design system.

Example:

```python
PRIMARY = "#E63946"
BACKGROUND = "#0F172A"
```

Changing the entire app theme becomes easy.

---

# `tests/`

Unit tests.

Critical for larger apps.

---

# Recommended App Flow

```text
app.py
    ↓
app_window.py
    ↓
login_page.py
    ↓
dashboard_page.py
    ↓
service layer
    ↓
repository layer
    ↓
supabase
```

# Example Proper Flow

## BAD

```python
# GUI directly calling database
client.table("projects").insert(...)
```

---

## GOOD

```python
# GUI
project_service.create_project(...)
```

↓

```python
# service
repository.insert_project(...)
```

↓

```python
# repository
supabase.table(...)
```

# Recommended Naming Convention

## Files

```text
snake_case.py
```

## Classes

```python
ProjectPage
ReferenceGenerator
```

## Constants

```python
PRIMARY_COLOR
MAX_DESCRIPTION_LENGTH
```

## Functions

```python
generate_reference()
copy_to_clipboard()
```

# Best Practices

## 1. One class per file

Avoid giant files.

---

## 2. Keep GUI clean

GUI should mostly:

* display data
* collect input
* call services

---

## 3. Centralize styles

Never repeat:

```python
fg_color="#E63946"
```

everywhere.

---

## 4. Use reusable widgets

Huge time saver.

---

## 5. Use type hints everywhere

```python
def generate_reference(name: str) -> str:
```

---

## 6. Document everything

Use docstrings:

```python
"""
Generate a unique project reference.
"""
```

---

# Recommended Scale

For Monolith specifically:

| Layer    | Approx Files |
| -------- | ------------ |
| GUI      | 20–30        |
| Widgets  | 10–15        |
| Services | 10           |
| Database | 5            |
| Models   | 5            |
| Utils    | 10           |

A real enterprise desktop app becomes large quickly.

---

# Packaging Later

This structure also prepares you for:

* PyInstaller
* auto-updaters
* installers
* CI/CD
* multi-user support
* plugins
* modular architecture

without rewriting the app later.
