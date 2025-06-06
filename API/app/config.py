from typing import List, Union

from app.utils.logging import logging
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

load_dotenv()


class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(
        description="API Key for Gemini",
    )
    GEMINI_MODEL_NAME: str = Field(
        description="Model to use for Gemini",
        default="gemini-2.5-flash-preview-05-20",
    )
    GEMINI_TEMPERATURE: float = Field(
        description="Temperature for Gemini",
        default=0.0,
    )
    GEMINI_MAX_TOKENS: int = Field(
        description="Max tokens for Gemini",
        default=65536,
    )
    GEMINI_TOP_P: float = Field(
        description="Top P for Gemini",
        default=0.95,
    )

    GEMINI_GROUNDING_ENABLED: bool = Field(
        description="Whether to enable grounding for Gemini",
        default=True,
    )

    APP_TITLE: str = Field(
        description="Title of the application",
        default="TR Squad Finder POC",
    )
    APP_DESCRIPTION: str = Field(
        description="Description of the application",
        default="POC of application which can return accurate squad information for premier league teams upon a natural language request.",
    )
    APP_VERSION: str = Field(
        description="Version of the application",
        default="0.1.0",
    )

    PUBLIC_END_USER_UI_URL: Union[str, List[str]] = Field(
        description="Public end user UI URL",
        default=["http://localhost:3000"],
    )

    VERCEL_PROJECT_PREFIX: str = Field(
        description="Vercel project prefix",
        default="tr-squad-poc",
    )
    VERCEL_PROJECT_SUFFIX: str = Field(
        description="Vercel project suffix",
        default="vercel-app",
    )

    @field_validator("PUBLIC_END_USER_UI_URL", mode="after")
    @classmethod
    def parse_comma_separated_urls(cls, value):
        """
        Parse comma-separated URLs into a list.

        Args:
            value (str or list): Comma-separated string or list of URLs.

        Returns:
            list: List of URLs.
        """
        if isinstance(value, str):
            return [url.strip() for url in value.split(",")]
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields


# Create a global settings object
settings = Settings()
