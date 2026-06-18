#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use keyring::Entry;
use rusqlite::Connection;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use regex::Regex;

#[derive(Serialize, Deserialize, Debug, Clone)]
struct ReferenceValue {
    code: String,
    description: Option<String>,
}

#[derive(Serialize, Deserialize, Debug)]
struct UserHint {
    last_authenticated_user: String,
}

// ──────────────────────────────────────────────────────────────────────────────
// SQLITE REFERENCE VALUE COMMAND
// ──────────────────────────────────────────────────────────────────────────────

#[tauri::command]
fn get_reference_values(
    handle: tauri::AppHandle,
    table_name: &str,
) -> Result<HashMap<String, ReferenceValue>, String> {
    let allowed_tables = [
        "countries",
        "document_categories",
        "sectors",
        "source_types",
        "file_types",
    ];
    if !allowed_tables.contains(&table_name) {
        return Err(format!(
            "Table '{}' is not an allowed reference table.",
            table_name
        ));
    }

    let db_path = handle
        .path_resolver()
        .resolve_resource("resources/references.db")
        .ok_or_else(|| "Failed to resolve references.db path".to_string())?;

    let conn = Connection::open(&db_path).map_err(|e| e.to_string())?;

    // Check if description column exists
    let mut stmt = conn
        .prepare(&format!("PRAGMA table_info({})", table_name))
        .map_err(|e| e.to_string())?;
    let mut rows = stmt.query([]).map_err(|e| e.to_string())?;
    let mut has_description = false;
    while let Some(row) = rows.next().map_err(|e| e.to_string())? {
        let name: String = row.get(1).map_err(|e| e.to_string())?;
        if name == "description" {
            has_description = true;
            break;
        }
    }

    let query = if has_description {
        format!("SELECT code, label, description FROM {} ORDER BY label", table_name)
    } else {
        format!("SELECT code, label, NULL FROM {} ORDER BY label", table_name)
    };

    let mut stmt = conn.prepare(&query).map_err(|e| e.to_string())?;
    let mut rows = stmt.query([]).map_err(|e| e.to_string())?;

    let mut items = HashMap::new();
    while let Some(row) = rows.next().map_err(|e| e.to_string())? {
        let code: String = row.get(0).map_err(|e| e.to_string())?;
        let label: String = row.get(1).map_err(|e| e.to_string())?;
        let description: Option<String> = row.get(2).map_err(|e| e.to_string())?;

        items.insert(
            label,
            ReferenceValue {
                code,
                description,
            },
        );
    }

    Ok(items)
}

// ──────────────────────────────────────────────────────────────────────────────
// SECURE STORAGE COMMANDS (KEYRING OS VAULT)
// ──────────────────────────────────────────────────────────────────────────────

const SERVICE_NAME: &str = "Monolith";

#[tauri::command]
fn save_secure_token(email: &str, token: &str) -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, email).map_err(|e| e.to_string())?;
    entry.set_password(token).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn get_secure_token(email: &str) -> Result<Option<String>, String> {
    let entry = Entry::new(SERVICE_NAME, email).map_err(|e| e.to_string())?;
    match entry.get_password() {
        Ok(password) => Ok(Some(password)),
        Err(keyring::Error::NoEntry) => Ok(None),
        Err(e) => Err(e.to_string()),
    }
}

#[tauri::command]
fn clear_secure_token(email: &str) -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, email).map_err(|e| e.to_string())?;
    match entry.delete_password() {
        Ok(_) => Ok(()),
        Err(keyring::Error::NoEntry) => Ok(()),
        Err(e) => Err(e.to_string()),
    }
}

// ──────────────────────────────────────────────────────────────────────────────
// LOCAL EMAIL HINT STORAGE COMMANDS
// ──────────────────────────────────────────────────────────────────────────────

fn get_hint_file_path() -> Result<PathBuf, String> {
    let home = std::env::var("HOME")
        .or_else(|_| std::env::var("USERPROFILE"))
        .map_err(|_| "Could not find home directory".to_string())?;
    Ok(PathBuf::from(home).join(".monolith_user_hint.json"))
}

#[tauri::command]
fn save_local_username(email: &str) -> Result<(), String> {
    let path = get_hint_file_path()?;
    let data = UserHint {
        last_authenticated_user: email.to_string(),
    };
    let json = serde_json::to_string(&data).map_err(|e| e.to_string())?;
    fs::write(path, json).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn load_local_username() -> Result<Option<String>, String> {
    let path = get_hint_file_path()?;
    if !path.exists() {
        return Ok(None);
    }
    let json = fs::read_to_string(path).map_err(|e| e.to_string())?;
    let data: UserHint = serde_json::from_str(&json).map_err(|e| e.to_string())?;
    Ok(Some(data.last_authenticated_user))
}

#[tauri::command]
fn clear_local_username() -> Result<(), String> {
    let path = get_hint_file_path()?;
    if path.exists() {
        fs::remove_file(path).map_err(|e| e.to_string())?;
    }
    Ok(())
}

// ──────────────────────────────────────────────────────────────────────────────
// STRING UTILITIES
// ──────────────────────────────────────────────────────────────────────────────

#[tauri::command]
fn to_snake_case(text: &str) -> String {
    if text.is_empty() {
        return String::new();
    }

    // 1. camelCase / PascalCase
    let re1 = Regex::new(r"([a-z0-9])([A-Z])").unwrap();
    let s1 = re1.replace_all(text, "${1}_${2}");

    // 2. Consecutive capitals
    let re2 = Regex::new(r"([A-Z]+)([A-Z][a-z])").unwrap();
    let s2 = re2.replace_all(&s1, "${1}_${2}");

    // 3. Non-alphanumeric split
    let re3 = Regex::new(r"[^a-zA-Z0-9]+").unwrap();
    let s3 = re3.replace_all(&s2, "_");

    let cleaned = s3.trim_matches('_');
    let words: Vec<&str> = cleaned.split('_').filter(|w| !w.is_empty()).collect();

    let capitalized: Vec<String> = words
        .iter()
        .map(|w| {
            let mut chars = w.chars();
            match chars.next() {
                None => String::new(),
                Some(first) => {
                    first.to_uppercase().collect::<String>()
                        + &chars.as_str().to_lowercase()
                }
            }
        })
        .collect();

    capitalized.join("_")
}

#[derive(Serialize)]
struct SupabaseConfig {
    url: String,
    key: String,
}

#[tauri::command]
fn get_supabase_config() -> SupabaseConfig {
    let mut path = std::env::current_dir().unwrap_or_default();
    let mut env_path = None;

    for _ in 0..5 {
        let check_path = path.join("src/Monolith/.env");
        if check_path.exists() {
            env_path = Some(check_path);
            break;
        }
        let check_path2 = path.join(".env");
        if check_path2.exists() {
            env_path = Some(check_path2);
            break;
        }
        if let Some(parent) = path.parent() {
            path = parent.to_path_buf();
        } else {
            break;
        }
    }

    let mut url = String::new();
    let mut key = String::new();

    if let Some(p) = env_path {
        if let Ok(content) = fs::read_to_string(p) {
            for line in content.lines() {
                if line.starts_with("SUPABASE_URL=") {
                    url = line.replace("SUPABASE_URL=", "").trim().to_string();
                } else if line.starts_with("SUPABASE_KEY_OLD=") {
                    key = line.replace("SUPABASE_KEY_OLD=", "").trim().to_string();
                }
            }
        }
    }

    // Fallbacks
    if url.is_empty() {
        url = "https://ltrrrknknhbzhsafgoiu.supabase.co".to_string();
    }
    if key.is_empty() {
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0cnJya25rbmhiemhzYWZnb2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3ODc3MTEsImV4cCI6MjA5NDM2MzcxMX0.teazRAnf9ExYggvZx3ZTFR43ZaOGDoCcLs0ze7UrXQA".to_string();
    }

    SupabaseConfig { url, key }
}

// ──────────────────────────────────────────────────────────────────────────────
// MAIN APPLICATION SETUP
// ──────────────────────────────────────────────────────────────────────────────

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_reference_values,
            save_secure_token,
            get_secure_token,
            clear_secure_token,
            save_local_username,
            load_local_username,
            clear_local_username,
            to_snake_case,
            get_supabase_config
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
