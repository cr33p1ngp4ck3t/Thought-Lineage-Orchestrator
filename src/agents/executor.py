"""
Executor Agent - Implements plans and reports results.
"""
from agents.base_agent import BaseAgent


class ExecutorAgent(BaseAgent):
    """
    Specialized agent for plan execution and implementation.
    Takes strategic plans and determines concrete execution steps.
    """

    def __init__(self):
        super().__init__(
            agent_id="executor-agent",
            role_description="Execution Specialist - transforms strategic plans into concrete implementation steps with measurable outcomes"
        )

    def execute_plan(self, problem: str, planning_signatures: list = None, constraints: list = None) -> dict:
        """
        Create execution steps based on the planning phase.

        Args:
            problem: The problem statement
            planning_signatures: Previous planning signatures for context
            constraints: Optional list of constraints

        Returns:
            Thought signature dictionary
        """
        return self.generate_signature(
            problem=f"Create concrete execution steps for: {problem}",
            reasoning_type="evaluation",
            parent_signatures=planning_signatures,
            constraints=constraints
        )
