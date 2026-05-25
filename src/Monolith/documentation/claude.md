Based on your Monolith project, here is the exact folder structure you should use:

```
monolith/
│
├── main.py                         ← Entry point. Run this.
├── requirements.txt                ← pip install -r requirements.txt
├── .env                            ← Your credentials (never commit this)
├── .env.example                    ← Template to share with teammates
├── .gitignore                      ← Must include .env
│
├── core/                           ← Pure logic. No GUI, no database.
│   ├── __init__.py
│   ├── constants.py                ← All lists: sectors, countries, file types…
│   ├── reference_generator.py      ← UID generation functions
│   └── duplicate_checker.py        ← Fuzzy similarity detection
│
├── database/                       ← All Supabase interaction lives here.
│   ├── __init__.py
│   └── supabase_client.py          ← DatabaseClient class + ReferenceRecord DTO
│
├── ui/                             ← Everything the user sees.
│   ├── __init__.py
│   ├── theme.py                    ← Colours, fonts, spacing, style dicts
│   ├── widgets.py                  ← Reusable custom widgets
│   ├── window_manager.py           ← Navigation controller (owns shared state)
│   └── screens/                   ← One file per screen/page.
│       ├── __init__.py
│       ├── splash.py               ← Login screen
│       ├── shell.py                ← App shell (sidebar + content pane)
│       ├── home.py                 ← Dashboard (the 3 tiles)
│       ├── project_form.py         ← Project & Resource wizard
│       ├── document_form.py        ← Document wizard
│       └── database_view.py        ← Database browser table
│
└── docs/                           ← Markdown documentation.
    ├── README.md                   ← Overview and quick start
    ├── USAGE.md                    ← Step-by-step user guide
    ├── INSTALL.md                  ← Supabase setup + packaging guide
    ├── FUNCTIONS.md                ← Full API / function reference
    └── LIBRARIES.md                ← Third-party library notes
```

---

### The rules behind this structure

**One responsibility per layer.** Each folder has a single job and a strict dependency direction — layers only import downward, never sideways or upward:

```
ui/screens  →  ui/widgets, ui/theme
ui/         →  core/, database/
core/       →  nothing (pure Python only)
database/   →  core/ (for ReferenceRecord), nothing else
```

**One screen per file.** Every screen in `ui/screens/` is self-contained. Adding a new screen never requires touching an existing one.

**`core/` is framework-free.** No `import customtkinter`, no `import supabase` anywhere in `core/`. This means you can unit-test every UID generation rule and duplicate check without launching a window or touching a database.

**`window_manager.py` is the only file that knows all screens.** No screen imports another screen directly — they all call `self._manager.show_xyz()`. This prevents circular imports and keeps navigation centralized.

---

### What goes where — quick reference

| You want to… | Edit this file |
|---|---|
| Change a colour or font | `ui/theme.py` |
| Add a new country or sector | `core/constants.py` |
| Change how UIDs are built | `core/reference_generator.py` |
| Add a new reusable widget | `ui/widgets.py` |
| Add a new screen | New file in `ui/screens/` + register in `window_manager.py` |
| Change the database schema | `database/supabase_client.py` |
| Change navigation flow | `ui/window_manager.py` |