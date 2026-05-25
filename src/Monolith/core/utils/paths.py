import sys
from pathlib import Path

# def get_asset_path(relative_path: str) -> Path:
#     """
#     Get the absolute path to an asset, handling both local development
#     and packaged production environments (PyInstaller / brief-case bundles).
#     """
#     # PyInstaller creates a temporary folder and stores its path in _MEIPASS
#     if hasattr(sys, "_MEIPASS"):
#         return Path(sys._MEIPASS) / "assets" / relative_path

#     # Local developer fallback path mapping
#     project_root = Path(__file__).resolve().parents[3]
#     return project_root / "assets" / relative_path


# import sys
# from pathlib import Path


def find_project_root(marker: str = "main.py") -> Path:
    """
    Scans upward from the current file's directory structure to locate
    the project root folder containing the designated anchor marker file.
    """
    current_path = Path(__file__).resolve().parent

    # Loop upward through parent folders all the way to the drive root
    for parent in [current_path] + list(current_path.parents):
        if (parent / marker).exists():
            return parent

    # Fail-safe backup if marker isn't found: fall back to current directory frame
    return current_path


def get_asset_path(relative_path: str) -> Path:
    """
    Resolves asset locations universally across local Python environments
    and packaged distribution wrappers (PyInstaller / brief-case bundle sandboxes).
    """
    # 1. Production Bundle Check (Handles running inside compiled Mac .app or Windows .exe)
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "assets" / relative_path

    # 2. Local System Resolution via Anchor Marker (Dynamic search)
    project_root = find_project_root("main.py")
    return project_root / "assets" / relative_path
