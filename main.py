from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from debate_engine import DebateEngine
from model_registry import recommend_ollama_models, ModelRegistry

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Council - Multi-LLM Debate Platform (API-only)")

# Initialize debate engine
model_registry = ModelRegistry()
debate_engine = DebateEngine(model_registry)

class DebateRequest(BaseModel):
    question: str
    rounds: int = 2  # used if consensus == False
    consensus: bool = False
    max_rounds: int = 6  # for consensus mode
    similarity_threshold: float = 0.85

@app.get("/")
async def read_root():
    """Simple API index."""
    return {
        "name": "AI Council",
        "mode": "API-only",
        "endpoints": {
            "debate": "/api/debate",
            "recommend_models": "/api/recommend_models",
            "health": "/api/health"
        }
    }

@app.post("/api/debate")
async def create_debate(request: DebateRequest):
    """
    Run a debate between multiple LLMs.
    
    Args:
        question: The question to debate
        rounds: Number of debate rounds (default 2, max 5)
    
    Returns:
        Debate results including history and final synthesis
    """
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not request.consensus:
        if request.rounds < 1 or request.rounds > 10:
            raise HTTPException(status_code=400, detail="Rounds must be between 1 and 10")
    else:
        if request.max_rounds < 1 or request.max_rounds > 12:
            raise HTTPException(status_code=400, detail="max_rounds must be between 1 and 12")
        if not (0.5 <= request.similarity_threshold <= 0.99):
            raise HTTPException(status_code=400, detail="similarity_threshold must be between 0.5 and 0.99")
    
    # Check if at least one model is callable: remote key OR valid ollama-only configuration
    # Ollama-only: ensure at least one Ollama model is configured
    has_ollama_models = any(getattr(m, "mode", "remote") == "ollama" for m in model_registry.models)
    if not has_ollama_models:
        raise HTTPException(
            status_code=500,
            detail="No local Ollama models configured. Add entries to models.json and ensure Ollama is running."
        )
    
    try:
        if request.consensus:
            result = await debate_engine.run_until_consensus(
                request.question,
                max_rounds=request.max_rounds,
                similarity_threshold=request.similarity_threshold,
            )
        else:
            result = await debate_engine.run_debate(request.question, request.rounds)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debate failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Check API health and configuration status."""
    return {
        "status": "healthy",
        "ollama_only": True,
        "models_loaded": model_registry.list_model_names()
    }

@app.get("/api/recommend_models")
async def recommend_models(question: str = Query("", description="Question to classify for model recommendations")):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question required for recommendations")
    try:
        rec = await recommend_ollama_models(question)
        return rec
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
