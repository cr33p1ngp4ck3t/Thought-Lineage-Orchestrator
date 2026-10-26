import pytest
from pydantic import ValidationError

from errors import ContradictionDetectionError, ProviderError
from intelligence import ContradictionDetector, Synthesizer
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


def test_detector_uses_injected_client():
    client = FakeGeminiClient({"has_contradiction": False})
    result = ContradictionDetector(client).detect(make_signature("a"), make_signature("b"))
    assert result["has_contradiction"] is False
    assert result["signatures_compared"] == ["a", "b"]
    assert len(client.prompts) == 1



def test_synthesizer_uses_injected_client():
    client = FakeGeminiClient(signature_payload("Hybrid"))
    result = Synthesizer(client).synthesize(make_signature("a"), make_signature("b"), {"contradiction_type": "assumption", "severity": 0.8})
    assert result["conclusion"] == "Hybrid"
    assert result["context"]["parent_signatures"] == ["a", "b"]
    assert len(client.prompts) == 1
