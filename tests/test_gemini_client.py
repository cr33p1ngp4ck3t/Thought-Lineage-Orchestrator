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


def test_overlapping_calls_keep_their_own_credentials(monkeypatch):
    first_started = threading.Event()
    release_first = threading.Event()
    second_configured = threading.Event()
    configured_key = None

    def configure(api_key):
        nonlocal configured_key
        configured_key = api_key
        if api_key == "second-key":
            second_configured.set()

    class Model:
        def __init__(self, name):
            pass

        def generate_content(self, prompt, generation_config=None):
            if prompt == "first":
                first_started.set()
                assert release_first.wait(5)
            return SimpleNamespace(text=f"{prompt}:{configured_key}")

    monkeypatch.setattr(client_module.genai, "configure", configure)
    monkeypatch.setattr(client_module.genai, "GenerativeModel", Model)

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(GeminiClient("first-key", "model").generate_content, "first")
        assert first_started.wait(5)
        second = executor.submit(GeminiClient("second-key", "model").generate_content, "second")
        try:
            assert not second_configured.wait(0.2)
        finally:
            release_first.set()

        assert first.result(timeout=5).text == "first:first-key"
        assert second.result(timeout=5).text == "second:second-key"
