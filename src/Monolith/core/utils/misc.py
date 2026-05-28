import pycountry
from core.utils.logger import logger
from PIL import Image


def iso3_to_iso2(code: str) -> str:

    country = pycountry.countries.get(alpha_3=code)

    if not country:
        return ""

    return country.alpha_2.lower()


def country_to_iso2(name: str) -> str:

    try:

        country = pycountry.countries.search_fuzzy(name)[0]

        return country.alpha_2.lower()

    except LookupError as e:

        logger.debug("Unable to load contry name: {e}")
        return ""


def country_to_iso3(name: str) -> str:

    try:

        country = pycountry.countries.search_fuzzy(name)[0]

        return country.alpha_3.lower()

    except LookupError as e:

        logger.debug("Unable to load contry name: {e}")
        return ""


def tint_icon(path, color=(255, 255, 255)):

    img = Image.open(path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for r, g, b, a in data:
        if a > 0:
            new_data.append((*color, a))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)
    return img
