"""
Pydantic models for updating application configuration settings.

This module defines models used for partial updates to the
application's configuration.
"""

from pydantic import BaseModel


class SettingsUpdate(BaseModel):
    """
    Represents a partial update to the application configuration.

    All fields are optional, allowing callers to update only the
    settings they want to change.
    """

    refresh_interval: int | None = None
    weeks_delta: int | None = None

    canvas_enabled: bool | None = None
    canvas_graphql_url: str | None = None
    canvas_token: str | None = None

    gradescope_enabled: bool | None = None
    gradescope_email: str | None = None
    gradescope_password: str | None = None

    ngrok_enabled: bool | None = None
    ngrok_domain: str | None = None
    ngrok_authtoken: str | None = None
