import requests
import json
from config.settings import OLLAMA_URL, OLLAMA_MODEL
from config.prompts import SYSTEM_PROMPT
from tools.logger import agent_logger

class OllamaClient:
    """Handles communications with local Ollama daemon infrastructure."""
    
    def __init__(self):
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL

    def generate(self, user_prompt: str) -> str:
        """Sends concatenated context to local LLM and strips control text."""
        payload = {
            "model": self.model,
            "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}\nOutput:",
            "stream": False
        }
        try:
            agent_logger.info(f"Dispatching query to Ollama ({self.model})...")
            response = requests.post(self.url, json=payload, timeout=30)
            response.raise_for_status()
            raw_response = response.json().get("response", "").strip()
            return raw_response
        except Exception as e:
            agent_logger.error(f"Ollama connection dropped/failed: {str(e)}")
            raise ConnectionError(f"Could not interact with local LLM context: {str(e)}")