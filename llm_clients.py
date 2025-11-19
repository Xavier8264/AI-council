"""
LLM client functions for communicating with different AI providers.
Each function follows the same async interface: takes a prompt string and returns a response string.
"""

import os
import httpx
from typing import Optional


async def call_openai(prompt: str) -> str:
    """
    Call OpenAI's API (GPT models).
    
    Args:
        prompt: The user prompt/question to send to the model
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not set"
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling OpenAI: {str(e)}"


async def call_anthropic(prompt: str) -> str:
    """
    Call Anthropic's API (Claude models).
    
    Args:
        prompt: The user prompt/question to send to the model
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not set"
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
    except Exception as e:
        return f"Error calling Anthropic: {str(e)}"


async def call_gemini(prompt: str) -> str:
    """
    Call Google's Gemini API.
    
    Args:
        prompt: The user prompt/question to send to the model
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not set"
    
    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error calling Gemini: {str(e)}"


async def call_grok(prompt: str) -> str:
    """
    Call xAI's Grok API.
    
    Args:
        prompt: The user prompt/question to send to the model
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "Error: XAI_API_KEY not set"
    
    # xAI/Grok API endpoint (uses OpenAI-compatible format)
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-beta",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling Grok: {str(e)}"
