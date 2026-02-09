# Quick Start Guide

Get the Thought Lineage Orchestrator running in 5 minutes.

## Prerequisites

- Python 3.10+ installed
- Gemini API key (get from https://aistudio.google.com/apikey)
- Git (optional, for cloning)

## Installation

### Step 1: Clone or Download
```bash
git clone https://github.com/[your-username]/gem-devpost.git
cd gem-devpost
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

## Usage

### Option 1: Web Interface (Recommended)
```bash
cd src
python app.py
```

Then open your browser to `http://localhost:5000`

**Try the demo**:
1. Problem is pre-filled: "Choose the pricing strategy for our AI tool"
2. Mode: Select "Parallel (Demonstrate contradiction detection)"
3. Click "Process Problem"
4. Watch the multi-agent reasoning unfold with contradiction detection!

### Option 2: Command Line Tests

**Test 1: Basic System Check**
```bash
cd src
python orchestrator.py
```
Expected output: API connection successful, test signature created

**Test 2: Multi-Agent Coordination**
```bash
cd src
python test_agents.py
```
Expected output: 3 agents process a product launch problem

**Test 3: Contradiction Detection (The Wow Factor!)**
```bash
cd src
python test_contradiction.py
```
Expected output: Parallel planners create conflicting strategies, system detects contradiction and synthesizes hybrid solution

## Understanding the Output

### Thought Signature
Each agent produces a structured signature:
- **Agent ID**: Which agent generated this
- **Reasoning Chain**: Step-by-step thought process
- **Conclusion**: Final recommendation
- **Confidence Score**: 0.0-1.0 (how confident the agent is)
- **Alternative Paths**: Other approaches considered

### Contradiction Detection
When agents disagree:
- **Type**: assumption | conclusion | evidence | interpretation
- **Severity**: 0.0-1.0 (how serious the conflict is)
- **Root Cause**: Why the agents diverged
- **Resolution**: How to reconcile the views

### Synthesis
The "wow" moment:
- Combines strengths of both conflicting paths
- Often has HIGHER confidence than either individual agent
- Explains why the hybrid is superior

## Troubleshooting

### "API key not found"
- Make sure `.env` file exists in project root
- Check that `GEMINI_API_KEY` is set correctly
- No quotes needed around the API key

### "Model not found"
- We use `gemini-3-flash-preview`
- This should be available in the API
- Check your API access at https://aistudio.google.com

### "Port 5000 already in use"
- Another app is using port 5000
- Edit `src/app.py` and change `app.run(debug=True, port=5000)` to another port like 5001

### Unicode errors on Windows
- These have been fixed (emojis removed from output)
- If you see encoding errors, check Python console encoding

## Next Steps

1. **Try your own problems**: Edit the problem statement in the web interface
2. **Explore the code**: Start with `src/orchestrator.py`
3. **Check the reasoning graph**: After running, look at generated `.json` files
4. **Read the architecture**: See README.md for detailed technical docs

## Questions?

- Check README.md for full documentation
- Review code comments for implementation details
- Open an issue on GitHub if you encounter problems

**Enjoy exploring AI-to-AI reasoning coordination!**
