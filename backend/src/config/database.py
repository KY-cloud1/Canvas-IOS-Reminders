"""
Provides persistent storage for application configuration.

This module manages the application's SQLite settings database,
including database initialization and operations for storing,
retrieving, updating, and deleting configuration values.
"""

import sqlite3
from pathlib import Path

# Filepath to the settings file.
DB_PATH = Path(__file__).resolve().parent / "settings.db"


# Default settings used upon initialization.
DEFAULT_SETTINGS = {
    "refresh_interval": "3600",  # 3600 seconds = 60 minutes
    "weeks_delta": "10",  # Standard academic quarter
    "canvas_enabled": "false",
    "canvas_graphql_url": "",
    "gradescope_enabled": "false",
    "ngrok_enabled": "false",
    "ngrok_domain": "",
}


class Database:
    """
    Manage access to the application's SQLite settings database.

    This class provides a simple interface for initializing the
    database, storing key-value pairs, retrieving stored values,
    updating, and deleting configuration values. Each database
    operation uses its own SQLite connection.
    """

    @classmethod
    def _connect(cls) -> sqlite3.Connection:
        """
        Open a new SQLite database connection.

        Returns:
            A new SQLite connection configured to return rows by column
            name.
        """
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the settings database.

        Creates the settings table if necessary and inserts any missing
        default settings from DEFAULT_SETTINGS. The database connection
        is closed after initialization.
        """
        conn = cls._connect()

        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )

            for key, value in DEFAULT_SETTINGS.items():
                conn.execute(
                    """
                    INSERT OR IGNORE INTO settings (key, value)
                    VALUES (?, ?)
                    """,
                    (key, value),
                )

            conn.commit()
        finally:
            conn.close()

    @classmethod
    def set(cls, key: str, value: str) -> None:
        """
        Store or update a configuration value.

        If a setting with the specified key already exists, its value
        is replaced. Otherwise, a new setting is created.

        Args:
            key: The unique identifier for the setting.
            value: The value to associate with the key.
        """
        conn = cls._connect()

        try:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, value),
            )

            conn.commit()
        finally:
            conn.close()

    @classmethod
    def get(cls, key: str) -> str:
        """
        Retrieve a stored configuration value.

        Args:
            key: The unique identifier for the setting.

        Returns:
            The stored value associated with the key.

        Raises:
            KeyError: If no setting exists for the specified key.
        """
        conn = cls._connect()

        try:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = ?",
                (key,),
            ).fetchone()

            if row is None:
                raise KeyError(f"Setting {key!r} does not exist.")

            return row["value"]
        finally:
            conn.close()

    @classmethod
    def delete(cls, key: str) -> None:
        """
        Delete a stored configuration value.

        If the specified key does not exist, this method has no effect.

        Args:
            key: The unique identifier for the setting to remove.
        """
        conn = cls._connect()

        try:
            conn.execute(
                "DELETE FROM settings WHERE key = ?",
                (key,),
            )

            conn.commit()
        finally:
            conn.close()

    @classmethod
    def exists(cls, key: str) -> bool:
        """
        Check whether a configuration value exists.

        Args:
            key: The unique identifier for the setting.

        Returns:
            True if the specified key exists in the database, otherwise
            False.
        """
        conn = cls._connect()

        try:
            row = conn.execute(
                "SELECT EXISTS(SELECT 1 FROM settings WHERE key = ?)",
                (key,),
            ).fetchone()

            return bool(row[0])
        finally:
            conn.close()

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """
        Retrieve all stored configuration values.

        Returns:
            A dictionary mapping each setting key to its corresponding
            value. If no settings are stored, an empty dictionary is
            returned.
        """
        conn = cls._connect()

        try:
            rows = conn.execute(
                "SELECT key, value FROM settings",
            ).fetchall()

            return {row["key"]: row["value"] for row in rows}
        finally:
            conn.close()
