from __future__ import annotations
import customtkinter as ctk
from core.utils.paths import get_asset_path
from core.utils.ref_number_generator import get_reference_values
from core.utils.logger import logger
from core.utils.paths import get_asset_path
from gui.widgets.search_combobox import SearchComboBox
from config.settings import REGISTRY


def load_image(
    relative_path: str,
    size=(20, 14),
):

    path = get_asset_path(relative_path)

    return SearchComboBox.load_image(
        path,
        size=size,
    )


def filetype_image_provider(filetype):

    return load_image(
        f"icons/files/{filetype.lower()}.png",
        size=(16, 16),
    )


def initialize_registry() -> None:

    for db_reg in REGISTRY.keys():
        db_info = get_reference_values(db_reg)

        for name, info in db_info.items():
            flag_image = None
            try:
                path = get_asset_path(f'flags/png/{info.get("code")}.png')
                flag_image = load_image(path, size=(20, 14))
            except Exception as e:
                logger.debug(f"Impossible of loading flag: {path} - {e}")
                flag_image = None

            # 4. Save into single structured registry record
            REGISTRY[db_reg][name] = {
                "code": info.get("code"),
                "image": flag_image,
                "description": info.get("description"),
            }
