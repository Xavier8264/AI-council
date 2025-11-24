import os
import json
import httpx
import asyncio
from typing import Callable, Dict, List, Any, Optional
from difflib import SequenceMatcher

class ModelClient:
    def __init__(self, name: str, provider: str, model: str, mode: str = "remote"):
        self.name = name
        self.provider = provider
        self.model = model
        self.mode = mode  # 'remote' or 'ollama'

    async def generate(self, prompt: str) -> str:
        if self.mode == "remote":
            return await self._generate_remote(prompt)
        elif self.mode == "ollama":
            return await self._generate_ollama(prompt)
        else:
            return f"Unsupported mode for {self.name}"

    async def _generate_remote(self, prompt: str) -> str:
        # Remote providers disabled in Ollama-only mode
        return f"Remote provider '{self.provider}' is disabled (Ollama-only mode)."

    async def _generate_ollama(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        data = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(url, json=data)
                resp.raise_for_status()
                payload = resp.json()
                return payload.get("response", "<no response>")
        except Exception as e:
            return f"Ollama Error ({self.model}): {e}"\

class ModelRegistry:
    def __init__(self, config_path: str = "models.json", ollama_only: bool = True):
        self.config_path = config_path
        self.ollama_only = ollama_only or os.getenv("OLLAMA_ONLY") == "1"
        self.models: List[ModelClient] = []
        self.load_config()

    def load_config(self) -> None:
        if not os.path.exists(self.config_path):
            # default Ollama-only config
            default = {
                "models": [
                    {"name": "Llama3 8B", "provider": "ollama", "model": "llama3:8b", "mode": "ollama"},
                    {"name": "Phi3.5 Mini", "provider": "ollama", "model": "phi3.5:mini", "mode": "ollama"},
                    {"name": "Qwen2.5 7B", "provider": "ollama", "model": "qwen2.5:7b", "mode": "ollama"}
                ]
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.models = []
        for m in data.get("models", []):
            if self.ollama_only and m.get("mode") != "ollama":
                continue
            self.models.append(
                ModelClient(
                    name=m.get("name", m.get("model")),
                    provider=m.get("provider", "unknown"),
                    model=m.get("model", "unknown"),
                    mode=m.get("mode", "remote"),
                )
            )

    async def generate_all(self, prompt: str) -> List[Dict[str, str]]:
        tasks = [self._wrap(mc, prompt) for mc in self.models]
        return await asyncio.gather(*tasks)

    async def _wrap(self, mc: ModelClient, prompt: str) -> Dict[str, str]:
        resp = await mc.generate(prompt)
        return {"model": mc.name, "response": resp}

    def list_model_names(self) -> List[str]:
        return [m.name for m in self.models]

# Consensus utilities

def responses_consensus(responses: List[str], threshold: float = 0.85) -> bool:
    if len(responses) <= 1:
        return True
    # naive pairwise similarity
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            a = normalize_text(responses[i])
            b = normalize_text(responses[j])
            ratio = SequenceMatcher(None, a, b).ratio()
            if ratio < threshold:
                return False
    return True

def normalize_text(t: str) -> str:
    return " ".join(t.lower().strip().split())

# Ollama utilities
async def list_ollama_models() -> List[str]:
    url = "http://localhost:11434/api/tags"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            return [m.get("name") for m in data.get("models", [])]
    except Exception:
        return []

DOMAIN_MODEL_MAP = {
    "code": ["deepseek-coder", "qwen2.5-coder", "llama3.1"],
    "reasoning": ["llama3.1", "qwen2.5", "gemma2"],
    "math": ["mathstral", "deepseek-math"],
    "general": ["llama3.1", "phi3.5", "qwen2.5"],
    "science": ["llama3.1", "mistral", "qwen2.5"],
}

KEYWORD_DOMAIN = {
    "python": "code",
    "javascript": "code",
    "algorithm": "code",
    "optimize": "code",
    "prove": "math",
    "integral": "math",
    "equation": "math",
    "theorem": "math",
    "reason": "reasoning",
    "strategy": "reasoning",
    "plan": "reasoning",
    "biology": "science",
    "physics": "science",
    "chemistry": "science",
}

def classify_question(question: str) -> str:
    q = question.lower()
    for kw, domain in KEYWORD_DOMAIN.items():
        if kw in q:
            return domain
    return "general"

async def recommend_ollama_models(question: str) -> Dict[str, Any]:
    installed = await list_ollama_models()
    domain = classify_question(question)
    desired = DOMAIN_MODEL_MAP.get(domain, DOMAIN_MODEL_MAP["general"])
    installed_recommended = [m for m in desired if any(inst.startswith(m) for inst in installed)]
    missing = [m for m in desired if not any(inst.startswith(m) for inst in installed)]
    return {
        "domain": domain,
        "installed_recommended": installed_recommended,
        "missing_recommendations": missing,
        "all_installed": installed,
    }
