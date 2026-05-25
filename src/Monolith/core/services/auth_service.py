"""
Authentication service for Monolith.
"""

from supabase import Client

from core.database.supabase_client import SupabaseConnection


class AuthService:
    """
    Handles user authentication and session management.
    """

    def __init__(self) -> None:
        self.client: Client = SupabaseConnection.get_client()

    def login(
        self,
        email: str,
        password: str,
    ) -> dict:
        """
        Authenticate user.

        Args:
            email: User email.
            password: User password.

        Returns:
            dict: Authentication response.
        """

        response = self.client.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        return response

    def logout(self) -> None:
        """
        Logout current user.
        """

        self.client.auth.sign_out()

    def get_current_user(self):
        """
        Return authenticated user.
        """

        return self.client.auth.get_user()
