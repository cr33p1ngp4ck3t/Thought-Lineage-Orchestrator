import threading
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

import gemini_client as client_module
from errors import ProviderError
from gemini_client import GeminiClient


def test_clients_configure_their_own_key_for_each_call(monkeypatch):
    configured = []
    models = []

    monkeypatch.setattr(
        client_module.genai, "configure", lambda api_key: configured.append(api_key)
    )

    class Model:
        def __init__(self, name):
            models.append(name)

        def generate_content(self, prompt, generation_config=None):
            return SimpleNamespace(text=prompt)

    monkeypatch.setattr(client_module.genai, "GenerativeModel", Model)

    assert GeminiClient("first-key", "first-model").generate_content("first").text == "first"
    assert GeminiClient("second-key", "second-model").generate_content("second").text == "second"
    assert configured == ["first-key", "second-key"]
    assert models == ["first-model", "second-model"]


def test_provider_errors_do_not_expose_sdk_details(monkeypatch):
    monkeypatch.setattr(client_module.genai, "configure", lambda api_key: None)
    monkeypatch.setattr(
        client_module.genai,
        "GenerativeModel",
        lambda model: (_ for _ in ()).throw(RuntimeError("secret provider detail")),
    )

    with pytest.raises(ProviderError, match="Gemini request failed") as error:
        GeminiClient("request-key", "model").generate_content("prompt")

    assert "secret" not in str(error.value)
