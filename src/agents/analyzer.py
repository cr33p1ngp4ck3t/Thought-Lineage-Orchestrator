"""
Analyzer Agent - Breaks down complex problems into sub-components.
"""
from agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    """
    Specialized agent for problem decomposition and analysis.
    Identifies key components, dependencies, and critical factors.
    """

    def __init__(self):
        super().__init__(
            agent_id="analyzer-agent",
            role_description="Problem Decomposition Specialist - breaks complex problems into manageable sub-components and identifies key factors"
        )

    def analyze(self, problem: str, constraints: list = None) -> dict:
        """
        Analyze a problem and break it down into components.

        Args:
            problem: The problem statement to analyze
            constraints: Optional list of constraints

        Returns:
            Thought signature dictionary
        """
        return self.generate_signature(
            problem=problem,
            reasoning_type="analysis",
            parent_signatures=None,
            constraints=constraints
        )
