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

fn hex_encode(text: &str) -> String {
    text.as_bytes().iter().map(|b| format!("{:02x}", b)).collect()
}

fn hex_decode(hex: &str) -> Result<String, String> {
    if hex.len() % 2 != 0 {
        return Err("Invalid hex string length".to_string());
    }
    let mut bytes = Vec::new();
    for i in (0..hex.len()).step_by(2) {
        let b = u8::from_str_radix(&hex[i..i+2], 16)
            .map_err(|_| "Failed to parse hex digit".to_string())?;
        bytes.push(b);
    }
    String::from_utf8(bytes).map_err(|e| e.to_string())
}

fn get_vault_file_path() -> Result<PathBuf, String> {
    let home = std::env::var("HOME")
        .or_else(|_| std::env::var("USERPROFILE"))
        .map_err(|_| "Could not find home directory".to_string())?;
    Ok(PathBuf::from(home).join(".monolith_vault.json"))
}

fn write_fallback_token(email: &str, token: &str) -> Result<(), String> {
    let path = get_vault_file_path()?;
    let mut map = if path.exists() {
        let content = fs::read_to_string(&path).map_err(|e| e.to_string())?;
        serde_json::from_str::<HashMap<String, String>>(&content).unwrap_or_default()
    } else {
        HashMap::new()
    };
    let encoded = hex_encode(token);
    map.insert(email.to_string(), encoded);
    let json = serde_json::to_string(&map).map_err(|e| e.to_string())?;
    fs::write(path, json).map_err(|e| e.to_string())?;
    Ok(())
}

fn read_fallback_token(email: &str) -> Result<Option<String>, String> {
    let path = get_vault_file_path()?;
    if !path.exists() {
        return Ok(None);
    }
    let content = fs::read_to_string(&path).map_err(|e| e.to_string())?;
    let map: HashMap<String, String> = serde_json::from_str(&content).unwrap_or_default();
    if let Some(encoded) = map.get(email) {
        let decoded = hex_decode(encoded)?;
        Ok(Some(decoded))
    } else {
        Ok(None)
    }
}

fn delete_fallback_token(email: &str) -> Result<(), String> {
    let path = get_vault_file_path()?;
    if !path.exists() {
        return Ok(());
    }
    let content = fs::read_to_string(&path).map_err(|e| e.to_string())?;
    let mut map: HashMap<String, String> = serde_json::from_str(&content).unwrap_or_default();
    if map.remove(email).is_some() {
        let json = serde_json::to_string(&map).map_err(|e| e.to_string())?;
        fs::write(path, json).map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
fn save_secure_token(email: &str, token: &str) -> Result<(), String> {
    match Entry::new(SERVICE_NAME, email) {
        Ok(entry) => {
            if let Err(e) = entry.set_password(token) {
                eprintln!("Keyring save failed ({}), falling back to local file.", e);
                write_fallback_token(email, token)?;
            }
        }
        Err(e) => {
            eprintln!("Keyring entry creation failed ({}), falling back to local file.", e);
            write_fallback_token(email, token)?;
        }
    }
    Ok(())
}

#[tauri::command]
fn get_secure_token(email: &str) -> Result<Option<String>, String> {
    match Entry::new(SERVICE_NAME, email) {
        Ok(entry) => {
            match entry.get_password() {
                Ok(password) => Ok(Some(password)),
                Err(keyring::Error::NoEntry) => {
                    read_fallback_token(email)
                }
                Err(e) => {
                    eprintln!("Keyring get failed ({}), trying local file fallback.", e);
                    read_fallback_token(email)
                }
            }
        }
        Err(e) => {
            eprintln!("Keyring entry creation failed ({}), trying local file fallback.", e);
            read_fallback_token(email)
        }
    }
}

#[tauri::command]
fn clear_secure_token(email: &str) -> Result<(), String> {
    if let Ok(entry) = Entry::new(SERVICE_NAME, email) {
        let _ = entry.delete_password();
    }
    delete_fallback_token(email)?;
    Ok(())
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
fn to_pascal_snake_case(text: &str) -> String {
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
        url = std::env::var("SUPABASE_URL").unwrap_or_default();
    }
    if key.is_empty() {
        key = std::env::var("SUPABASE_KEY").unwrap_or_default();
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
            to_pascal_snake_case,
            get_supabase_config
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
