"""
Flask web application for Thought Lineage Orchestrator visualization.
"""
from flask import Flask, render_template, jsonify, request
from orchestrator import ThoughtLineageOrchestrator, ThoughtSignature
from agents import AnalyzerAgent, PlannerAgent
from intelligence import ContradictionDetector, Synthesizer
import json

app = Flask(__name__)
orchestrator = None
current_results = None


@app.route('/')
def index():
    """Main visualization page."""
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def process_problem():
    """Process a problem through the TLO system."""
    global orchestrator, current_results

    data = request.json
    problem = data.get('problem', '')
    mode = data.get('mode', 'sequential')  # sequential or parallel
    custom_api_key = data.get('api_key')  # Optional custom API key
    model = data.get('model', 'gemini-3-flash-preview')  # Optional model selection

    if not problem:
        return jsonify({"error": "Problem statement required"}), 400

    # If custom API key provided, temporarily configure it
    import google.generativeai as genai
    original_api_key = None
    original_model = None

    try:
        if custom_api_key:
            # Save original config
            from config import Config
            original_api_key = Config.GEMINI_API_KEY
            original_model = Config.GEMINI_MODEL

            # Use custom config
            Config.GEMINI_API_KEY = custom_api_key
            Config.GEMINI_MODEL = model
            genai.configure(api_key=custom_api_key)

            # Create new orchestrator with custom config
            orchestrator = ThoughtLineageOrchestrator()
        else:
            # Use default config but update model if specified
            from config import Config
            if model != Config.GEMINI_MODEL:
                original_model = Config.GEMINI_MODEL
                Config.GEMINI_MODEL = model

            orchestrator = ThoughtLineageOrchestrator()

        if mode == 'parallel':
            # Parallel mode: create conflicting plans to demonstrate contradiction detection
            results = run_parallel_demo(problem)
        else:
            # Sequential mode: standard workflow
            results = orchestrator.process_problem(problem)

        current_results = results
        return jsonify(results)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] {error_details}")
        return jsonify({"error": str(e)}), 500

    finally:
        # Restore original config if it was changed
        if original_api_key:
            from config import Config
            Config.GEMINI_API_KEY = original_api_key
            Config.GEMINI_MODEL = original_model or 'gemini-3-flash-preview'
            genai.configure(api_key=original_api_key)
        elif original_model:
            from config import Config
            Config.GEMINI_MODEL = original_model


@app.route('/api/graph')
def get_graph():
    """Get the current reasoning graph."""
    if orchestrator:
        return jsonify(orchestrator.get_graph_visualization_data())
    return jsonify({"nodes": [], "edges": []})


def run_parallel_demo(problem):
    """Run parallel planning demo with contradiction detection."""
    detector = ContradictionDetector()
    synthesizer = Synthesizer()

    # Analysis phase
    analyzer = AnalyzerAgent()
    analysis_data = analyzer.analyze(problem)
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
    orchestrator.register_signature(analysis_sig)

    # Parallel planning with COMPETING INCENTIVES
    planner_a = PlannerAgent(focus="growth")
    planner_b = PlannerAgent(focus="revenue")

    constraints_a = ["Maximize user acquisition at all costs", "Viral growth is paramount", "Ignore short-term burn rate"]
    constraints_b = ["Protect unit economics ruthlessly", "No pricing below sustainable margins", "Cash flow survival required"]

    plan_a_data = planner_a.plan(
        problem,
        analysis_signatures=[analysis_sig.to_dict()],
        constraints=constraints_a
    )
    plan_a_sig = ThoughtSignature(
        agent_id="planner-growth-focus",
        reasoning_type=plan_a_data['reasoning_type'],
        reasoning_chain=plan_a_data['reasoning_chain'],
        conclusion=plan_a_data['conclusion'],
        confidence_score=plan_a_data['confidence_score'],
        parent_signatures=[analysis_sig.signature_id],
        input_data=plan_a_data['context'].get('input_data', {}),
        constraints=constraints_a,
        alternative_paths=plan_a_data.get('alternative_paths', [])
    )
    orchestrator.register_signature(plan_a_sig)

    plan_b_data = planner_b.plan(
        problem,
        analysis_signatures=[analysis_sig.to_dict()],
        constraints=constraints_b
    )
    plan_b_sig = ThoughtSignature(
        agent_id="planner-revenue-focus",
        reasoning_type=plan_b_data['reasoning_type'],
        reasoning_chain=plan_b_data['reasoning_chain'],
        conclusion=plan_b_data['conclusion'],
        confidence_score=plan_b_data['confidence_score'],
        parent_signatures=[analysis_sig.signature_id],
        input_data=plan_b_data['context'].get('input_data', {}),
        constraints=constraints_b,
        alternative_paths=plan_b_data.get('alternative_paths', [])
    )
    orchestrator.register_signature(plan_b_sig)

    # Detect contradictions
    contradiction = detector.detect(plan_a_sig.to_dict(), plan_b_sig.to_dict())

    synthesis_sig = None
    if contradiction['has_contradiction'] and contradiction['severity'] > 0.5:
        # Synthesize resolution
        synthesis_data = synthesizer.synthesize(
            plan_a_sig.to_dict(),
            plan_b_sig.to_dict(),
            contradiction
        )
        synthesis_sig = ThoughtSignature(
            agent_id=synthesis_data['agent_id'],
            reasoning_type=synthesis_data['reasoning_type'],
            reasoning_chain=synthesis_data['reasoning_chain'],
            conclusion=synthesis_data['conclusion'],
            confidence_score=synthesis_data['confidence_score'],
            parent_signatures=synthesis_data['context'].get('parent_signatures', []),
            input_data=synthesis_data['context'].get('input_data', {}),
            constraints=synthesis_data['context'].get('constraints', []),
            alternative_paths=synthesis_data.get('alternative_paths', [])
        )
        orchestrator.register_signature(synthesis_sig)

    signatures = [analysis_sig, plan_a_sig, plan_b_sig]
    if synthesis_sig:
        signatures.append(synthesis_sig)

    return {
        "problem": problem,
        "mode": "parallel",
        "signatures": [sig.to_dict() for sig in signatures],
        "contradiction": contradiction if contradiction['has_contradiction'] else None,
        "final_conclusion": synthesis_sig.conclusion if synthesis_sig else plan_a_sig.conclusion,
        "graph": orchestrator.get_graph_visualization_data()
    }


if __name__ == '__main__':
    import os
    print("\n" + "="*80)
    print(" THOUGHT LINEAGE ORCHESTRATOR - Web Interface")
    print("="*80)
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting server on port {port}")
    print("Press Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=port, debug=False)
