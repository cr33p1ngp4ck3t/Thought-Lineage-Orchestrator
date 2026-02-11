"""
Configuration module for Thought Lineage Orchestrator.
Manages API keys and environment settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for TLO system."""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Model selection (using Gemini 3 Flash for speed and cost-efficiency)
    GEMINI_MODEL = 'gemini-3-flash-preview'

    # System settings
    MAX_REASONING_STEPS = 10
    DEFAULT_TEMPERATURE = 0.7

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file or provide one in the web UI.")
        return True

    @classmethod
    def is_configured(cls):
        """Check if API key is configured without raising."""
        return bool(cls.GEMINI_API_KEY)

# Warn but don't crash at import - users can provide API key via the web UI
if not Config.is_configured():
    import sys
    print("[WARNING] GEMINI_API_KEY not set. Users must provide an API key via the web UI.", file=sys.stderr)
