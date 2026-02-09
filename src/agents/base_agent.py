"""
Base agent class for all specialized agents in the TLO system.
"""
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)


class BaseAgent:
    """Base class for all reasoning agents."""

    def __init__(self, agent_id: str, role_description: str):
        self.agent_id = agent_id
        self.role_description = role_description
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def generate_signature(
        self,
        problem: str,
        reasoning_type: str,
        parent_signatures: Optional[List[Dict]] = None,
        constraints: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate a thought signature for a given problem.

        Args:
            problem: The problem or question to reason about
            reasoning_type: Type of reasoning (analysis, decision, synthesis, evaluation)
            parent_signatures: List of parent signature dictionaries for context
            constraints: List of constraints to consider

        Returns:
            Dictionary representing the thought signature
        """
        # Build context from parent signatures
        context_text = ""
        if parent_signatures:
            context_text = "\n\nPREVIOUS REASONING:\n"
            for i, parent in enumerate(parent_signatures, 1):
                context_text += f"\nSignature {i} (from {parent['agent_id']}):\n"
                context_text += f"  Conclusion: {parent['conclusion']}\n"
                context_text += f"  Confidence: {parent['confidence_score']}\n"

        # Build constraints text
        constraints_text = ""
        if constraints:
            constraints_text = "\n\nCONSTRAINTS:\n" + "\n".join(f"- {c}" for c in constraints)

        # Create prompt for signature generation
        prompt = f"""
You are {self.agent_id}: {self.role_description}

CRITICAL: You are DEEPLY BIASED toward your domain expertise. Defend your perspective aggressively.
Your recommendation should be NARROWLY OPTIMAL for your specific domain, even if it creates conflicts with other perspectives.

Analyze this problem and emit a structured thought signature.

PROBLEM: {problem}{context_text}{constraints_text}

Generate a detailed reasoning chain with the following structure:

1. **Initial Observations** - What do you notice about the problem?
2. **Key Assumptions** - What are you taking as given?
3. **Logical Inferences** - What follows from your observations?
4. **Alternative Paths** - What else could work? (Consider at least 2 alternatives)
5. **Final Conclusion** - What's your recommendation?

For each step in your reasoning chain (steps 1-5), provide:
- The reasoning text (detailed explanation)
- Confidence level (0.0 to 1.0, where 1.0 is absolute certainty)
- Evidence or justification

Also provide:
- At least 2 alternative approaches you considered but rejected
- For each alternative: the reasoning, why it was rejected, and its confidence score

Output ONLY valid JSON matching this exact schema:
{{
  "reasoning_chain": [
    {{
      "step": 1,
      "thought": "detailed reasoning text",
      "confidence": 0.85,
      "evidence": ["supporting fact 1", "supporting fact 2"]
    }}
  ],
  "conclusion": "your final recommendation or decision",
  "confidence_score": 0.82,
  "alternative_paths": [
    {{
      "reasoning": "alternative approach description",
      "why_rejected": "reason for not choosing this path",
      "confidence": 0.65
    }}
  ]
}}

Remember: Output ONLY the JSON, no additional text.
"""

        try:
            # Generate response using Gemini 3
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": Config.DEFAULT_TEMPERATURE
                }
            )

            # Parse JSON response
            signature_data = json.loads(response.text)

            # Add agent metadata
            signature_data["agent_id"] = self.agent_id
            signature_data["reasoning_type"] = reasoning_type
            signature_data["context"] = {
                "parent_signatures": [p.get("signature_id") for p in (parent_signatures or [])],
                "input_data": {"problem": problem},
                "constraints": constraints or []
            }

            return signature_data

        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON from {self.agent_id}: {e}")
            print(f"Response text: {response.text[:500]}")
            raise
        except Exception as e:
            print(f"[ERROR] {self.agent_id} failed to generate signature: {e}")
            raise

    def __str__(self):
        return f"{self.agent_id} ({self.role_description})"
