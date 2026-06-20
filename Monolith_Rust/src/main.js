// Global error reporting layer to capture webview crashes or exceptions
window.addEventListener('error', (event) => {
  const errorMsg = `Global Error: ${event.message}\nAt: ${event.filename}:${event.lineno}:${event.colno}`;
  console.error(errorMsg);
  alert(errorMsg);
});
window.addEventListener('unhandledrejection', (event) => {
  const errorMsg = `Unhandled Promise Rejection: ${event.reason}`;
  console.error(errorMsg);
  alert(errorMsg);
});

const isTauri = typeof window !== 'undefined' && window.__TAURI__ !== undefined;

const invoke = isTauri ? window.__TAURI__.tauri.invoke : async (cmd, args) => {
  console.log(`[Mock Invoke] ${cmd}`, args);
  if (cmd === "get_supabase_config") {
    return {
      url: "https://ltrrrknknhbzhsafgoiu.supabase.co",
      key: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0cnJya25rbmhiemhzYWZnb2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3ODc3MTEsImV4cCI6MjA5NDM2MzcxMX0.teazRAnf9ExYggvZx3ZTFR43ZaOGDoCcLs0ze7UrXQA"
    };
  }
  if (cmd === "load_local_username" || cmd === "get_secure_token") {
    return null;
  }
  if (cmd === "get_reference_values") {
    if (args.tableName === "countries") {
      return { 
        "France": { code: "FR", description: "Western European nation" }, 
        "United States": { code: "US", description: "North American nation" }, 
        "Germany": { code: "DE", description: "Central European nation" },
        "UAE": { code: "AE", description: "Middle Eastern nation" }
      };
    }
    if (args.tableName === "sectors") {
      return { 
        "Banking": { code: "BNK", description: "Financial systems" }, 
        "Technology": { code: "TEC", description: "Tech infrastructure" } 
      };
    }
    if (args.tableName === "file_types") {
      return { 
        "PDF": { code: "PDF", description: "Portable Document" }, 
        "Word": { code: "DOC", description: "Word Document" } 
      };
    }
    if (args.tableName === "document_categories") {
      return { 
        "Agreement": { code: "AGR", description: "Legal agreements" }, 
        "Invoice": { code: "INV", description: "Billing invoicing" } 
      };
    }
    return {};
  }
  if (cmd === "to_pascal_snake_case") {
    return args.text.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('_');
  }
  if (cmd === "load_offline_records") {
    return localStorage.getItem("monolith_offline_records") || "[]";
  }
  if (cmd === "save_offline_records") {
    localStorage.setItem("monolith_offline_records", args.recordsJson);
    return null;
  }
  return null;
};

async function saveLocalOfflineRecords(records) {
  const jsonStr = JSON.stringify(records);
  if (isTauri) {
    try {
      await invoke("save_offline_records", { recordsJson: jsonStr });
    } catch (e) {
      console.error("Failed to save offline records via Tauri:", e);
    }
  } else {
    localStorage.setItem("monolith_offline_records", jsonStr);
  }
}

async function loadLocalOfflineRecords() {
  if (isTauri) {
    try {
      const jsonStr = await invoke("load_offline_records");
      return JSON.parse(jsonStr || "[]");
    } catch (e) {
      console.error("Failed to load offline records via Tauri:", e);
      return [];
    }
  } else {
    const jsonStr = localStorage.getItem("monolith_offline_records");
    return JSON.parse(jsonStr || "[]");
  }
}

const appWindow = isTauri ? window.__TAURI__.window.appWindow : {
  setSize: async (size) => console.log(`[Mock SetSize] ${size.width}x${size.height}`),
  close: async () => console.log("[Mock Close]"),
  outerPosition: async () => { console.log("[Mock GetPosition]"); return { x: 100, y: 100 }; },
  setPosition: async (pos) => console.log(`[Mock SetPosition] ${pos.x},${pos.y}`),
  scaleFactor: async () => { console.log("[Mock ScaleFactor]"); return 1; }
};

const LogicalSize = isTauri ? window.__TAURI__.window.LogicalSize : class {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }
};

const PhysicalPosition = isTauri ? window.__TAURI__.window.PhysicalPosition : class {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
};


// ──────────────────────────────────────────────────────────────────────────────
// STATE & CONFIG
// ──────────────────────────────────────────────────────────────────────────────
let supabaseClient = null;
let currentView = "login";
let dbRecords = [];
let currentUserEmail = "";
let cameFromView = "home";
let isWindowShifted = false;

// Form data payloads
let projectFormData = {
  country: "",
  country_code: "",
  sector: "",
  sector_code: "",
  name: "",
  type: "Project",
  type_code: "PRO",
  description: ""
};

let docFormData = {
  project_name: "",
  project_ref: "",
  doccat: "",
  doccat_code: "",
  name: "",
  description: ""
};

// Caches for references database
let referencesCache = {
  countries: {},
  sectors: {},
  file_types: {},
  document_categories: {}
};

// ──────────────────────────────────────────────────────────────────────────────
// INITIALIZATION
// ──────────────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
  // Set current year
  document.querySelector(".current-year").textContent = new Date().getFullYear();
  
  // Set initial window size
  await appWindow.setSize(new LogicalSize(370, 570));

  // Initialize Supabase client
  try {
    const config = await invoke("get_supabase_config");
    supabaseClient = supabase.createClient(config.url, config.key);
  } catch (error) {
    console.error("Failed to initialize Supabase:", error);
  }

  // Pre-load reference lists from SQLite db
  await loadReferenceData();

  // Pre-load database records cache deferred to post-login

  // Setup UI elements & event listeners
  setupEventListeners();
  
  // Load saved credentials hint if any
  await checkSavedUserHint();
});

// ──────────────────────────────────────────────────────────────────────────────
// LOAD SQLITE REFERENCES
// ──────────────────────────────────────────────────────────────────────────────
async function loadReferenceData() {
  const tables = ["countries", "sectors", "file_types", "document_categories"];
  for (const table of tables) {
    try {
      referencesCache[table] = await invoke("get_reference_values", { tableName: table });
    } catch (e) {
      console.error(`Error loading sqlite table ${table}:`, e);
    }
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// CREDENTIALS VAULT AUTO-FILL
// ──────────────────────────────────────────────────────────────────────────────
async function checkSavedUserHint() {
  try {
    const savedUser = await invoke("load_local_username");
    if (savedUser) {
      currentUserEmail = savedUser;
      document.getElementById("email-input").value = savedUser;
      document.getElementById("remember-me").checked = true;

      const savedPass = await invoke("get_secure_token", { email: savedUser });
      if (savedPass) {
        document.getElementById("password-input").value = savedPass;
      }
    }
  } catch (e) {
    console.error("Vault check failed:", e);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// NAVIGATION & LAYOUT SWITCH
// ──────────────────────────────────────────────────────────────────────────────
async function switchView(viewName) {
  if (viewName !== "database" && isWindowShifted) {
    if (isTauri) {
      try {
        const factor = await appWindow.scaleFactor();
        const pos = await appWindow.outerPosition();
        const newX = pos.x + Math.round(50 * factor);
        await appWindow.setPosition(new PhysicalPosition(newX, pos.y));
      } catch (e) {
        console.error("Failed to restore window position:", e);
      }
    }
    isWindowShifted = false;
  }

  try {
    currentView = viewName;
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    document.querySelectorAll(".subview").forEach(sv => sv.classList.remove("active"));

    if (viewName === "login") {
      document.getElementById("login-view").classList.add("active");
      await appWindow.setSize(new LogicalSize(370, 570));
      document.getElementById("app-view").classList.remove("extended");
    } else {
      document.getElementById("app-view").classList.add("active");
      
      if (viewName === "database") {
        document.getElementById("app-stepper").style.display = "none";
        document.getElementById("app-view-title").style.display = "block";
        document.getElementById("database-subview").classList.add("active");
        document.getElementById("app-view").classList.add("extended");
        if (isTauri && !isWindowShifted) {
          try {
            const factor = await appWindow.scaleFactor();
            const pos = await appWindow.outerPosition();
            const newX = pos.x - Math.round(50 * factor);
            await appWindow.setPosition(new PhysicalPosition(newX, pos.y));
            isWindowShifted = true;
          } catch (e) {
            console.error("Failed to shift window position left:", e);
          }
        }
        await appWindow.setSize(new LogicalSize(800, 720)); // Expanded width to 800px
        loadDatabaseGrid();
      } else {
        document.getElementById("app-stepper").style.display = "flex";
        document.getElementById("app-view-title").style.display = "none";
        document.getElementById("app-view").classList.remove("extended");
        await appWindow.setSize(new LogicalSize(650, 500));
        
        if (viewName === "home") {
          document.getElementById("home-subview").classList.add("active");
          updateStepper(1);
        } else if (viewName === "project") {
          document.getElementById("project-subview").classList.add("active");
          updateStepper(2);
          initCombobox("country-combobox", Object.keys(referencesCache.countries).sort(), "countries");
          initCombobox("sector-combobox", Object.keys(referencesCache.sectors).sort(), "sectors");
          initCombobox("type-combobox", ["Project", "Resource"]);
          document.getElementById("project-char-counter").textContent = `${document.getElementById("project-desc-input").value.length} / 200`;
        } else if (viewName === "document") {
          document.getElementById("doc-subview").classList.add("active");
          updateStepper(2);
          initCombobox("project-select-combobox", getProjectResourceNames(), "projects");
          initCombobox("doccat-combobox", Object.keys(referencesCache.document_categories).sort(), "document_categories");
          document.getElementById("doc-char-counter").textContent = `${document.getElementById("doc-desc-input").value.length} / 200`;
        } else if (viewName === "ref") {
          document.getElementById("ref-subview").classList.add("active");
          updateStepper(3);

          // Populate selection summary dynamically
          const summaryContent = document.getElementById("ref-summary-content");
          if (summaryContent) {
            const refNum = document.getElementById("generated-ref-val").textContent;
            if (cameFromView === "project") {
              summaryContent.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Country of Origin:</span> <span style="font-weight: 500; color: var(--text-main);">${projectFormData.country}</span></div>
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Sector:</span> <span style="font-weight: 500; color: var(--text-main);">${projectFormData.sector}</span></div>
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Project/Resource Name:</span> <span style="font-weight: 500; color: var(--text-main);">${projectFormData.name}</span></div>
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Type:</span> <span style="font-weight: 500; color: var(--text-main);">${projectFormData.type}</span></div>
                  <div style="margin-top: 6px; padding-top: 10px; border-top: 1px dashed var(--border-color);"><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Reference Number:</span> <span style="font-weight: 600; color: var(--accent-green); font-family: var(--font-mono);">${refNum}</span></div>
                </div>
              `;
            } else if (cameFromView === "document") {
              summaryContent.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Project/Resource:</span> <span style="font-weight: 500; color: var(--text-main);">${docFormData.project_name}</span></div>
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Document Category:</span> <span style="font-weight: 500; color: var(--text-main);">${docFormData.doccat}</span></div>
                  <div><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Document Name:</span> <span style="font-weight: 500; color: var(--text-main);">${docFormData.name}</span></div>
                  <div style="margin-top: 6px; padding-top: 10px; border-top: 1px dashed var(--border-color);"><span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px;">Reference Number:</span> <span style="font-weight: 600; color: var(--accent-green); font-family: var(--font-mono);">${refNum}</span></div>
                </div>
              `;
            }
          }
        }
      }
    }
  } catch (error) {
    console.error("Error in switchView:", error);
    alert(`switchView Error: ${error.message}\nStack: ${error.stack}`);
  }
}

function updateStepper(stepNumber) {
  document.querySelectorAll(".step").forEach(s => {
    const sNum = parseInt(s.getAttribute("data-step"));
    if (sNum < stepNumber) {
      s.classList.add("active");
      s.classList.remove("current");
    } else if (sNum === stepNumber) {
      s.classList.add("active");
      s.classList.add("current");
    } else {
      s.classList.remove("active");
      s.classList.remove("current");
    }
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// EVENT LISTENERS SETUP
// ──────────────────────────────────────────────────────────────────────────────
function setupEventListeners() {
  // Login Page Actions
  document.getElementById("sign-in-btn").addEventListener("click", handleLogin);
  document.getElementById("password-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleLogin();
  });
  document.getElementById("toggle-password-btn").addEventListener("click", togglePasswordVisibility);

  const offlineBypassBtn = document.getElementById("offline-bypass-btn");
  if (offlineBypassBtn) {
    offlineBypassBtn.addEventListener("click", async () => {
      const email = document.getElementById("email-input").value.trim() || "offline@example.com";
      const password = document.getElementById("password-input").value || "offline";
      const rememberChecked = document.getElementById("remember-me").checked;

      currentUserEmail = email;
      supabaseClient = null;

      if (rememberChecked) {
        await invoke("save_local_username", { email });
        await invoke("save_secure_token", { email, token: password });
      } else {
        await invoke("clear_local_username");
        await invoke("clear_secure_token", { email });
      }

      await loadDatabaseRecordsCache();
      await switchView("home");
    });
  }

  // Stepper Click Actions
  document.querySelectorAll(".step").forEach(stepEl => {
    stepEl.addEventListener("click", () => {
      const stepNum = parseInt(stepEl.getAttribute("data-step"));
      if (stepNum === 1) {
        resetForms();
        switchView("home");
      } else if (stepNum === 2) {
        if (currentView === "ref") {
          switchView(cameFromView);
        } else if (currentView === "home") {
          switchView("project");
        }
      } else if (stepNum === 3) {
        const refVal = document.getElementById("generated-ref-val").textContent;
        if (refVal && refVal !== "FR-BNK-PRJ-A1B2" && refVal !== "") {
          switchView("ref");
        }
      }
    });
  });

  // Dashboard Page Actions
  document.getElementById("nav-project-btn").addEventListener("click", () => switchView("project"));
  document.getElementById("nav-doc-btn").addEventListener("click", () => switchView("document"));
  document.getElementById("nav-db-btn").addEventListener("click", () => switchView("database"));
  document.getElementById("exit-btn").addEventListener("click", () => appWindow.close());

  // Wizard General Previous Button
  document.querySelectorAll(".back-to-home-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      // Clear forms values
      resetForms();
      switchView("home");
    });
  });

  // Project Page Next Button
  document.getElementById("project-next-btn").addEventListener("click", handleProjectNext);
  setupCharCounter("project-desc-input", "project-char-counter");

  // Document Page Next Button
  document.getElementById("doc-next-btn").addEventListener("click", handleDocNext);
  setupCharCounter("doc-desc-input", "doc-char-counter");

  // Reference generated result buttons
  document.getElementById("ref-back-btn").addEventListener("click", async () => {
    await switchView(cameFromView);
  });
  document.getElementById("ref-create-another-btn").addEventListener("click", async () => {
    resetForms();
    await switchView("home");
  });
  document.getElementById("ref-exit-btn").addEventListener("click", () => {
    appWindow.close();
  });

  // Clipboard copies
  const copyRefBtn = document.getElementById("copy-ref-btn");
  if (copyRefBtn) copyRefBtn.addEventListener("click", (e) => handleCopy(e.currentTarget));

  const copyFileBtn = document.getElementById("copy-file-btn");
  if (copyFileBtn) copyFileBtn.addEventListener("click", (e) => handleCopy(e.currentTarget));

  const copyCombinedBtn = document.getElementById("copy-combined-btn");
  if (copyCombinedBtn) copyCombinedBtn.addEventListener("click", (e) => handleCopy(e.currentTarget));

  // Database Filter Events
  document.getElementById("db-search").addEventListener("input", filterDatabaseGrid);
  document.getElementById("db-type-filter").addEventListener("change", filterDatabaseGrid);
  document.getElementById("db-country-filter").addEventListener("change", filterDatabaseGrid);

  // Database Exports
  document.getElementById("export-csv-btn").addEventListener("click", exportCSV);
  document.getElementById("export-xlsx-btn").addEventListener("click", exportExcel);

  // Close dropdowns on click outside globally
  document.addEventListener("click", (e) => {
    document.querySelectorAll(".search-combobox").forEach(combobox => {
      const dropdown = combobox.querySelector(".combo-dropdown");
      if (dropdown && !combobox.contains(e.target)) {
        dropdown.classList.remove("open");
      }
    });
  });
}

// Toggle password text entry visibility
function togglePasswordVisibility() {
  const input = document.getElementById("password-input");
  const img = document.getElementById("eye-icon");
  if (input.type === "password") {
    input.type = "text";
    img.src = "assets/icons/eye-open-w.png";
  } else {
    input.type = "password";
    img.src = "assets/icons/eye-closed-w.png";
  }
}

// Show success snackbar for 3 seconds
function showSuccessSnackbar() {
  const snack = document.getElementById("snackbar");
  if (!snack) return;
  snack.classList.add("show");
  setTimeout(() => {
    snack.classList.remove("show");
  }, 3000);
}

// character counter trigger
function setupCharCounter(inputId, counterId) {
  const input = document.getElementById(inputId);
  const counter = document.getElementById(counterId);
  input.addEventListener("input", () => {
    const len = input.value.length;
    counter.textContent = `${len} / 200`;
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SECURE LOGIN AUTHENTICATION
// ──────────────────────────────────────────────────────────────────────────────
async function handleLogin() {
  const email = document.getElementById("email-input").value.trim();
  const password = document.getElementById("password-input").value;
  const rememberChecked = document.getElementById("remember-me").checked;
  const errorLabel = document.getElementById("login-error");
  const offlineBypassContainer = document.getElementById("offline-bypass-container");

  errorLabel.textContent = "";
  if (offlineBypassContainer) offlineBypassContainer.style.display = "none";

  if (!email || !password) {
    errorLabel.textContent = "Please fill in all credentials.";
    return;
  }

  if (!supabaseClient || !supabaseClient.auth) {
    // If Supabase not loaded/configured, login with mock bypass
    console.log("Supabase not loaded, performing mock login bypass.");
    currentUserEmail = email;
    if (rememberChecked) {
      await invoke("save_local_username", { email });
      await invoke("save_secure_token", { email, token: password });
    } else {
      await invoke("clear_local_username");
      await invoke("clear_secure_token", { email });
    }
    await loadDatabaseRecordsCache();
    await switchView("home");
    return;
  }

  try {
    const { data, error } = await supabaseClient.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      errorLabel.textContent = error.message;
      if (offlineBypassContainer) offlineBypassContainer.style.display = "block";
      return;
    }

    if (data && data.user) {
      currentUserEmail = data.user.email;
      // Remember me vault mappings
      if (rememberChecked) {
        await invoke("save_local_username", { email });
        await invoke("save_secure_token", { email, token: password });
      } else {
        await invoke("clear_local_username");
        await invoke("clear_secure_token", { email });
      }

      await loadDatabaseRecordsCache();
      await switchView("home");
    }
  } catch (err) {
    console.error("Login connection failed:", err);
    errorLabel.textContent = "Supabase connection failed.";
    if (offlineBypassContainer) offlineBypassContainer.style.display = "block";
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// CUSTOM COMBOBOX IMPLEMENTATION
// ──────────────────────────────────────────────────────────────────────────────
function initCombobox(id, values, type) {
  const combobox = document.getElementById(id);
  if (!combobox) return;
  const input = combobox.querySelector(".combo-input");
  const dropdown = combobox.querySelector(".combo-dropdown");
  const searchInput = combobox.querySelector(".combo-search");
  const resultsContainer = combobox.querySelector(".combo-results");

  // Prevent stale closures in event listeners by storing values on the element
  combobox._values = values;
  combobox._type = type;

  // Clear previous active selections on re-init unless there is a saved value
  let initialValue = "";
  if (id === "country-combobox") {
    initialValue = projectFormData.country;
  } else if (id === "sector-combobox") {
    initialValue = projectFormData.sector;
  } else if (id === "type-combobox") {
    initialValue = projectFormData.type;
  } else if (id === "project-select-combobox") {
    initialValue = docFormData.project_name;
  } else if (id === "doccat-combobox") {
    initialValue = docFormData.doccat;
  }
  input.value = initialValue || "";
  if (searchInput) searchInput.value = "";

  // Reset border colors from error highlights
  input.style.borderColor = "";

  const toggleDropdown = (e) => {
    e.stopPropagation();
    // Close other dropdowns first
    document.querySelectorAll(".combo-dropdown").forEach(d => {
      if (d !== dropdown) d.classList.remove("open");
    });
    dropdown.classList.toggle("open");
    if (dropdown.classList.contains("open") && searchInput) {
      searchInput.focus();
    }
  };

  if (!input._hasListener) {
    input.addEventListener("click", toggleDropdown);
    input._hasListener = true;
  }
  
  const arrow = combobox.querySelector(".combo-arrow");
  if (arrow && !arrow._hasListener) {
    arrow.addEventListener("click", toggleDropdown);
    arrow._hasListener = true;
  }

  const filterItems = () => {
    const currentValues = combobox._values || [];
    const currentType = combobox._type;
    const term = searchInput ? searchInput.value.toLowerCase() : "";
    resultsContainer.innerHTML = "";

    const filtered = currentValues.filter(v => v.toLowerCase().includes(term));
    filtered.forEach(value => {
      const item = document.createElement("div");
      item.className = "combo-item";
      item.setAttribute("data-value", value);

      // Pre-load icon images if countries
      let iconPath = "";
      if (currentType === "countries" && referencesCache.countries[value]) {
        iconPath = `assets/flags/png/${referencesCache.countries[value].code.toLowerCase()}.png`;
      }

      if (iconPath) {
        const img = document.createElement("img");
        img.src = iconPath;
        img.onerror = () => img.style.display = "none";
        item.appendChild(img);
      }

      const text = document.createElement("span");
      text.textContent = value;
      item.appendChild(text);

      item.addEventListener("click", () => {
        input.value = value;
        dropdown.classList.remove("open");
        
        // Save selected payload
        if (id === "country-combobox") {
          projectFormData.country = value;
          projectFormData.country_code = referencesCache.countries[value].code;
        } else if (id === "sector-combobox") {
          projectFormData.sector = value;
          projectFormData.sector_code = referencesCache.sectors[value].code;
        } else if (id === "type-combobox") {
          projectFormData.type = value;
          projectFormData.type_code = value === "Project" ? "PRO" : "RES";
        } else if (id === "project-select-combobox") {
          docFormData.project_name = value;
          const match = dbRecords.find(r => r.name_title === value && (r.type === "Project" || r.type === "Resource"));
          docFormData.project_ref = match ? match.ref_number : "";
        } else if (id === "doccat-combobox") {
          docFormData.doccat = value;
          docFormData.doccat_code = referencesCache.document_categories[value].code;
        }
      });
      resultsContainer.appendChild(item);
    });
  };

  if (searchInput) {
    if (!searchInput._hasListener) {
      searchInput.addEventListener("input", filterItems);
      searchInput._hasListener = true;
    }
  } else {
    // For fixed dropdown lists like project type
    combobox.querySelectorAll(".combo-item").forEach(item => {
      if (!item._hasListener) {
        item.addEventListener("click", () => {
          const val = item.getAttribute("data-value");
          input.value = val;
          dropdown.classList.remove("open");
          projectFormData.type = val;
          projectFormData.type_code = val === "Project" ? "PRO" : "RES";
        });
        item._hasListener = true;
      }
    });
  }

  // Re-build initial results
  if (searchInput) filterItems();
}

// ──────────────────────────────────────────────────────────────────────────────
// WIZARDS VALIDATION & SUBMIT
// ──────────────────────────────────────────────────────────────────────────────
async function handleProjectNext() {
  const country = projectFormData.country;
  const sector = projectFormData.sector;
  const type = projectFormData.type;
  const name = document.getElementById("project-name-input").value.trim();
  const desc = document.getElementById("project-desc-input").value;

  let valid = true;

  // Reset highlight styling
  document.querySelector("#country-combobox .combo-input").style.borderColor = "";
  document.querySelector("#sector-combobox .combo-input").style.borderColor = "";
  document.querySelector("#type-combobox .combo-input").style.borderColor = "";
  document.getElementById("project-name-input").style.borderColor = "";

  if (!country) {
    document.querySelector("#country-combobox .combo-input").style.borderColor = "#ef4444";
    valid = false;
  }
  if (!sector) {
    document.querySelector("#sector-combobox .combo-input").style.borderColor = "#ef4444";
    valid = false;
  }
  if (!type) {
    document.querySelector("#type-combobox .combo-input").style.borderColor = "#ef4444";
    valid = false;
  }
  if (!name) {
    document.getElementById("project-name-input").style.borderColor = "#ef4444";
    valid = false;
  }

  if (!valid) return;

  projectFormData.name = name;
  projectFormData.description = desc;

  // Generate reference and filename tokens
  const hex = generateRandomHex();
  const refNum = `${projectFormData.country_code.toUpperCase()}-${projectFormData.sector_code.toUpperCase()}-${projectFormData.type_code}-${hex}`;
  const cleanName = await invoke("to_pascal_snake_case", { text: name });

  // Update DOM Output View
  document.getElementById("generated-ref-val").textContent = refNum;
  document.getElementById("generated-file-val").textContent = cleanName;
  document.getElementById("generated-combined-val").textContent = `${refNum}_${cleanName}`;

  // Sync to database
  await pushRecordToDatabase(refNum, projectFormData.type, name, country, projectFormData.description);

  cameFromView = "project";
  await switchView("ref");
  showSuccessSnackbar();
}

async function handleDocNext() {
  const projectSelect = docFormData.project_name;
  const category = docFormData.doccat;
  const name = document.getElementById("doc-name-input").value.trim();
  const desc = document.getElementById("doc-desc-input").value;

  let valid = true;

  document.querySelector("#project-select-combobox .combo-input").style.borderColor = "";
  document.querySelector("#doccat-combobox .combo-input").style.borderColor = "";
  document.getElementById("doc-name-input").style.borderColor = "";

  if (!projectSelect) {
    document.querySelector("#project-select-combobox .combo-input").style.borderColor = "#ef4444";
    valid = false;
  }
  if (!category) {
    document.querySelector("#doccat-combobox .combo-input").style.borderColor = "#ef4444";
    valid = false;
  }
  if (!name) {
    document.getElementById("doc-name-input").style.borderColor = "#ef4444";
    valid = false;
  }

  if (!valid) return;

  docFormData.name = name;
  docFormData.description = desc;

  // Generate document ref: {project_ref}-{doccat_code}-{hex}
  const hex = generateRandomHex();
  const prefix = docFormData.project_ref || "PROJ-REF";
  const refNum = `${prefix}-${docFormData.doccat_code.toUpperCase()}-${hex}`;
  const cleanName = await invoke("to_pascal_snake_case", { text: name });

  document.getElementById("generated-ref-val").textContent = refNum;
  document.getElementById("generated-file-val").textContent = cleanName;
  document.getElementById("generated-combined-val").textContent = `${refNum}_${cleanName}`;

  // Sync to database
  const match = dbRecords.find(r => r.name_title === projectSelect && (r.type === "Project" || r.type === "Resource"));
  const country = match ? match.country : "France";

  await pushRecordToDatabase(refNum, "Document", name, country, docFormData.description);

  cameFromView = "document";
  await switchView("ref");
  showSuccessSnackbar();
}

function generateRandomHex() {
  return Math.random().toString(16).substr(2, 4).toUpperCase();
}

function getTodayDateString() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
}

// Clean fields upon workflow exit/teardowns
function resetForms() {
  projectFormData = { country: "", country_code: "", sector: "", sector_code: "", name: "", type: "Project", type_code: "PRO", description: "" };
  docFormData = { project_name: "", project_ref: "", doccat: "", doccat_code: "", name: "", description: "" };
  
  document.getElementById("project-name-input").value = "";
  document.getElementById("project-desc-input").value = "";
  document.getElementById("project-char-counter").textContent = "0 / 200";

  document.getElementById("doc-name-input").value = "";
  document.getElementById("doc-desc-input").value = "";
  document.getElementById("doc-char-counter").textContent = "0 / 200";
}

// ──────────────────────────────────────────────────────────────────────────────
// CLIPBOARD COPY ACTIONS
// ──────────────────────────────────────────────────────────────────────────────
function handleCopy(button) {
  const targetId = button.getAttribute("data-clipboard-id");
  const value = document.getElementById(targetId).textContent;
  
  // Write to clipboard via web API
  navigator.clipboard.writeText(value);

  // Success Feedback Animation
  const originalHTML = button.innerHTML;
  button.innerHTML = "Copied!";
  button.style.backgroundColor = "#123c36";
  button.style.color = "#34d399";
  button.style.width = "65px";

  setTimeout(() => {
    button.innerHTML = originalHTML;
    button.style.backgroundColor = "";
    button.style.color = "";
    button.style.width = "";
  }, 1500);
}

// ──────────────────────────────────────────────────────────────────────────────
// DATABASE VIEWER GRID
// ──────────────────────────────────────────────────────────────────────────────
async function loadDatabaseRecordsCache() {
  if (!supabaseClient) {
    dbRecords = await loadLocalOfflineRecords();
    return;
  }

  try {
    const { data, error } = await supabaseClient
      .from("records")
      .select("ref_number, type, name_title, country, added_by, date_added, description")
      .order("date_added", { ascending: false });

    if (error) throw error;
    dbRecords = data || [];
    await saveLocalOfflineRecords(dbRecords);
  } catch (e) {
    console.error("Failed to load database records cache, falling back to local storage:", e);
    dbRecords = await loadLocalOfflineRecords();
  }
}

async function loadDatabaseGrid() {
  const container = document.getElementById("db-grid-content");
  container.innerHTML = "<div style='text-align:center; padding:30px; color:var(--text-muted);'>Loading records...</div>";

  await loadDatabaseRecordsCache();
  renderDatabaseGrid(dbRecords);
}

let mockInitialized = false;

function loadMockDatabaseGrid() {
  if (!mockInitialized) {
    dbRecords = [];
    mockInitialized = true;
  }
}

function getProjectResourceNames() {
  const names = dbRecords
    .filter(r => r.type === "Project" || r.type === "Resource")
    .map(r => r.name_title);
  return [...new Set(names)].sort();
}

function renderDatabaseGrid(records) {
  const container = document.getElementById("db-grid-content");
  const countLabel = document.getElementById("db-record-count");
  container.innerHTML = "";

  countLabel.textContent = `Total: ${records.length} records`;

  if (records.length === 0) {
    container.innerHTML = "<div style='text-align:center; padding:30px; color:var(--text-muted);'>No records match filters.</div>";
    return;
  }

  records.forEach(row => {
    const rowEl = document.createElement("div");
    rowEl.className = "db-row";

    // Format date string
    let dateStr = row.date_added || "";
    if (dateStr.includes("T")) {
      dateStr = dateStr.replace("T", " ").substring(0, 16);
    }

    rowEl.innerHTML = `
      <div class="col-ref">${row.ref_number || ""}</div>
      <div class="col-type">${row.type || ""}</div>
      <div class="col-title">${row.name_title || ""}</div>
      <div class="col-desc" title="${row.description || ""}">${row.description || ""}</div>
      <div class="col-country">${row.country || ""}</div>
      <div class="col-addedby">${row.added_by || ""}</div>
      <div class="col-date">${dateStr}</div>
    `;
    container.appendChild(rowEl);
  });
}

function filterDatabaseGrid() {
  const search = document.getElementById("db-search").value.toLowerCase();
  const type = document.getElementById("db-type-filter").value;
  const country = document.getElementById("db-country-filter").value;

  const filtered = dbRecords.filter(row => {
    const matchesSearch = 
      (row.ref_number && row.ref_number.toLowerCase().includes(search)) ||
      (row.name_title && row.name_title.toLowerCase().includes(search)) ||
      (row.description && row.description.toLowerCase().includes(search)) ||
      (row.added_by && row.added_by.toLowerCase().includes(search));
    
    const matchesType = type === "All Types" || row.type === type;
    const matchesCountry = country === "All Countries" || row.country === country;

    return matchesSearch && matchesType && matchesCountry;
  });

  renderDatabaseGrid(filtered);
}

// ──────────────────────────────────────────────────────────────────────────────
// SYNC REQUISITES BACK TO SUPABASE
// ──────────────────────────────────────────────────────────────────────────────
async function pushRecordToDatabase(refNum, type, name, country, description) {
  const email = currentUserEmail || "Unknown User";
  const newRecord = {
    ref_number: refNum,
    type: type,
    name_title: name,
    description: description || "",
    country: country,
    added_by: email,
    date_added: new Date().toISOString()
  };

  // Add dynamically to local grid
  dbRecords.unshift(newRecord);

  // Save local persistent backup
  await saveLocalOfflineRecords(dbRecords);

  if (!supabaseClient) {
    console.log("Offline mode: saved record locally.");
    return;
  }

  try {
    const { error } = await supabaseClient.from("records").insert({
      ref_number: refNum,
      type: type,
      name_title: name,
      description: description || "",
      country: country,
      added_by: email,
      date_added: newRecord.date_added
    });

    if (error) {
      console.error("Failed to insert record to Supabase:", error.message);
    } else {
      console.log("Successfully sent record to Supabase!");
    }
  } catch (e) {
    console.error("Database insert query aborted:", e);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// EXPORTS UTILITIES (CSV & EXCEL)
// ──────────────────────────────────────────────────────────────────────────────
function triggerBrowserDownload(content, filename, contentType) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

async function exportCSV() {
  if (dbRecords.length === 0) return;

  let csvContent = "Ref. Number,Type,Name / Title,Description,Country,Added By,Date Added\n";

  dbRecords.forEach(r => {
    const row = [
      r.ref_number || "",
      r.type || "",
      `"${(r.name_title || "").replace(/"/g, '""')}"`,
      `"${(r.description || "").replace(/"/g, '""')}"`,
      r.country || "",
      r.added_by || "",
      r.date_added || ""
    ];
    csvContent += row.join(",") + "\n";
  });

  if (isTauri) {
    try {
      const { save } = window.__TAURI__.dialog;
      const { writeTextFile } = window.__TAURI__.fs;
      const filePath = await save({
        defaultPath: 'monolith_database_export.csv',
        filters: [{ name: 'CSV', extensions: ['csv'] }]
      });
      if (filePath) {
        await writeTextFile(filePath, csvContent);
      }
    } catch (e) {
      console.error("Tauri CSV export failed, falling back to browser download:", e);
      triggerBrowserDownload(csvContent, "monolith_database_export.csv", "text/csv");
    }
  } else {
    triggerBrowserDownload(csvContent, "monolith_database_export.csv", "text/csv");
  }
}

async function exportExcel() {
  if (dbRecords.length === 0) return;

  let excelContent = "Ref. Number\tType\tName / Title\tDescription\tCountry\tAdded By\tDate Added\n";

  dbRecords.forEach(r => {
    const row = [
      r.ref_number || "",
      r.type || "",
      r.name_title || "",
      r.description || "",
      r.country || "",
      r.added_by || "",
      r.date_added || ""
    ];
    excelContent += row.join("\t") + "\n";
  });

  if (isTauri) {
    try {
      const { save } = window.__TAURI__.dialog;
      const { writeTextFile } = window.__TAURI__.fs;
      const filePath = await save({
        defaultPath: 'monolith_database_export.xls',
        filters: [{ name: 'Excel', extensions: ['xls'] }]
      });
      if (filePath) {
        await writeTextFile(filePath, excelContent);
      }
    } catch (e) {
      console.error("Tauri Excel export failed, falling back to browser download:", e);
      triggerBrowserDownload(excelContent, "monolith_database_export.xls", "application/vnd.ms-excel");
    }
  } else {
    triggerBrowserDownload(excelContent, "monolith_database_export.xls", "application/vnd.ms-excel");
  }
}
