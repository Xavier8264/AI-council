"""
LLM Client implementations for different providers.
Each function takes a prompt and returns the model's response as a string.
"""

import os
import httpx
from typing import Optional


async def call_openai(prompt: str) -> str:
    """
    Call OpenAI's GPT model using their API.
    
    Args:
        prompt: The user's prompt/question
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not configured"
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"OpenAI API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"OpenAI Error: {str(e)}"


async def call_anthropic(prompt: str) -> str:
    """
    Call Anthropic's Claude model using their API.
    
    Args:
        prompt: The user's prompt/question
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not configured"
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
    except httpx.HTTPStatusError as e:
        return f"Anthropic API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Anthropic Error: {str(e)}"


async def call_gemini(prompt: str) -> str:
    """
    Call Google's Gemini model using their API.
    
    Args:
        prompt: The user's prompt/question
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not configured"
    
    # Using Gemini 1.5 Flash model
    model = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except httpx.HTTPStatusError as e:
        return f"Gemini API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Gemini Error: {str(e)}"


async def call_grok(prompt: str) -> str:
    """
    Call xAI's Grok model using their API.
    
    Args:
        prompt: The user's prompt/question
        
    Returns:
        The model's response as a string
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "Error: XAI_API_KEY not configured"
    
    # xAI uses OpenAI-compatible API
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "grok-beta",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"Grok API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Grok Error: {str(e)}"
