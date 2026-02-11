"""
Contradiction Detector - Identifies logical conflicts between reasoning paths.
"""
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from config import Config

if Config.is_configured():
    genai.configure(api_key=Config.GEMINI_API_KEY)


class ContradictionDetector:
    """Detects and analyzes contradictions between thought signatures."""

    def __init__(self):
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def detect(self, signature_a: Dict, signature_b: Dict) -> Dict:
        """
        Analyze two signatures for contradictions.

        Args:
            signature_a: First thought signature
            signature_b: Second thought signature

        Returns:
            Dictionary with contradiction analysis
        """
        prompt = f"""
You are analyzing IRRECONCILABLE ASSUMPTIONS between two reasoning agents.

SIGNATURE A (from {signature_a['agent_id']}):
Conclusion: {signature_a['conclusion']}
Confidence: {signature_a['confidence_score']}

Key reasoning:
{self._format_reasoning_chain(signature_a['reasoning_chain'][:3])}

SIGNATURE B (from {signature_b['agent_id']}):
Conclusion: {signature_b['conclusion']}
Confidence: {signature_b['confidence_score']}

Key reasoning:
{self._format_reasoning_chain(signature_b['reasoning_chain'][:3])}

CRITICAL ANALYSIS REQUIRED:
Focus on ASSUMPTION-LEVEL conflicts, not just conclusion differences.

1. What CORE ASSUMPTION does Agent A make? (e.g., "Market share creates winner-take-all dynamics")
2. What CORE ASSUMPTION does Agent B make? (e.g., "Cash flow is the only survival metric")
3. Are these assumptions LOGICALLY INCOMPATIBLE? (Can both be true simultaneously?)
4. At what specific reasoning step did their logic diverge?
5. What is the FUNDAMENTAL TRADE-OFF they disagree on?

Create a "Reasoning Collision Report" that identifies the exact logical divergence point.

Output ONLY valid JSON:
{{
  "has_contradiction": true/false,
  "contradiction_type": "conclusion|assumption|evidence|interpretation|none",
  "severity": 0.0-1.0,
  "assumption_a": "Core assumption from Agent A",
  "assumption_b": "Core assumption from Agent B",
  "logical_incompatibility": "Why these assumptions cannot both be true",
  "divergence_point": "At which reasoning step did they diverge",
  "fundamental_tradeoff": "The underlying trade-off they disagree on",
  "root_cause": "explanation of the core conflict",
  "resolution_suggestion": "how to reconcile these views",
  "conflicting_elements": [
    "specific point from A that conflicts with B"
  ]
}}
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.3  # Lower temperature for analytical tasks
                }
            )

            result = json.loads(response.text)
            result["signatures_compared"] = [
                signature_a["signature_id"],
                signature_b["signature_id"]
            ]
            return result

        except Exception as e:
            print(f"[ERROR] Contradiction detection failed: {e}")
            return {
                "has_contradiction": False,
                "contradiction_type": "error",
                "severity": 0.0,
                "root_cause": f"Detection failed: {str(e)}",
                "resolution_suggestion": "Manual review required",
                "signatures_compared": [
                    signature_a["signature_id"],
                    signature_b["signature_id"]
                ]
            }

    def detect_multi(self, signatures: List[Dict]) -> List[Dict]:
        """
        Detect contradictions across multiple signatures.

        Args:
            signatures: List of thought signatures to analyze

        Returns:
            List of contradiction analyses
        """
        contradictions = []

        # Compare each pair
        for i in range(len(signatures)):
            for j in range(i + 1, len(signatures)):
                result = self.detect(signatures[i], signatures[j])
                if result["has_contradiction"] and result["severity"] > 0.5:
                    contradictions.append(result)

        return contradictions

    def _format_reasoning_chain(self, chain: List[Dict]) -> str:
        """Format reasoning chain for display."""
        formatted = []
        for step in chain:
            formatted.append(f"  Step {step['step']}: {step['thought'][:150]}...")
        return "\n".join(formatted)
