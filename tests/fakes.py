import json
from types import SimpleNamespace


def signature_payload(conclusion="Done", confidence=0.8):
    return {
        "reasoning_chain": [
            {"step": 1, "thought": "Reasoning", "confidence": confidence, "evidence": ["Test"]}
        ],
        "conclusion": conclusion,
        "confidence_score": confidence,
        "alternative_paths": [],
    }


class FakeGeminiClient:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.prompts = []

    def generate_content(self, prompt, generation_config=None):
        self.prompts.append(prompt)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return SimpleNamespace(text=json.dumps(response))
