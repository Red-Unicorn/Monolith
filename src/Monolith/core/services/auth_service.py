"""
Authentication service for Monolith.
"""

from supabase import Client

from core.database.supabase_client import SupabaseConnection
from core.utils.logger import logger


class AuthService:

    def __init__(self) -> None:
        self.client: Client = SupabaseConnection.get_client()

    def login(
        self,
        email: str,
        password: str,
    ) -> dict:

        response = self.client.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        return response

    def logout(self) -> None:

        self.client.auth.sign_out()

    def get_current_user(self):

        return self.client.auth.get_user()

    def validate_token(
        self,
        refresh_token: str,
    ) -> bool:
        """
        Validate stored refresh token.
        """

        try:

            response = self.client.auth.refresh_session(refresh_token=refresh_token)

            return response.session is not None

        except Exception as error:

            logger.error(f"Token validation failed: {error}")

            return False
