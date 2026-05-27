"""
Supabase client initialization.
"""

from supabase import create_client
from supabase.client import Client
from core.utils.logger import logger

from config.settings import SUPABASE_KEY
from config.settings import SUPABASE_URL

print(SUPABASE_KEY)
print(SUPABASE_URL)


class SupabaseConnection:
    """
    Singleton wrapper around Supabase client.
    """

    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Return a shared Supabase client instance.

        Returns:
            Client: Supabase client.
        """
        try:
            if cls._client is None:
                cls._client = create_client(
                    SUPABASE_URL,
                    SUPABASE_KEY,
                )
                logger.info("Supabase client initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")

        return cls._client
