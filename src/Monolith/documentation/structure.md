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