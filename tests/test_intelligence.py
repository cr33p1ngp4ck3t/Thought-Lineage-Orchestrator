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


def test_detector_uses_injected_client():
    client = FakeGeminiClient({"has_contradiction": False})
    result = ContradictionDetector(client).detect(make_signature("a"), make_signature("b"))
    assert result["has_contradiction"] is False
    assert result["signatures_compared"] == ["a", "b"]
    assert len(client.prompts) == 1
