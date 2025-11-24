from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from debate_engine import DebateEngine
from ollama_client import check_ollama_available, list_available_models, verify_model_available
from models_config import get_active_models, RECOMMENDED_MODELS, get_model_display_name
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Council - Ollama Multi-LLM Debate Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize debate engine
debate_engine = DebateEngine()

class DebateRequest(BaseModel):
    question: str
    max_rounds: int = 10

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")

@app.post("/api/debate")
async def create_debate(request: DebateRequest):
    """
    Run a debate between multiple Ollama LLMs until consensus is reached.
    
    Args:
        question: The question to debate
        max_rounds: Maximum number of debate rounds (default 10)
    
    Returns:
        Debate results including history, consensus status, and final synthesis
    """
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if request.max_rounds < 1 or request.max_rounds > 20:
        raise HTTPException(status_code=400, detail="Max rounds must be between 1 and 20")
    
    # Check if Ollama is available
    if not await check_ollama_available():
        raise HTTPException(
            status_code=500,
            detail="Ollama is not running. Please start Ollama with: ollama serve"
        )
    
    # Verify at least some configured models are available
    active_models = get_active_models()
    available_count = 0
    for model in active_models:
        if await verify_model_available(model):
            available_count += 1
    
    if available_count == 0:
        model_list = ", ".join(active_models)
        raise HTTPException(
            status_code=500,
            detail=f"No configured models are available in Ollama. Please pull models: {model_list}"
        )
    
    try:
        result = await debate_engine.run_debate(request.question, request.max_rounds)
        return result
    except Exception as e:
        logger.error(f"Debate failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Debate failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Check API health and Ollama configuration status."""
    ollama_available = await check_ollama_available()
    
    if not ollama_available:
        return {
            "status": "error",
            "ollama_running": False,
            "message": "Ollama is not running. Please start with: ollama serve"
        }
    
    available_models = await list_available_models()
    configured_models = get_active_models()
    
    # Check which configured models are available
    model_status = {}
    for model_id in configured_models:
        is_available = any(m.startswith(model_id) or model_id in m for m in available_models)
        model_status[get_model_display_name(model_id)] = is_available
    
    ready_count = sum(1 for v in model_status.values() if v)
    
    return {
        "status": "healthy" if ready_count > 0 else "warning",
        "ollama_running": True,
        "configured_models": model_status,
        "ready_models": ready_count,
        "total_configured": len(configured_models),
        "all_available_models": available_models
    }

@app.get("/api/models/recommended")
async def get_recommended_models():
    """Get list of recommended Ollama models for the AI Council."""
    return {
        "recommended_models": RECOMMENDED_MODELS,
        "active_models": get_active_models()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
