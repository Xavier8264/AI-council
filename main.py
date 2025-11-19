"""
Main FastAPI application for AI Council debate orchestration.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from debate_engine import DebateEngine

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI Council",
    description="Orchestrate multiple LLMs in a debate format",
    version="1.0.0"
)

# Initialize debate engine
debate_engine = DebateEngine()

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


class DebateRequest(BaseModel):
    """Request model for starting a debate."""
    question: str
    models: List[str]
    rounds: int = 2


class DebateResponse(BaseModel):
    """Response model for debate results."""
    question: str
    debate_history: List[dict]
    final_answer: str


@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    static_path = os.path.join(static_dir, "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return {"message": "AI Council API - Visit /docs for API documentation"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "AI Council is running"
    }


@app.get("/api/models")
async def get_available_models():
    """
    Get list of available LLM models.
    
    Returns:
        List of model names and their configuration status
    """
    models = [
        {
            "name": "openai",
            "display_name": "OpenAI GPT-3.5",
            "configured": bool(os.getenv("OPENAI_API_KEY"))
        },
        {
            "name": "anthropic",
            "display_name": "Anthropic Claude",
            "configured": bool(os.getenv("ANTHROPIC_API_KEY"))
        },
        {
            "name": "gemini",
            "display_name": "Google Gemini",
            "configured": bool(os.getenv("GOOGLE_API_KEY"))
        },
        {
            "name": "grok",
            "display_name": "xAI Grok",
            "configured": bool(os.getenv("XAI_API_KEY"))
        }
    ]
    
    return {"models": models}


@app.post("/api/debate")
async def start_debate(request: DebateRequest):
    """
    Start a debate with selected models.
    
    Args:
        request: DebateRequest with question, models, and rounds
        
    Returns:
        DebateResponse with debate history and final answer
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not request.models or len(request.models) == 0:
        raise HTTPException(status_code=400, detail="At least one model must be selected")
    
    if request.rounds < 1 or request.rounds > 5:
        raise HTTPException(status_code=400, detail="Rounds must be between 1 and 5")
    
    try:
        result = await debate_engine.run_debate(
            question=request.question,
            selected_models=request.models,
            rounds=request.rounds
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running debate: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
