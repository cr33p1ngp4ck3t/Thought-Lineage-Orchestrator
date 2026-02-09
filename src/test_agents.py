"""
Test script for multi-agent coordination.
"""
import sys
sys.path.insert(0, '.')

from orchestrator import ThoughtLineageOrchestrator

def test_multi_agent_coordination():
    """Test the full multi-agent reasoning pipeline."""

    print("="*80)
    print(" TESTING MULTI-AGENT THOUGHT LINEAGE ORCHESTRATOR")
    print("="*80)

    # Create orchestrator
    orchestrator = ThoughtLineageOrchestrator()

    # Test problem (simplified for speed)
    problem = "Plan a product launch for a new AI tool. Consider market timing and competitive landscape."
    constraints = [
        "Budget: $100K",
        "Timeline: 3 months",
        "Target market: B2B SaaS companies"
    ]

    print(f"\n[PROBLEM]")
    print(f"  {problem}")
    print(f"\n[CONSTRAINTS]")
    for c in constraints:
        print(f"  - {c}")

    # Process through agents
    try:
        results = orchestrator.process_problem(problem, constraints)

        print("\n" + "="*80)
        print(" RESULTS")
        print("="*80)

        print(f"\n[FINAL CONCLUSION]")
        print(f"  {results['final_conclusion']}\n")

        print(f"[GRAPH STATS]")
        graph = results['graph']
        print(f"  Nodes: {len(graph['nodes'])}")
        print(f"  Edges: {len(graph['edges'])}")

        print(f"\n[SIGNATURE SUMMARY]")
        for i, sig in enumerate(results['signatures'], 1):
            print(f"  {i}. {sig['agent_id']}: {sig['conclusion'][:80]}...")
            print(f"     Confidence: {sig['confidence_score']:.2f}")

        # Save graph
        orchestrator.save_graph("reasoning_graph.json")

        print("\n[SUCCESS] Multi-agent coordination working!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_multi_agent_coordination()
    sys.exit(0 if success else 1)
