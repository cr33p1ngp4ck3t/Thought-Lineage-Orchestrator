"""
Test contradiction detection and synthesis with parallel planning.
"""
import sys
sys.path.insert(0, '.')

from orchestrator import ThoughtLineageOrchestrator, ThoughtSignature
from agents import AnalyzerAgent, PlannerAgent
from intelligence import ContradictionDetector, Synthesizer


def test_contradiction_detection():
    """Test contradiction detection with deliberately conflicting plans."""

    print("="*80)
    print(" TESTING CONTRADICTION DETECTION & SYNTHESIS")
    print("="*80)

    orchestrator = ThoughtLineageOrchestrator()
    detector = ContradictionDetector()
    synthesizer = Synthesizer()

    # Problem that will generate conflicting opinions
    problem = "Choose the pricing strategy for our AI tool"
    constraints_a = ["Maximize market penetration", "Build large user base quickly", "Compete with free alternatives"]
    constraints_b = ["Maximize revenue and profitability", "Position as premium product", "Target enterprise customers"]

    print(f"\n[PROBLEM] {problem}\n")

    # Get analysis first
    print("[PHASE 1] Initial Analysis...")
    analyzer = AnalyzerAgent()
    analysis_data = analyzer.analyze(problem)
    analysis_sig = ThoughtSignature(
        agent_id=analysis_data['agent_id'],
        reasoning_type=analysis_data['reasoning_type'],
        reasoning_chain=analysis_data['reasoning_chain'],
        conclusion=analysis_data['conclusion'],
        confidence_score=analysis_data['confidence_score'],
        parent_signatures=analysis_data['context'].get('parent_signatures', []),
        input_data=analysis_data['context'].get('input_data', {}),
        constraints=analysis_data['context'].get('constraints', []),
        alternative_paths=analysis_data.get('alternative_paths', [])
    )
    orchestrator.register_signature(analysis_sig)
    print(f"  -> {analysis_sig.conclusion[:100]}...\n")

    # Create TWO planners with different constraints (parallel reasoning)
    print("[PHASE 2] Creating PARALLEL PLANS with COMPETING INCENTIVES...")

    planner_a = PlannerAgent(focus="growth")
    planner_b = PlannerAgent(focus="revenue")

    print("  [Planner A] Growth-Obsessed (100% user acquisition focus)")
    plan_a_data = planner_a.plan(
        problem,
        analysis_signatures=[analysis_sig.to_dict()],
        constraints=constraints_a
    )
    plan_a_sig = ThoughtSignature(
        agent_id="planner-agent-growth-focus",
        reasoning_type=plan_a_data['reasoning_type'],
        reasoning_chain=plan_a_data['reasoning_chain'],
        conclusion=plan_a_data['conclusion'],
        confidence_score=plan_a_data['confidence_score'],
        parent_signatures=[analysis_sig.signature_id],
        input_data=plan_a_data['context'].get('input_data', {}),
        constraints=constraints_a,
        alternative_paths=plan_a_data.get('alternative_paths', [])
    )
    orchestrator.register_signature(plan_a_sig)
    print(f"    -> Plan A: {plan_a_sig.conclusion[:100]}...")
    print(f"    -> Confidence: {plan_a_sig.confidence_score:.2f}\n")

    print("  [Planner B] Margin-Protection (100% profitability focus)")
    plan_b_data = planner_b.plan(
        problem,
        analysis_signatures=[analysis_sig.to_dict()],
        constraints=constraints_b
    )
    plan_b_sig = ThoughtSignature(
        agent_id="planner-agent-revenue-focus",
        reasoning_type=plan_b_data['reasoning_type'],
        reasoning_chain=plan_b_data['reasoning_chain'],
        conclusion=plan_b_data['conclusion'],
        confidence_score=plan_b_data['confidence_score'],
        parent_signatures=[analysis_sig.signature_id],
        input_data=plan_b_data['context'].get('input_data', {}),
        constraints=constraints_b,
        alternative_paths=plan_b_data.get('alternative_paths', [])
    )
    orchestrator.register_signature(plan_b_sig)
    print(f"    -> Plan B: {plan_b_sig.conclusion[:100]}...")
    print(f"    -> Confidence: {plan_b_sig.confidence_score:.2f}\n")

    # Detect contradictions
    print("[PHASE 3] DETECTING CONTRADICTIONS...")
    contradiction = detector.detect(plan_a_sig.to_dict(), plan_b_sig.to_dict())

    if contradiction['has_contradiction']:
        print(f"  [!] REASONING COLLISION DETECTED!")
        print(f"      Type: {contradiction['contradiction_type']}")
        print(f"      Severity: {contradiction['severity']:.2f}")
        print(f"      Agent A Assumes: {contradiction.get('assumption_a', 'N/A')}")
        print(f"      Agent B Assumes: {contradiction.get('assumption_b', 'N/A')}")
        print(f"      Incompatibility: {contradiction.get('logical_incompatibility', contradiction['root_cause'])}")
        print(f"      Trade-off: {contradiction.get('fundamental_tradeoff', 'Not specified')}")
        print(f"      Suggestion: {contradiction['resolution_suggestion']}\n")

        # Synthesize resolution
        print("[PHASE 4] SYNTHESIZING RESOLUTION...")
        synthesis_data = synthesizer.synthesize(
            plan_a_sig.to_dict(),
            plan_b_sig.to_dict(),
            contradiction
        )

        synthesis_sig = ThoughtSignature(
            agent_id=synthesis_data['agent_id'],
            reasoning_type=synthesis_data['reasoning_type'],
            reasoning_chain=synthesis_data['reasoning_chain'],
            conclusion=synthesis_data['conclusion'],
            confidence_score=synthesis_data['confidence_score'],
            parent_signatures=synthesis_data['context'].get('parent_signatures', []),
            input_data=synthesis_data['context'].get('input_data', {}),
            constraints=synthesis_data['context'].get('constraints', []),
            alternative_paths=synthesis_data.get('alternative_paths', [])
        )
        orchestrator.register_signature(synthesis_sig)

        print(f"  [+] CHIEF JUSTICE SYNTHESIS COMPLETE")
        print(f"      Conclusion: {synthesis_sig.conclusion}")
        print(f"      Confidence: {synthesis_sig.confidence_score:.2f}")
        print(f"      Explanation: {synthesis_data.get('synthesis_explanation', 'N/A')}")

        # Show arbitration log if available
        if 'arbitration_log' in synthesis_data:
            arb = synthesis_data['arbitration_log']
            print(f"\n  [⚖️] ARBITRATION LOG:")
            print(f"      Deprioritized: {arb.get('deprioritized_assumption', 'N/A')}")
            print(f"      Hybrid Assumption: {arb.get('hybrid_assumption', 'N/A')}")
            print(f"      Confidence Basis: {arb.get('confidence_justification', 'N/A')}\n")
        else:
            print()

    else:
        print("  [OK] No significant contradictions detected.\n")

    # Final results
    print("="*80)
    print(" RESULTS")
    print("="*80)
    graph = orchestrator.get_graph_visualization_data()
    print(f"\n[GRAPH STATS]")
    print(f"  Nodes: {len(graph['nodes'])}")
    print(f"  Edges: {len(graph['edges'])}")
    print(f"  Signatures: Analysis -> 2 Parallel Plans -> Synthesis\n")

    orchestrator.save_graph("contradiction_demo_graph.json")
    print("[SUCCESS] Contradiction detection and synthesis working!\n")

    return True


if __name__ == "__main__":
    try:
        success = test_contradiction_detection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
