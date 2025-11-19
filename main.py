"""
FastAPI application for AI Council debate orchestration.
"""

import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from debate_engine import DebateEngine

# Load environment variables from .env file
load_dotenv()

# Verify API keys are set (optional warning)
required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "XAI_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
    print("Some models may not work. Please set them in your .env file.")

# Initialize FastAPI app
app = FastAPI(
    title="AI Council Debate",
    description="Orchestrate multiple LLMs to debate questions and produce final answers",
    version="1.0.0"
)

# Initialize debate engine
debate_engine = DebateEngine()


# Request/Response models
class DebateRequest(BaseModel):
    """Request model for starting a debate."""
    question: str
    models: List[str]
    rounds: Optional[int] = 2


class DebateResponse(BaseModel):
    """Response model for debate results."""
    question: str
    debate_history: List[dict]
    final_answer: str


# API Endpoints
@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


@app.get("/api/models")
async def get_available_models():
    """
    Get list of available AI models.
    
    Returns:
        List of model names that can participate in debates
    """
    return {
        "models": list(debate_engine.models.keys())
    }


@app.post("/api/debate")
async def start_debate(request: DebateRequest):
    """
    Start a debate between selected models.
    
    Args:
        request: DebateRequest containing question, models, and rounds
        
    Returns:
        Debate results including history and final answer
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not request.models:
        raise HTTPException(status_code=400, detail="At least one model must be selected")
    
    if request.rounds < 1 or request.rounds > 5:
        raise HTTPException(status_code=400, detail="Rounds must be between 1 and 5")
    
    # Run the debate
    result = await debate_engine.run_debate(
        question=request.question,
        selected_models=request.models,
        rounds=request.rounds
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status of the service
    """
    return {
        "status": "healthy",
        "service": "AI Council Debate"
    }


# Mount static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
