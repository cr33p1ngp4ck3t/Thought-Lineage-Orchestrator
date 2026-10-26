import pytest

from errors import SignatureGenerationError
from orchestrator import ReasoningGraph, ThoughtLineageOrchestrator, ThoughtSignature
from tests.fakes import FakeGeminiClient, signature_payload


def test_thought_signature_serializes_context():
    signature = ThoughtSignature(
        agent_id="agent",
        reasoning_type="analysis",
        reasoning_chain=[],
        conclusion="Result",
        confidence_score=0.75,
        parent_signatures=["parent"],
        constraints=["budget"],
    )

    result = signature.to_dict()

    assert result["signature_id"]
    assert result["context"] == {
        "parent_signatures": ["parent"],
        "input_data": {},
        "constraints": ["budget"],
    }


def test_reasoning_graph_returns_complete_lineage():
    graph = ReasoningGraph()
    root = ThoughtSignature("root", "analysis", [], "Root", 0.9)
    child = ThoughtSignature(
        "child", "decision", [], "Child", 0.8, parent_signatures=[root.signature_id]
    )
    leaf = ThoughtSignature(
        "leaf", "evaluation", [], "Leaf", 0.7, parent_signatures=[child.signature_id]
    )
    for signature in (root, child, leaf):
        graph.add_signature(signature)

    assert graph.get_lineage(leaf.signature_id) == [child, root]


def test_orchestrator_runs_offline_with_injected_client():
    client = FakeGeminiClient(
        signature_payload("Analysis"),
        signature_payload("Plan"),
        signature_payload("Execution"),
    )

    result = ThoughtLineageOrchestrator(client).process_problem("Launch a product")

    assert result["final_conclusion"] == "Execution"
    assert [item["agent_id"] for item in result["signatures"]] == [
        "analyzer-agent",
        "planner-agent",
        "executor-agent",
    ]
    assert len(result["graph"]["nodes"]) == 3


def test_orchestrator_rejects_malformed_model_output():
    client = FakeGeminiClient({"conclusion": "Missing reasoning fields"})

    with pytest.raises(SignatureGenerationError):
        ThoughtLineageOrchestrator(client).process_problem("Launch a product")
