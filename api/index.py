"""
Vercel serverless function entry point.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

# Vercel expects 'app' to be the Flask application
# This is the handler that Vercel will use
