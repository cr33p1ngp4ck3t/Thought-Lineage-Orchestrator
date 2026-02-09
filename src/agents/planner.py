"""
Planner Agent - Creates action sequences based on analysis.
"""
from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Specialized agent for strategic planning and sequencing.
    Takes analysis and creates actionable plans with timing and dependencies.
    """

    def __init__(self, focus=None):
        if focus == "growth":
            agent_id = "planner-growth-focus"
            role_description = "Growth-Obsessed Strategist - Your ONLY metric is User Acquisition. Your reward function is 100% tied to capturing market share. You MUST prioritize rapid adoption even if it means burning cash or accepting risks. Budget overruns are acceptable if they accelerate growth."
        elif focus == "revenue":
            agent_id = "planner-revenue-focus"
            role_description = "Margin-Protection Strategist - Your ONLY metric is Unit Economics and Profitability. Your reward function is 100% tied to protecting margins. You MUST block any strategy that lowers pricing or increases CAC, even if it limits growth. Cash flow survival trumps market share."
        else:
            agent_id = "planner-agent"
            role_description = "Strategic Planning Specialist - creates actionable plans with timing, sequencing, and resource allocation"

        super().__init__(agent_id=agent_id, role_description=role_description)

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
