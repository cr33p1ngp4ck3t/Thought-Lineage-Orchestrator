from types import SimpleNamespace

import pytest

import app as app_module
from config import Config
from tests.fakes import FakeGeminiClient, signature_payload


class FakeOrchestrator:
    def __init__(self, client):
        self.client = client

    def process_problem(self, problem):
        return {
            "problem": problem,
            "signatures": [],
            "final_conclusion": "ok",
            "graph": {"nodes": [], "edges": []},
        }


def test_process_rejects_non_object_json():
    response = app_module.app.test_client().post("/api/process", json=[])

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be a JSON object"


def test_custom_key_is_request_local(monkeypatch):
    keys = []

    def client_factory(api_key, model):
        keys.append(api_key)
        return SimpleNamespace()

    monkeypatch.setattr(app_module, "GeminiClient", client_factory)
    monkeypatch.setattr(app_module, "ThoughtLineageOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(Config, "GEMINI_API_KEY", None)
    client = app_module.app.test_client()

    first = client.post("/api/process", json={"problem": "First", "api_key": "request-key"})
    second = client.post("/api/process", json={"problem": "Second"})

    assert first.status_code == 200
    assert second.status_code == 400
    assert keys == ["request-key"]
    assert Config.GEMINI_API_KEY is None


def test_graph_endpoint_does_not_expose_shared_results():
    response = app_module.app.test_client().get("/api/graph")

    assert response.status_code == 410
