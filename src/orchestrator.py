"""
Thought Lineage Orchestrator (TLO) - Core coordination system.
Manages thought signatures and reasoning lineage across multiple agents.
"""
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)


class ThoughtSignature:
    """Represents a single thought signature from an agent."""

    def __init__(
        self,
        agent_id: str,
        reasoning_type: str,
        reasoning_chain: List[Dict],
        conclusion: str,
        confidence_score: float,
        parent_signatures: Optional[List[str]] = None,
        input_data: Optional[Dict] = None,
        constraints: Optional[List[str]] = None,
        alternative_paths: Optional[List[Dict]] = None
    ):
        self.signature_id = str(uuid.uuid4())
        self.agent_id = agent_id
        self.timestamp = datetime.now().isoformat()
        self.reasoning_type = reasoning_type
        self.context = {
            "parent_signatures": parent_signatures or [],
            "input_data": input_data or {},
            "constraints": constraints or []
        }
        self.reasoning_chain = reasoning_chain
        self.conclusion = conclusion
        self.confidence_score = confidence_score
        self.alternative_paths = alternative_paths or []

    def to_dict(self) -> Dict:
        """Convert signature to dictionary format."""
        return {
            "signature_id": self.signature_id,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "reasoning_type": self.reasoning_type,
            "context": self.context,
            "reasoning_chain": self.reasoning_chain,
            "conclusion": self.conclusion,
            "confidence_score": self.confidence_score,
            "alternative_paths": self.alternative_paths
        }

    def to_json(self) -> str:
        """Convert signature to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class ReasoningGraph:
    """Manages the directed acyclic graph of thought signatures."""

    def __init__(self):
        self.nodes: Dict[str, ThoughtSignature] = {}  # signature_id -> ThoughtSignature
        self.edges: Dict[str, List[str]] = {}  # parent_id -> [child_id, ...]

    def add_signature(self, signature: ThoughtSignature):
        """Add a thought signature to the graph."""
        self.nodes[signature.signature_id] = signature

        # Add edges from parent signatures
        for parent_id in signature.context["parent_signatures"]:
            if parent_id not in self.edges:
                self.edges[parent_id] = []
            self.edges[parent_id].append(signature.signature_id)

    def get_signature(self, signature_id: str) -> Optional[ThoughtSignature]:
        """Retrieve a signature by ID."""
        return self.nodes.get(signature_id)

    def get_children(self, signature_id: str) -> List[ThoughtSignature]:
        """Get all child signatures of a given signature."""
        child_ids = self.edges.get(signature_id, [])
        return [self.nodes[child_id] for child_id in child_ids if child_id in self.nodes]

    def get_lineage(self, signature_id: str) -> List[ThoughtSignature]:
        """Get the complete lineage (ancestors) of a signature."""
        lineage = []
        signature = self.get_signature(signature_id)
        if not signature:
            return lineage

        # Recursively collect parent signatures
        for parent_id in signature.context["parent_signatures"]:
            parent = self.get_signature(parent_id)
            if parent:
                lineage.append(parent)
                lineage.extend(self.get_lineage(parent_id))

        return lineage

    def to_dict(self) -> Dict:
        """Export graph structure for visualization."""
        return {
            "nodes": [
                {
                    "id": sig_id,
                    "agent": sig.agent_id,
                    "type": sig.reasoning_type,
                    "conclusion": sig.conclusion,
                    "confidence": sig.confidence_score,
                    "timestamp": sig.timestamp
                }
                for sig_id, sig in self.nodes.items()
            ],
            "edges": [
                {"source": parent_id, "target": child_id}
                for parent_id, child_ids in self.edges.items()
                for child_id in child_ids
            ]
        }


class ThoughtLineageOrchestrator:
    """
    Main orchestrator that coordinates agents and manages reasoning lineage.
    """

    def __init__(self):
        self.graph = ReasoningGraph()
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def register_signature(self, signature: ThoughtSignature) -> str:
        """Register a new thought signature in the reasoning graph."""
        self.graph.add_signature(signature)
        print(f"[+] Registered signature {signature.signature_id[:8]}... from {signature.agent_id}")
        return signature.signature_id

    def get_graph_visualization_data(self) -> Dict:
        """Get graph data formatted for visualization."""
        return self.graph.to_dict()

    def get_signature_details(self, signature_id: str) -> Optional[Dict]:
        """Get detailed information about a specific signature."""
        signature = self.graph.get_signature(signature_id)
        return signature.to_dict() if signature else None

    def export_lineage(self, signature_id: str) -> Dict:
        """Export the complete lineage for a given signature."""
        signature = self.graph.get_signature(signature_id)
        if not signature:
            return {"error": "Signature not found"}

        lineage = self.graph.get_lineage(signature_id)
        return {
            "target_signature": signature.to_dict(),
            "lineage": [sig.to_dict() for sig in lineage],
            "lineage_depth": len(lineage)
        }

    def process_problem(self, problem: str, constraints: Optional[List[str]] = None) -> Dict:
        """
        Process a problem through multiple agents and manage their reasoning.

        Args:
            problem: The problem statement to solve
            constraints: Optional list of constraints to consider

        Returns:
            Dictionary containing final result and complete reasoning graph
        """
        from agents import AnalyzerAgent, PlannerAgent, ExecutorAgent

        print(f"\n[*] Processing problem: {problem[:100]}...")

        # Create specialized agents
        analyzer = AnalyzerAgent()
        planner = PlannerAgent()
        executor = ExecutorAgent()

        signatures = []

        # Phase 1: Analysis
        print("[PHASE 1] Running analysis...")
        analysis_data = analyzer.analyze(problem, constraints)
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
        self.register_signature(analysis_sig)
        signatures.append(analysis_sig)
        print(f"  -> Analysis complete: {analysis_sig.conclusion[:100]}...")

        # Phase 2: Planning (using analysis)
        print("[PHASE 2] Creating plan...")
        planning_data = planner.plan(
            problem,
            analysis_signatures=[analysis_sig.to_dict()],
            constraints=constraints
        )
        planning_sig = ThoughtSignature(
            agent_id=planning_data['agent_id'],
            reasoning_type=planning_data['reasoning_type'],
            reasoning_chain=planning_data['reasoning_chain'],
            conclusion=planning_data['conclusion'],
            confidence_score=planning_data['confidence_score'],
            parent_signatures=planning_data['context'].get('parent_signatures', []),
            input_data=planning_data['context'].get('input_data', {}),
            constraints=planning_data['context'].get('constraints', []),
            alternative_paths=planning_data.get('alternative_paths', [])
        )
        self.register_signature(planning_sig)
        signatures.append(planning_sig)
        print(f"  -> Plan complete: {planning_sig.conclusion[:100]}...")

        # Phase 3: Execution planning
        print("[PHASE 3] Planning execution...")
        execution_data = executor.execute_plan(
            problem,
            planning_signatures=[planning_sig.to_dict()],
            constraints=constraints
        )
        execution_sig = ThoughtSignature(
            agent_id=execution_data['agent_id'],
            reasoning_type=execution_data['reasoning_type'],
            reasoning_chain=execution_data['reasoning_chain'],
            conclusion=execution_data['conclusion'],
            confidence_score=execution_data['confidence_score'],
            parent_signatures=execution_data['context'].get('parent_signatures', []),
            input_data=execution_data['context'].get('input_data', {}),
            constraints=execution_data['context'].get('constraints', []),
            alternative_paths=execution_data.get('alternative_paths', [])
        )
        self.register_signature(execution_sig)
        signatures.append(execution_sig)
        print(f"  -> Execution plan complete: {execution_sig.conclusion[:100]}...")

        results = {
            "problem": problem,
            "signatures": [sig.to_dict() for sig in signatures],
            "final_conclusion": execution_sig.conclusion,
            "graph": self.get_graph_visualization_data()
        }

        return results

    def save_graph(self, filepath: str):
        """Save the reasoning graph to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.graph.to_dict(), f, indent=2)
        print(f"[SAVED] Saved reasoning graph to {filepath}")


# Simple test to verify API connection
if __name__ == "__main__":
    print("[TEST] Testing Gemini 3 API connection...")
    try:
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        response = model.generate_content("Say 'API connection successful!' and nothing else.")
        print(f"[OK] {response.text.strip()}")

        print("\n[TEST] Testing ThoughtLineageOrchestrator...")
        orchestrator = ThoughtLineageOrchestrator()

        # Create a test signature
        test_sig = ThoughtSignature(
            agent_id="test-agent",
            reasoning_type="analysis",
            reasoning_chain=[
                {
                    "step": 1,
                    "thought": "This is a test thought",
                    "confidence": 0.9
                }
            ],
            conclusion="Test successful",
            confidence_score=0.9
        )

        sig_id = orchestrator.register_signature(test_sig)
        print(f"[OK] Created test signature: {sig_id[:8]}...")

        # Test graph export
        graph_data = orchestrator.get_graph_visualization_data()
        print(f"[OK] Graph has {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")

        print("\n[SUCCESS] All Phase 1 core components working!")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
