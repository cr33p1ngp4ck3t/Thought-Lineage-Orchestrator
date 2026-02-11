# Deployment Guide

The Thought Lineage Orchestrator is a Flask application. Here are the recommended deployment options:

## ⚡ Quick Deploy Options

### Option 1: Render (RECOMMENDED - Easiest for Flask) 🎨

**Why Render**: Native Python/Flask support, free tier, automatic deployments.

**Steps**:
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your `Thought-Lineage-Orchestrator` repository
5. Configure:
   - **Name**: `thought-lineage-orchestrator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd src && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
   - **Environment Variables**:
     - Key: `GEMINI_API_KEY`
     - Value: Your API key
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Get your live URL: `https://thought-lineage-orchestrator.onrender.com`

**Pros**:
- ✅ Free tier
- ✅ Native Flask support
- ✅ Auto-deploy from GitHub
- ✅ Built-in environment variables
- ✅ No cold starts on free tier

---

### Option 2: Railway 🚂

**Why Railway**: Simple, generous free tier, great Python support.

**Steps**:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `Thought-Lineage-Orchestrator`
5. Railway auto-detects Python and Flask
6. Add environment variable:
   - Click "Variables" tab
   - Add `GEMINI_API_KEY` = Your API key
7. Click "Deploy"
8. Get your URL from the deployment

**Pros**:
- ✅ Very simple setup
- ✅ Auto-detects Flask
- ✅ Good free tier ($5/month credit)
- ✅ Fast deployments

---

### Option 3: PythonAnywhere (Traditional Hosting)

**Why PythonAnywhere**: Specifically designed for Python web apps.

**Steps**:
1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Click "Web" → "Add a new web app"
4. Choose "Flask" framework
5. Upload your code or clone from GitHub
6. Configure:
   - Working directory: `/home/yourusername/Thought-Lineage-Orchestrator/src`
   - WSGI configuration file: point to `app.py`
7. Add environment variable in Web tab
8. Reload web app

---

### Option 4: Heroku (Classic)

**Already configured!** You have `Procfile` and `runtime.txt`.

**Steps**:
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create thought-lineage-orchestrator`
4. Set env var: `heroku config:set GEMINI_API_KEY=your_key`
5. Deploy: `git push heroku main`
6. Open: `heroku open`

---

## 🚫 Why Vercel is Challenging

Vercel is optimized for serverless functions and Next.js, not traditional Flask apps with:
- Template rendering
- Complex file structure (agents/, intelligence/, etc.)
- Stateful orchestration

**For Vercel**, you'd need to:
- Restructure as serverless functions
- Move templates to static hosting
- Convert to stateless API

**Recommendation**: Use Render or Railway instead - they're designed for Flask.

---

## 🎯 Recommended Quick Path

**For Hackathon Judges**: Use **Render**

1. Fork/clone repo
2. Connect to Render
3. One-click deploy
4. Live in 3 minutes

**Your URL will be**: `https://thought-lineage-orchestrator.onrender.com`

---

## 🔧 Local Development

Always works perfectly:
```bash
cd src
python app.py
# Visit http://localhost:5000
```

---

## 📝 For Devpost Submission

**If deployment is taking too long:**

1. **Option A**: Submit with "Deployment in progress" note
   - Provide GitHub URL
   - Mention "Local deployment instructions in README"

2. **Option B**: Use GitHub Pages for static demo
   - Record a full demo video
   - Let judges use local setup
   - Provide clear setup instructions

3. **Option C**: Judges can use their own API keys
   - Web interface supports custom API keys
   - No deployment needed for them to test

**Judges understand**:
- Time constraints of hackathons
- API rate limits
- Deployment challenges

**What matters most**:
- ✅ Code quality (on GitHub)
- ✅ Demo video (shows it working)
- ✅ Documentation (comprehensive)
- ✅ Innovation (architecture is novel)

---

## ⚡ Quick Deploy Command (Render)

```bash
# If you use Render CLI
render deploy
```

That's it! Choose Render for the fastest deployment.
