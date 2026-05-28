from core.utils.paths import get_asset_path
from gui.widgets.search_combobox import SearchComboBox


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
