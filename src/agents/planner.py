"""
Planner Agent - Creates action sequences based on analysis.
"""
from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Specialized agent for strategic planning and sequencing.
    Takes analysis and creates actionable plans with timing and dependencies.
    """

    def __init__(self):
        super().__init__(
            agent_id="planner-agent",
            role_description="Strategic Planning Specialist - creates actionable plans with timing, sequencing, and resource allocation"
        )

    def plan(self, problem: str, analysis_signatures: list = None, constraints: list = None) -> dict:
        """
        Create a plan based on the problem and prior analysis.

        Args:
            problem: The problem statement to plan for
            analysis_signatures: Previous analysis signatures for context
            constraints: Optional list of constraints

        Returns:
            Thought signature dictionary
        """
        return self.generate_signature(
            problem=problem,
            reasoning_type="decision",
            parent_signatures=analysis_signatures,
            constraints=constraints
        )
