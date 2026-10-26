# Thought Lineage Orchestrator (TLO)

**A Marathon Agent system that coordinates AI-to-AI reasoning and detects contradictions using Gemini 3**

🏆 **Built for the Gemini 3 Global Hackathon**

## The Innovation

As AI agents proliferate, we face a coming coordination crisis: multiple autonomous agents making interdependent decisions without a coherent oversight layer. The Thought Lineage Orchestrator solves this by creating **traceable reasoning lineages** that persist across agent interactions.

When Agent A makes a decision, its reasoning becomes verifiable input for Agent B, creating transparent chains of logic that can be audited, debugged, and optimized in real-time.

## Why This Matters (Future-Ready)

This project doesn't solve today's problems better—it solves **tomorrow's problems** that don't exist yet:

- **AI-to-AI Coordination**: As organizations deploy multiple specialized agents, maintaining coherence becomes critical
- **Reasoning Auditability**: Understanding *why* AI systems made decisions is essential for trust and compliance
- **Contradiction Detection**: When agents disagree, we need intelligent arbitration that understands cognitive models
- **Hybrid Solution Synthesis**: Instead of choosing one agent's recommendation, TLO can synthesize optimal hybrid approaches

## Key Features

### 0. Competing Incentives (Domain Bias)
Agents are programmed with **narrow domain optimization**:
- Growth-focused planner: 100% user acquisition, ignores burn rate
- Revenue-focused planner: 100% margin protection, blocks low pricing
- This creates genuine reasoning conflicts (not artificial disagreement)

### 1. Thought Signatures
Every agent interaction creates a structured "thought signature" containing:
- Step-by-step reasoning chain with confidence scores
- Evidence and justifications
- Alternative paths considered
- Parent-child dependencies

### 2. Multi-Agent Coordination
Three specialized agents work in concert:
- **Analyzer Agent**: Breaks down complex problems
- **Planner Agent**: Creates strategic action sequences
- **Executor Agent**: Transforms plans into concrete steps

### 3. Contradiction Detection (The "Wow" Factor)
Using Gemini 3's deep reasoning capabilities, TLO:
- **Analyzes assumption-level incompatibility** (not just conclusion differences)
- Identifies irreconcilable core beliefs between agents
- Extracts the fundamental trade-off they disagree on
- Pinpoints exact divergence point in reasoning chains
- Measures severity and creates "Reasoning Collision Report"

### 4. Intelligent Synthesis (Chief Justice Mode)
When contradictions are detected, TLO acts as a Chief Justice:
- **Arbitration Log**: Documents which assumptions were deprioritized and why
- **Hybrid Assumption Creation**: Generates new unified assumptions
- **Confidence Justification**: Mathematical reasoning for confidence scores
- **Risk Resolution**: Addresses specific concerns from both reasoning paths
- Synthesizes solutions that achieve BOTH conflicting objectives

### 5. Reasoning Graph Visualization
Real-time visual representation of:
- Reasoning flow across agents
- Confidence levels (color-coded)
- Dependency relationships
- Contradiction alerts

## Technical Architecture

```
User Problem
    ↓
[Orchestrator]
    ↓
[Analyzer Agent] → Thought Signature A
    ↓
[Planner Agent] → Thought Signature B (depends on A)
    ↓
[Executor Agent] → Thought Signature C (depends on B)
    ↓
[Contradiction Detector] → Analyzes signature pairs
    ↓
[Synthesizer] → Creates hybrid solution
    ↓
Final Coherent Output + Full Reasoning Lineage
```

## Gemini 3 Integration

This project heavily leverages Gemini 3's advanced capabilities:

1. **Structured Output Generation**: Thought signatures use JSON schema responses
2. **Deep Reasoning**: Multi-step analysis with confidence calibration
3. **Meta-Cognitive Analysis**: Understanding *why* reasoning paths diverge
4. **Synthesis**: Creating novel hybrid solutions from conflicting inputs
5. **Low Latency**: Real-time coordination across multiple agent calls

### API Usage Example

```python
from orchestrator import ThoughtLineageOrchestrator

orchestrator = ThoughtLineageOrchestrator()

result = orchestrator.process_problem(
    problem="Choose pricing strategy for our AI tool",
    constraints=["Budget: $100K", "Timeline: 3 months"]
)

# Access reasoning graph
graph = orchestrator.get_graph_visualization_data()

# Export lineage for audit
orchestrator.save_graph("reasoning_lineage.json")
```

## Installation & Setup

```bash
# Python 3.13
python -m venv .venv

# Windows
.venv/Scripts/python -m pip install -r requirements-lock.txt

# macOS/Linux
.venv/bin/python -m pip install -r requirements-lock.txt

# Set up environment
cp .env.example .env
# Edit .env and add your Gemini API key

# Run web interface from the repository root
.venv/Scripts/python src/app.py

# Visit http://localhost:5000
```

On macOS or Linux, replace `.venv/Scripts/python` with `.venv/bin/python`.

The service exposes `GET /health` for liveness. Each `POST /api/process` response contains its own graph; the former shared `GET /api/graph` endpoint now returns `410` to prevent one request from exposing another request's results.

### Tests and lint

Tests use fake Gemini responses and run without an API key or network access.

```bash
.venv/Scripts/python -m pip install -r requirements-lock.txt -r requirements-dev-lock.txt
.venv/Scripts/python -m ruff check src tests
.venv/Scripts/python -m pytest tests -v
```

Use `.venv/bin/python` on macOS or Linux. See `CONTRIBUTING.md` for lockfile maintenance.

### Docker

```bash
docker build -t thought-lineage-orchestrator .
docker run --rm -p 5000:5000 -e GEMINI_API_KEY=your_key thought-lineage-orchestrator
```

## Demo Scenarios

### Scenario 1: Parallel Planning with Contradiction
**Problem**: "Choose pricing strategy for our AI tool"

**Two planners with different priorities**:
- Planner A: Maximize market penetration (freemium model)
- Planner B: Maximize revenue (premium positioning)

**Result**: TLO detects the contradiction (severity: 0.65) and synthesizes a "Dual-Track Monetization Framework" that achieves both goals through market segmentation.

### Scenario 2: Sequential Reasoning
**Problem**: "Plan a product launch for a new AI tool"

**Agent Flow**:
1. Analyzer: Breaks down timing, resources, and competitive factors
2. Planner: Creates 90-day phased launch strategy
3. Executor: Defines concrete budget allocation and milestones

**Result**: Coherent end-to-end plan with full reasoning audit trail.

## Project Structure

```
gem-devpost/
├── src/
│   ├── agents/
│   │   ├── base_agent.py      # Base agent class
│   │   ├── analyzer.py         # Problem decomposition
│   │   ├── planner.py          # Strategic planning
│   │   └── executor.py         # Execution planning
│   ├── intelligence/
│   │   ├── contradiction_detector.py  # Conflict detection
│   │   └── synthesizer.py             # Hybrid solution creation
│   ├── orchestrator.py         # Core TLO system
│   ├── config.py              # Configuration
│   ├── app.py                 # Flask web interface
│   └── templates/
│       └── index.html         # Visualization UI
├── requirements.txt
└── README.md
```

## Judging Criteria Alignment

### Technical Execution (40%)
- ✅ Deep Gemini 3 API integration across multiple agents
- ✅ Complex graph algorithms for reasoning lineage
- ✅ Real-time contradiction detection
- ✅ Structured JSON schema responses
- ✅ Modular, extensible architecture

### Innovation / Wow Factor (30%)
- ✅ Novel approach: coordinates *reasoning*, not just execution
- ✅ Solves future problem of AI-AI coordination
- ✅ Demonstrates meta-cognitive capabilities
- ✅ Visual contradiction detection and resolution

### Potential Impact (20%)
- ✅ Essential infrastructure as agents proliferate
- ✅ Enables trustworthy multi-agent systems
- ✅ Applicable to enterprise AI deployments
- ✅ Reasoning auditability for compliance

### Presentation / Demo (10%)
- ✅ Clear problem definition
- ✅ Compelling visual demonstration
- ✅ Well-documented architecture
- ✅ Easy to understand and reproduce

## Future Enhancements

1. **Reasoning Evolution Engine**: Analyze success patterns and evolve decision strategies
2. **Multi-Turn Interactions**: Support conversational reasoning across sessions
3. **External Tool Integration**: Allow agents to call APIs and use tools
4. **Reasoning Replay**: Step-through debugging of decision chains
5. **Confidence Calibration**: Learn from outcomes to improve confidence scoring

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with:
- **Gemini 3 API** for advanced reasoning capabilities
- **Flask** for web interface
- **Python 3.13** for core logic

---

**Built for Gemini 3 Global Hackathon | February 2026**

*Solving tomorrow's AI coordination challenges today*
