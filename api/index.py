"""
Vercel serverless entrypoint. Vercel's Python runtime looks for a WSGI
callable named `app` in this file (see vercel.json rewrite rule).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402  (Flask app instance, reused as-is)
