"""
Synthesizer - Resolves contradictions and creates hybrid solutions.
"""
import json
from typing import Dict, List
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)


class Synthesizer:
    """Synthesizes conflicting reasoning paths into coherent solutions."""

    def __init__(self):
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def synthesize(
        self,
        signature_a: Dict,
        signature_b: Dict,
        contradiction: Dict
    ) -> Dict:
        """
        Synthesize two conflicting signatures into a coherent resolution.

        Args:
            signature_a: First thought signature
            signature_b: Second thought signature
            contradiction: Contradiction analysis

        Returns:
            New synthesized thought signature
        """
        prompt = f"""
You are the Orchestrator synthesizing conflicting reasoning paths.

PATH 1 (from {signature_a['agent_id']}):
Conclusion: {signature_a['conclusion']}
Confidence: {signature_a['confidence_score']}

PATH 2 (from {signature_b['agent_id']}):
Conclusion: {signature_b['conclusion']}
Confidence: {signature_b['confidence_score']}

CONTRADICTION DETECTED:
Type: {contradiction['contradiction_type']}
Severity: {contradiction['severity']}
Root Cause: {contradiction['root_cause']}
Suggested Resolution: {contradiction['resolution_suggestion']}

Create a hybrid solution that:
1. Preserves the strengths of both reasoning paths
2. Resolves the logical inconsistency
3. Maximizes overall confidence
4. Explains why this synthesis is superior to either individual path

Generate a new thought signature with the same JSON structure:
{{
  "reasoning_chain": [
    {{
      "step": 1,
      "thought": "synthesis reasoning",
      "confidence": 0.0-1.0,
      "evidence": ["supporting facts"]
    }}
  ],
  "conclusion": "synthesized recommendation",
  "confidence_score": 0.0-1.0,
  "alternative_paths": [
    {{
      "reasoning": "original Path 1 approach",
      "why_rejected": "reason for not using it exclusively",
      "confidence": {signature_a['confidence_score']}
    }},
    {{
      "reasoning": "original Path 2 approach",
      "why_rejected": "reason for not using it exclusively",
      "confidence": {signature_b['confidence_score']}
    }}
  ],
  "synthesis_explanation": "why this hybrid approach is optimal"
}}

Output ONLY the JSON.
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.5
                }
            )

            synthesis_data = json.loads(response.text)

            # Add metadata
            synthesis_data["agent_id"] = "synthesizer-orchestrator"
            synthesis_data["reasoning_type"] = "synthesis"
            synthesis_data["context"] = {
                "parent_signatures": [
                    signature_a["signature_id"],
                    signature_b["signature_id"]
                ],
                "input_data": {"contradiction": contradiction},
                "constraints": []
            }

            return synthesis_data

        except Exception as e:
            print(f"[ERROR] Synthesis failed: {e}")
            # Return fallback: choose higher confidence path
            higher_conf = signature_a if signature_a['confidence_score'] > signature_b['confidence_score'] else signature_b
            return {
                "agent_id": "synthesizer-orchestrator",
                "reasoning_type": "synthesis",
                "reasoning_chain": [
                    {
                        "step": 1,
                        "thought": f"Synthesis failed, defaulting to higher confidence path from {higher_conf['agent_id']}",
                        "confidence": higher_conf['confidence_score'],
                        "evidence": ["Automatic fallback due to synthesis error"]
                    }
                ],
                "conclusion": higher_conf['conclusion'],
                "confidence_score": higher_conf['confidence_score'] * 0.9,  # Slight penalty
                "alternative_paths": [],
                "synthesis_explanation": f"Fallback to {higher_conf['agent_id']} due to synthesis error: {str(e)}",
                "context": {
                    "parent_signatures": [signature_a["signature_id"], signature_b["signature_id"]],
                    "input_data": {},
                    "constraints": []
                }
            }
