import json
import re
import shutil
import subprocess

import pytest

import app as app_module


@pytest.mark.skipif(shutil.which("node") is None, reason="Rendering self-check requires Node.js")
def test_template_escapes_generated_content_and_shows_synthesis_fallback():
    degraded = False
    response = app_module.app.test_client().get("/")
    html = response.get_data(as_text=True)
    script = re.search(r"<script>(.*?)</script>", html, re.DOTALL).group(1)
    payload = '<img src=x onerror="alert(1)"> & text'
    data = {
        "signatures": [
            {
                "agent_id": payload,
                "reasoning_type": 'synthesis" onclick="alert(1)',
                "conclusion": payload,
                "confidence_score": 0.8,
                "degraded": degraded,
            }
        ],
        "graph": {"nodes": [{}], "edges": []},
    }
    harness = """
        const elements = {};
        global.document = {getElementById(id) {
            return elements[id] ??= {innerHTML: '', textContent: '', classList: {add() {}}};
        }};
    """
    execution = subprocess.run(
        [shutil.which("node"), "-"],
        input=harness + script + f"\ndisplayResults({json.dumps(data)});"
        + '\nprocess.stdout.write(elements.graphContainer.innerHTML);',
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=10,
    )

    rendered = execution.stdout
    assert payload not in rendered
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt; &amp; text" in rendered
    assert '<div class="node analysis">' in rendered
