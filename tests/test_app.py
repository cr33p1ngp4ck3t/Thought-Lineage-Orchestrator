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



def test_health_endpoint():
    response = app_module.app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}



def test_process_rejects_non_object_json():
    response = app_module.app.test_client().post("/api/process", json=[])

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be a JSON object"



def test_process_validates_fields():
    response = app_module.app.test_client().post(
        "/api/process", json={"problem": "   ", "mode": "unknown", "api_key": "secret"}
    )

    assert response.status_code == 400
    fields = {error["field"] for error in response.get_json()["details"]}
    assert fields == {"problem", "mode"}



def test_process_rejects_oversized_json_with_json_error():
    response = app_module.app.test_client().post(
        "/api/process", json={"problem": "x" * 70_000, "api_key": "secret"}
    )

    assert response.status_code == 413
    assert response.get_json() == {"error": "Request body is too large"}



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



@pytest.mark.parametrize("server_key", ["   ", "x" * 1001])
def test_invalid_server_key_is_rejected_before_provider(monkeypatch, server_key):
    monkeypatch.setattr(Config, "GEMINI_API_KEY", server_key)

    def unexpected_client(*_):
        pytest.fail("Invalid server credential reached the provider")

    monkeypatch.setattr(app_module, "GeminiClient", unexpected_client)
    response = app_module.app.test_client().post("/api/process", json={"problem": "First"})

    assert response.status_code == 400



@pytest.mark.parametrize("synthesis_fails", [False, True])
def test_parallel_response_preserves_lineage_and_fallback(monkeypatch, synthesis_fails):
    contradiction = {
        "has_contradiction": True,
        "contradiction_type": "assumption",
        "severity": 0.8,
        "assumption_a": "Growth first",
        "assumption_b": "Margins first",
        "logical_incompatibility": "Competing budgets",
        "divergence_point": "Budget allocation",
        "fundamental_tradeoff": "Growth versus margin",
        "root_cause": "Different priorities",
        "resolution_suggestion": "Split the budget",
        "conflicting_elements": ["Budget"],
    }
    synthesis = signature_payload("Hybrid")
    synthesis.update(
        arbitration_log={
            "deprioritized_assumption": "Growth at any cost",
            "hybrid_assumption": "Grow within margins",
            "confidence_justification": "Both constraints met",
            "risk_resolution": "Bound the budget",
        },
        synthesis_explanation="Balance both goals",
    )
    monkeypatch.setattr(
        app_module, "GeminiClient", lambda *_: FakeGeminiClient(
            signature_payload("Analysis"), signature_payload("Growth", 0.9),
            signature_payload("Revenue", 0.7), contradiction,
            RuntimeError("private provider detail") if synthesis_fails else synthesis,
        )
    )

    response = app_module.app.test_client().post(
        "/api/process", json={"problem": "Pricing", "mode": "parallel", "api_key": "request-key"}
    )
    result = response.get_json()

    assert response.status_code == 200
    assert result["final_conclusion"] == ("Growth" if synthesis_fails else "Hybrid")
    assert len(result["graph"]["nodes"]) == 4
    assert len(result["graph"]["edges"]) == 4
    signatures = result["signatures"]
    assert signatures[-1]["context"]["parent_signatures"] == [
        signatures[1]["signature_id"], signatures[2]["signature_id"]
    ]
    assert signatures[-1].get("degraded", False) is synthesis_fails
    assert "private provider detail" not in response.get_data(as_text=True)
