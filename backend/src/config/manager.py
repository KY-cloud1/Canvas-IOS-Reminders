"""
Utilities for loading, accessing, and persisting application settings.
"""

from config.database import Database
from config.secrets import SecretStore
from config.settings import Settings


class SettingsManager:
    """
    Manage the application's configuration lifecycle.

    This class provides a centralized interface for loading settings
    from persistent storage, retrieving the current configuration,
    updating stored values, and reloading the in-memory settings.
    """

    _settings: Settings | None = None

    @classmethod
    def load(cls) -> None:
        """
        Initialize the database and load application settings.

        Ensures the database is initialized, then retrieves
        configuration values from the database and secret store,
        converts them to their appropriate types, and caches them
        in memory.
        """
        Database.initialize()

        cls._settings = Settings(
            canvas_enabled=Database.get("canvas_enabled") == "true",
            canvas_graphql_url=Database.get("canvas_graphql_url") or "",
            canvas_token=SecretStore.get("canvas_token"),
            gradescope_enabled=Database.get("gradescope_enabled") == "true",
            gradescope_email=SecretStore.get("gradescope_email"),
            gradescope_password=SecretStore.get("gradescope_password"),
            refresh_interval=int(Database.get("refresh_interval")),
            weeks_delta=int(Database.get("weeks_delta")),
            ngrok_enabled=Database.get("ngrok_enabled") == "true",
            ngrok_domain=Database.get("ngrok_domain") or "",
            ngrok_authtoken=SecretStore.get("ngrok_authtoken"),
        )

    @classmethod
    def get(cls) -> Settings:
        """
        Return the application settings, loading them if necessary.

        If the settings have not yet been loaded, they are loaded
        automatically before being returned.

        Returns:
            The application Settings instance.
        """
        if cls._settings is None:
            cls.load()

        assert cls._settings is not None
        return cls._settings

    @classmethod
    def save(cls, settings: Settings) -> None:
        """
        Initialize the database, persist application settings, and
        update the in-memory cache.

        Args:
            settings: The settings instance to save.
        """
        Database.initialize()

        Database.set("canvas_enabled", str(settings.canvas_enabled).lower())
        Database.set("canvas_graphql_url", settings.canvas_graphql_url)
        Database.set("gradescope_enabled", str(settings.gradescope_enabled).lower())
        Database.set("refresh_interval", str(settings.refresh_interval))
        Database.set("weeks_delta", str(settings.weeks_delta))
        Database.set("ngrok_enabled", str(settings.ngrok_enabled).lower())
        Database.set("ngrok_domain", settings.ngrok_domain)

        cls._save_secret("canvas_token", settings.canvas_token)
        cls._save_secret("gradescope_email", settings.gradescope_email)
        cls._save_secret("gradescope_password", settings.gradescope_password)
        cls._save_secret("ngrok_authtoken", settings.ngrok_authtoken)

        cls._settings = settings

    @classmethod
    def reload(cls) -> None:
        """
        Reload application settings from persistent storage.

        Any cached settings are replaced with the latest persisted
        values.
        """
        cls.load()

    @staticmethod
    def _save_secret(name: str, value: str | None) -> None:
        """
        Persist or remove a secret from the secret store.

        If the provided value is ``None``, the secret is deleted.
        Otherwise, the secret is stored or updated with the given
        value.

        Args:
            name: The name of the secret.
            value: The secret value to store, or ``None`` to delete
                the secret.
        """
        if value is None:
            SecretStore.delete(name)
        else:
            SecretStore.set(name, value)
