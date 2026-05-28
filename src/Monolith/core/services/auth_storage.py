from __future__ import annotations

import json
import keyring

from pathlib import Path

from core.utils.logger import logger

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

SERVICE_NAME = "Monolith"

USER_HINT_FILE = Path.home() / ".monolith_user_hint.json"


# ─────────────────────────────────────────────────────────────
# SECURE TOKEN STORAGE
# ─────────────────────────────────────────────────────────────


def save_secure_token(email: str, refresh_token: str):
    """
    Save refresh token securely in OS keychain.
    """

    try:
        keyring.set_password(
            SERVICE_NAME,
            email,
            refresh_token,
        )

    except Exception as error:

        logger.error(f"Failed to save secure token: {error}")


def get_secure_token(email: str) -> str | None:
    """
    Retrieve secure token from OS keychain.
    """

    try:
        return keyring.get_password(
            SERVICE_NAME,
            email,
        )

    except Exception as error:

        logger.error(f"Failed to load secure token: {error}")

        return None


def clear_secure_token(email: str):
    """
    Remove token from OS vault.
    """

    try:
        keyring.delete_password(
            SERVICE_NAME,
            email,
        )

    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# LOCAL EMAIL STORAGE
# ─────────────────────────────────────────────────────────────


def save_local_username(email: str):
    """
    Save non-sensitive email locally.
    """

    try:

        with open(USER_HINT_FILE, "w") as file:

            json.dump(
                {"last_authenticated_user": email},
                file,
            )

    except Exception as error:

        logger.error(f"Failed to save local username: {error}")


def load_local_username() -> str | None:
    """
    Load saved email.
    """

    try:

        if not USER_HINT_FILE.exists():
            return None

        with open(USER_HINT_FILE, "r") as file:

            data = json.load(file)

        return data.get("last_authenticated_user")

    except Exception as error:

        logger.error(f"Failed to load local username: {error}")

        return None


def clear_local_username():
    """
    Remove saved email.
    """

    try:

        if USER_HINT_FILE.exists():
            USER_HINT_FILE.unlink()

    except Exception as error:

        logger.error(f"Failed to clear local username: {error}")


### For AUTO-FILING RATHER THAN AUTO-LOGIN
def save_password(email: str, password: str):

    keyring.set_password(
        SERVICE_NAME,
        email,
        password,
    )


def load_password(email: str) -> str | None:

    return keyring.get_password(
        SERVICE_NAME,
        email,
    )
