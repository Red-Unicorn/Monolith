import pycountry
from core.utils.logger import logger


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
