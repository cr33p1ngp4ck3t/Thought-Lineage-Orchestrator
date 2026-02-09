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
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
        return True

# Validate configuration on import
Config.validate()
