import threading

import google.generativeai as genai

from errors import ProviderError


class GeminiClient:
    """Request-scoped Gemini credentials over the SDK's global configuration."""

    _lock = threading.Lock()

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate_content(self, prompt, generation_config=None):
        try:
            with self._lock:
                genai.configure(api_key=self.api_key)
                return genai.GenerativeModel(self.model).generate_content(
                    prompt, generation_config=generation_config
                )
        except Exception as exc:
            raise ProviderError("Gemini request failed") from exc
