# 🛡️ Monolith Codebase Quality, Performance & Professionalism Audit Report

**Date:** June 17, 2026  
**Auditor:** Code Engineering Team  
**Scope:** Monolith Cross-Platform Engine (Python / CustomTkinter Core)

---

## ── 1. Executive Summary ──────────────────────────────────────────

This document presents a comprehensive, deep-dive security, architectural, quality, and performance audit of the Monolith codebase. The application utilizes **CustomTkinter** for its UI layout, **Pillow** for image rendering, **pycountry** for geographical standard resolution, and **Supabase** for backend services.

Our investigation revealed critical runtime bugs (fatal page-load crashes), severe security risks (exposed credentials), real-time UI performance bottlenecks (including I/O in the main event thread, inefficient fuzzy search algorithms, and memory leaks), and substantial dead code pollution across core UI modules.

### 📊 Overall Audit Dashboard

| Audit Dimension | Rating | Description / Primary Bottleneck |
| :--- | :---: | :--- |
| **Correctness & Stability** | 🔴 **Critical** | Fatal `AttributeError` in `folder_page.py` causing immediate application crashes on rendering. |
| **Security & Secrets Safety** | 🔴 **Critical** | Hardcoded production-level Supabase credentials in the test suite (`test_connection.py`). |
| **Real-Time UI Performance** | 🔴 **Critical** | Keystroke-level disk I/O & expensive fuzzy country string matches blocking the main Tkinter event loop. |
| **Code Hygiene (Linter)** | 🔴 **Critical** | 44 unresolved Ruff linter violations, including unused imports, variables, and duplicate function redefinitions. |
| **Memory Efficiency** | 🟡 **Needs Improvement** | Unbounded memory growth (memory leak) via an uncleared image cache in dropdown widgets. |
| **Professionalism & Clean Code**| 🟡 **Needs Improvement** | Thousands of lines of duplicate or alternative implementations commented out inside active files. |
| **Database & Thread Architecture**| 🟡 **Needs Improvement** | High SQLite connection handshake overhead; non-thread-safe UI updates in legacy database windows. |

---

## ── 2. Critical Bugs & Security Findings ─────────────────────────

### 2.1 Fatal Runtime Crash (AttributeError)
* **File**: `src/Monolith/gui/pages/folder_page.py`
* **Mechanic**:
  The initialization logic for `FolderPage` contains a severe regression where `self.country_combo` was duplicated and overwritten with the sector dropdown, while `self.sector_combo` was completely left undefined:
  ```python
  # Line 248: Overwrites self.country_combo with sector values
  self.country_combo = ctk.CTkOptionMenu(
      self.form_frame,
      values=self.sector_values,  
      ...
  )
  ...
  # Line 269: Attempts to call grid() on an undefined variable
  self.sector_combo.grid(
      row=1,
      column=1,
      sticky="ew",
      pady=(0, 10),
  )
  ```
* **Impact**: **Severe/Fatal**. The application will crash immediately with an `AttributeError: 'FolderPage' object has no attribute 'sector_combo'` as soon as the user navigates to the Folder creation wizard page.
* **Remediation**: Correct the variable assignment on line 248 to instantiate `self.sector_combo` instead of overwriting `self.country_combo`.

### 2.2 Security & Credentials Exposure
* **Vulnerability**: Hardcoded Production Supabase Credentials (`src/Monolith/test_connection.py`)
  * **Line 5**:
    ```python
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0cnJya25rbmhiemhzYWZnb2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3ODc3MTEsImV4cCI6MjA5NDM2MzcxMX0.teazRAnf9ExYggvZx3ZTFR43ZaOGDoCcLs0ze7UrXQA"
    ```
  * **Impact**: Exposing JWT bearer tokens in source control enables unauthorized actors to modify databases, access private data, or deplete Supabase service limits.
  * **Remediation**: Move the key to the environment variables configuration, and load via python-dotenv:
    ```python
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    ```

### 2.3 Syntax Bug / Inoperative Statement
* **Bug**: Broken Print Statement Expression (`src/Monolith/test_connection.py`)
  * **Lines 13–14**:
    ```python
    print
    (data)
    ```
  * **Impact**: Syntax-legal but inoperative. Evaluates `print` as a function object on line 13 and discards it, then evaluates `(data)` as a tuple on line 14 and discards it. No output is printed to stdout.
  * **Remediation**: Correct to a standard, single-line function call:
    ```python
    print(data)
    ```

### 2.4 Code Hygiene and Linter Violations
* **Analysis**: Running Ruff linter against the codebase reveals **44 errors/warnings**:
  * **Duplicate Redefinitions**: `get_asset_path` is imported twice on lines 3 and 6 of `src/Monolith/gui/widgets/image_provider.py`.
  * **Unused Imports & Variables**: Unused imports such as `PIL.Image` inside `misc.py`, `pathlib.Path` inside `env.py`, `logger.py`, and `ref_number_generator.py`. Local variables assigned but never read (e.g. `refresh_token` in `login_page.py` and `KeyError` variables in `ref_page.py`).
  * **Star Imports (`from module import *`)**: Used on line 19 of `wizard_page.py`, generating undefined/unresolvable names like `TEXT`, `TEXT_SECONDARY`, `CARD`, and `BORDER` according to static linter definitions.

---

## ── 3. Performance & Efficiency Analysis ─────────────────────────

### 3.1 Keystroke-Level Disk I/O Bottleneck
* **File**: `gui/widgets/search_combobox.py` and `gui/widgets/image_provider.py`
* **Mechanic**:
  Every keypress inside searchable dropdown frames triggers result rebuilding. If `self.image_provider` is bound, the widget makes up to 200 filesystem lookups and decodes PNG data on the fly inside the main event loop.
* **Performance Impact**:
  Causes intense UI stuttering and input lag when rendering dozens of flag icons on standard search actions.
* **Remediation**: Use the preloaded `REGISTRY` cache initialized at boot, preventing any filesystem disk reads during real-time UI filtering.

### 3.2 Computational Complexity of Fuzzy Country Search
* **File**: `core/utils/misc.py` (specifically `country_to_iso2` and `country_to_iso3`)
* **Mechanic**:
  On search combobox rebuilds, `pycountry.countries.search_fuzzy()` is called iteratively inside the main execution thread.
* **Performance Impact**:
  `search_fuzzy` performs extensive Levenshtein distance string matching across a massive database. Running this synchronously on every keystroke freezes CustomTkinter's single UI thread completely.
* **Remediation**: Match search terms directly against preloaded startup mappings or perform high-speed cached lookup sequences.

### 3.3 Memory Leak via Unbounded Image Cache
* **File**: `gui/widgets/search_combobox.py`
* **Mechanic**:
  To prevent Tkinter garbage collection of active images, references are tracked using `self.image_cache.append(image)`. However, the cache is never flushed or cleared.
* **Performance Impact**:
  Continuous typing inside search dropdowns leads to unbounded RAM utilization growth, producing a classic memory leak.
* **Remediation**: Add a `.clear()` instruction on `self.image_cache` at the beginning of `_build_results()` when existing widgets are destroyed:
  ```python
  for widget in self.results_frame.winfo_children():
      widget.destroy()
  self.image_cache.clear()
  ```

### 3.4 SQLite Connection Handshake Overhead
* **File**: `core/utils/ref_number_generator.py`
* **Mechanic**:
  `get_reference_values` connects to, queries, and disconnects from `references.db` on every single invocation.
* **Performance Impact**:
  Repeatedly executing disk and connection handshakes during page initialization delays page load transitions.
* **Remediation**: Memoize and cache reference datasets (such as countries, sectors, and file-types) after the first database read.

### 3.5 Thread Safety Violations
* **File**: `gui/pages/database_page.py` (Legacy Commented Block)
* **Mechanic**:
  The legacy database window spins up `threading.Thread` targeting `_database_network_query_worker`, which directly edits active GUI elements (`self._write_console_log(row)`).
* **Performance/Stability Impact**:
  Tkinter is single-threaded and not thread-safe. Modifying widget states from separate threads leads to intermittent race conditions and segmentation faults.
* **Remediation**: Implement thread-safe communications via a thread-safe Queue or scheduling callbacks on the main thread via `self.after()`.

---

## ── 4. Actionable Remediation Roadmap ──────────────────────────

### Phase 1: Correctness & Security Cleanup (Immediate)
1. **Fix `folder_page.py`**: Resolve the variable assignment crash on line 248 so `self.sector_combo` is correctly initialized.
2. **Revoke and Rotate Credentials**: Revoke the Supabase JWT key hardcoded in `test_connection.py` and move secret variables into `.env`.
3. **Resolve Ruff Linter Errors**: Run ruff fixes to strip unused imports and resolve duplicate definition warnings.
4. **Fix Malformed Syntax**: Repair the printed data expression in `test_connection.py`.

### Phase 2: Performance & Memory Leak Fixes (Short-Term)
1. **Fix Memory Leak**: Clear `self.image_cache` inside `search_combobox.py` during result rebuild sequences.
2. **Eliminate Disk I/O**: Ensure the searchable combobox references the preloaded `REGISTRY` instead of loading images from disk.
3. **Introduce Static Memoization**: Cache database reference datasets inside `ref_number_generator.py`.
