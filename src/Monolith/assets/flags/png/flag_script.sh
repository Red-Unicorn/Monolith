#!/bin/bash

#FLAG_DIR="src/Monolith/assets/flags/png"

FLAG_DIR="."
python3 << EOF
from pathlib import Path
import pycountry

flag_dir = Path("$FLAG_DIR")

converted = 0
skipped = 0

for png in flag_dir.glob("*.png"):
    iso2 = png.stem.upper()

    country = pycountry.countries.get(alpha_2=iso2)

    if country:
        new_name = png.with_name(f"{country.alpha_3}.png")

        if png != new_name:
            png.rename(new_name)
            print(f"{png.name:15} -> {new_name.name}")
            converted += 1
    else:
        print(f"SKIPPED: {png.name}")
        skipped += 1

print()
print(f"Converted: {converted}")
print(f"Skipped:   {skipped}")
EOF
