import pytest
from pydantic import ValidationError

from errors import ContradictionDetectionError, ProviderError
from intelligence import ContradictionDetector, Synthesizer
from schemas import ContradictionResponse
from tests.fakes import FakeGeminiClient, signature_payload


def make_signature(identifier, confidence=0.8):
    return {
        "signature_id": identifier,
        "agent_id": identifier,
        "reasoning_chain": [],
        "conclusion": identifier,
        "confidence_score": confidence,
    }



def test_detection_failure_is_not_reported_as_no_contradiction():
    detector = ContradictionDetector(FakeGeminiClient(ProviderError("unavailable")))

    with pytest.raises(ContradictionDetectionError):
        detector.detect(make_signature("a"), make_signature("b"))



def test_malformed_detection_output_is_an_explicit_error():
    detector = ContradictionDetector(FakeGeminiClient({"has_contradiction": False}))

    with pytest.raises(ContradictionDetectionError):
        detector.detect(make_signature("a"), make_signature("b"))



def test_synthesis_failure_is_explicitly_degraded():
    synthesizer = Synthesizer(FakeGeminiClient(ProviderError("unavailable")))

    result = synthesizer.synthesize(
        make_signature("a", 0.9),
        make_signature("b", 0.7),
        {"contradiction_type": "assumption", "severity": 0.8},
    )

    assert result["conclusion"] == "a"
    assert result["degraded"] is True
    assert "unavailable" not in result["synthesis_explanation"]


def test_detector_uses_injected_client():
    client = FakeGeminiClient({
        "has_contradiction": False, "contradiction_type": "none", "severity": 0,
        "assumption_a": "", "assumption_b": "", "logical_incompatibility": "",
        "divergence_point": "", "fundamental_tradeoff": "", "root_cause": "",
        "resolution_suggestion": "", "conflicting_elements": [],
    })
    result = ContradictionDetector(client).detect(make_signature("a"), make_signature("b"))
    assert result["has_contradiction"] is False
    assert result["signatures_compared"] == ["a", "b"]
    assert len(client.prompts) == 1



def test_synthesizer_uses_injected_client():
    payload = signature_payload("Hybrid")
    payload.update(
        arbitration_log={"deprioritized_assumption": "Growth", "hybrid_assumption": "Balance", "confidence_justification": "Budget", "risk_resolution": "Limit"},
        synthesis_explanation="Balanced plan",
    )
    client = FakeGeminiClient(payload)
    result = Synthesizer(client).synthesize(make_signature("a"), make_signature("b"), {"contradiction_type": "assumption", "severity": 0.8})
    assert result["conclusion"] == "Hybrid"
    assert result["context"]["parent_signatures"] == ["a", "b"]
    assert len(client.prompts) == 1
