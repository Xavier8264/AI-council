from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from debate_engine import DebateEngine

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Council - Multi-LLM Debate Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize debate engine
debate_engine = DebateEngine()

class DebateRequest(BaseModel):
    question: str
    rounds: int = 2

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
    
    if request.rounds < 1 or request.rounds > 5:
        raise HTTPException(status_code=400, detail="Rounds must be between 1 and 5")
    
    # Check if at least one API key is configured
    if not any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
        os.getenv("XAI_API_KEY")
    ]):
        raise HTTPException(
            status_code=500,
            detail="No API keys configured. Please set up your .env file."
        )
    
    try:
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
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
