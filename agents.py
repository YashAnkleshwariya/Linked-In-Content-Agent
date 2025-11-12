# agents.py
"""
Gemini-powered agents for the LinkedIn Content Crew (uses Gemini 2.5 Flash).
Requirements:
    pip install google-generativeai python-dotenv
.env must contain: GOOGLE_API_KEY=your_key_here
"""

import os
import time
import logging
from typing import Optional
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception as e:
    genai = None

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — [%(levelname)s] — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

if not GOOGLE_API_KEY:
    logger.error("❌ Missing GOOGLE_API_KEY in .env. Add it and restart.")
else:
    if genai is None:
        logger.error("❌ google-generativeai not installed. Run: pip install google-generativeai")
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("✅ Gemini client configured.")


def generate_with_gemini(
    prompt: str,
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_output_tokens: int = 256,
    retries: int = 2,
) -> str:
    """Send prompt to Gemini and return text."""
    if genai is None:
        return "❌ google-generativeai library not installed."

    model_id = model_name or MODEL_ID
    attempt = 0
    while attempt <= retries:
        try:
            t0 = time.time()
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(prompt)
            latency = time.time() - t0
            text = getattr(response, "text", str(response))
            preview = text[:180].replace("\n", " ")
            logger.info(f"✅ Gemini responded in {latency:.2f}s — Preview: {preview}...")
            return text.strip()
        except Exception as e:
            attempt += 1
            logger.warning(f"⚠️ Attempt {attempt}/{retries} failed: {e}")
            time.sleep(1.5)

    logger.error("❌ All Gemini retries failed.")
    return "❌ Generation error after multiple attempts."


# --- Agent classes ---
class StrategistAgent:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_ID

    def generate(self, prompt: str, temperature: float = 0.6, max_tokens: int = 300):
        return generate_with_gemini(prompt, self.model_name, temperature, max_tokens)


class WriterAgent:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_ID

    def generate(self, prompt: str, temperature: float = 0.85, max_tokens: int = 400):
        return generate_with_gemini(prompt, self.model_name, temperature, max_tokens)


class EditorAgent:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_ID

    def generate(self, prompt: str, temperature: float = 0.5, max_tokens: int = 320):
        return generate_with_gemini(prompt, self.model_name, temperature, max_tokens)


# Instantiate agents
strategist_agent = StrategistAgent()
writer_agent = WriterAgent()
editor_agent = EditorAgent()
