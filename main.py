from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from debate_engine import DebateEngine
from model_registry import recommend_ollama_models, ModelRegistry

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Council - Multi-LLM Debate Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    """Serve the main HTML page."""
    return FileResponse("static/index.html")

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
    remote_keys_present = any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
        os.getenv("XAI_API_KEY")
    ])
    has_ollama_models = any(getattr(m, "mode", "remote") == "ollama" for m in model_registry.models)
    if not remote_keys_present and not (model_registry.ollama_only and has_ollama_models):
        raise HTTPException(
            status_code=500,
            detail="No usable models configured. Provide API keys or enable Ollama models with OLLAMA_ONLY=1 and entries in models.json."
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
        "configured_providers": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY")),
            "xai": bool(os.getenv("XAI_API_KEY"))
        },
        "models_loaded": model_registry.list_model_names(),
        "ollama_only": model_registry.ollama_only
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
