from pathlib import Path

import cairosvg

from core.utils.paths import get_asset_path

# ─────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────

SVG_DIR = get_asset_path("flags/svg")
PNG_DIR = get_asset_path("flags/png")

PNG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ─────────────────────────────────────────────────────────────
# CONVERT SVG → PNG
# ─────────────────────────────────────────────────────────────

for svg_file in SVG_DIR.glob("*.svg"):

    png_file = PNG_DIR / f"{svg_file.stem}.png"

    print(f"Converting {svg_file.name} → {png_file.name}")

    cairosvg.svg2png(
        url=str(svg_file),
        write_to=str(png_file),
        output_width=32,
        output_height=24,
    )

print("Conversion complete.")
