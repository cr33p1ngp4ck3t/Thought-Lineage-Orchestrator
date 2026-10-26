"""
Configuration module for Thought Lineage Orchestrator.
Manages API keys and environment settings.
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for TLO system."""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Model selection (using Gemini 3 Flash for speed and cost-efficiency)
    GEMINI_MODEL = "gemini-3-flash-preview"

    # System settings
    MAX_REASONING_STEPS = 10
    DEFAULT_TEMPERATURE = 0.7
    MAX_CONTENT_LENGTH = 64 * 1024

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. Please set it in .env file or provide one in the web UI."
            )
        return True

    @classmethod
    def is_configured(cls):
        """Check if API key is configured without raising."""
        return bool(cls.GEMINI_API_KEY)


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s level=%(levelname)s logger=%(name)s message=%(message)s",
)

# Warn but don't crash at import - users can provide API key via the web UI
if not Config.is_configured():
    logging.getLogger(__name__).warning(
        "GEMINI_API_KEY is not set; requests must provide an API key"
    )
