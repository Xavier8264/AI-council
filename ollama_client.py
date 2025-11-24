"""
Ollama client for interacting with local Ollama models.
"""
import asyncio
import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Ollama default endpoint
OLLAMA_BASE_URL = "http://localhost:11434"

async def check_ollama_available() -> bool:
    """
    Check if Ollama is running and accessible.
    
    Returns:
        bool: True if Ollama is available, False otherwise
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Ollama connection failed: {e}")
        return False

async def list_available_models() -> list:
    """
    List all models available in the local Ollama instance.
    
    Returns:
        list: List of model names
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        logger.error(f"Failed to list Ollama models: {e}")
        return []

async def call_ollama(model: str, prompt: str, temperature: float = 0.7) -> str:
    """
    Call an Ollama model with a prompt.
    
    Args:
        model: Name of the Ollama model to use
        prompt: The prompt to send to the model
        temperature: Sampling temperature (0.0 to 1.0)
    
    Returns:
        str: The model's response
    """
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        # Longer timeout for model inference
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
            
    except httpx.TimeoutException:
        error_msg = f"Timeout calling Ollama model '{model}'. The model may be slow or not responding."
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            error_msg = f"Model '{model}' not found. Please pull it with: ollama pull {model}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        else:
            error_msg = f"HTTP error calling Ollama: {e}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Ollama Error for model '{model}': {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

async def verify_model_available(model: str) -> bool:
    """
    Check if a specific model is available in Ollama.
    
    Args:
        model: Name of the model to check
        
    Returns:
        bool: True if model is available, False otherwise
    """
    available_models = await list_available_models()
    # Exact match or model with version tags (e.g., "llama3.1" matches "llama3.1:latest")
    return any(m == model or m.startswith(f"{model}:") for m in available_models)

async def pull_model(model: str) -> bool:
    """
    Pull a model from Ollama library.
    
    Args:
        model: Name of the model to pull
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        url = f"{OLLAMA_BASE_URL}/api/pull"
        data = {"name": model, "stream": False}
        
        async with httpx.AsyncClient(timeout=600.0) as client:  # 10 min timeout for pull
            response = await client.post(url, json=data)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Failed to pull model '{model}': {e}")
        return False
