# AI Council - Offline (Ollama) Debate & Consensus

A local application that orchestrates multiple local LLMs via Ollama to debate questions, iteratively refine answers, and optionally pursue unanimous consensus — no external API keys required.

## Features

- 🤖 Multi-model debate system (Ollama local models only)
- 🔄 Two modes: Fixed rounds OR consensus-seeking loop
- ⚡ Fast async API calls with httpx
- 🧩 Pluggable model registry (easy to add more models)
- 🧠 Automatic Ollama model recommendations per question domain
- 🔌 Fully offline — no external API keys

## Tech Stack

- Backend: Python 3 + FastAPI
- HTTP Client: httpx (calls local Ollama server)
- Server: Uvicorn
- Config: python-dotenv

## Quick Start (Ollama Only)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama and Pull Models
Install Ollama: https://ollama.com
Start the Ollama service, then pull a few models:
```bash
ollama pull llama3:8b
ollama pull phi3.5:mini
ollama pull qwen2.5:7b
```
No API keys are required.

### 3. Run the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

The root endpoint `/` returns a simple API index JSON.

## Project Structure

```
AI-council/
├── main.py              # FastAPI app and endpoints (API-only)
├── debate_engine.py     # Debate orchestration + consensus logic
├── model_registry.py    # Model abstraction (Ollama only) and recommendations
├── llm_clients.py       # (Legacy) remote LLM client functions (unused)
├── requirements.txt     # Python dependencies
├── models.json          # Model configuration (auto-created if missing)
└── README.md            # This file
```

## Usage

Call the API via HTTP:

```bash
curl -X POST http://localhost:8000/api/debate \
  -H "Content-Type: application/json" \
  -d '{"question":"Best way to snapshot a Postgres DB?","consensus":true,"max_rounds":6}'
```

## API Endpoints

- `GET /` - API index
- `POST /api/debate` - Run a debate
- `GET /api/health` - Check configuration status
- `GET /api/recommend_models` - Recommend Ollama models for a question

## How It Works (Debate Modes)

### Fixed-Round Debate
1. Round 1: Each model provides an initial response
2. Refinement Rounds: Each model critiques others and improves its answer
3. Synthesis: A designated synthesizer model (first local model) combines strongest points

### Consensus-Seeking Debate
Iterates until either all model responses are sufficiently similar (pairwise similarity threshold) or `max_rounds` is reached. Each round nudges models toward shared agreement while retaining accuracy.

Consensus is detected with a simple textual similarity heuristic (difflib `SequenceMatcher`). Adjustable threshold via `similarity_threshold` (default 0.85).

## Customization

### Model Configuration (`models.json`)
On first run a `models.json` file is created. Example:
```json
{
  "models": [
    {"name": "Llama3 8B", "provider": "ollama", "model": "llama3:8b", "mode": "ollama"},
    {"name": "Phi3.5 Mini", "provider": "ollama", "model": "phi3.5:mini", "mode": "ollama"},
    {"name": "Qwen2.5 7B", "provider": "ollama", "model": "qwen2.5:7b", "mode": "ollama"}
  ]
}
```
Add local Ollama models by appending entries:
```json
{"name": "Llama3 70B", "provider": "ollama", "model": "llama3:70b", "mode": "ollama"}
```

### Adding Models
Pull the model with Ollama, then add it to `models.json`.

### Ollama Integration
Ensure the Ollama service is running; the API calls to `http://localhost:11434` are used under the hood.

### Model Recommendations
Endpoint: `GET /api/recommend_models?question=...`
Returns recommended installed vs missing Ollama models based on simple domain classification of the question.

Domains & example mapping include: code (deepseek-coder), reasoning (llama3.1), math (mathstral), general (phi3.5), science (mistral).

## API Usage (Extended)

`POST /api/debate` body examples:
```json
{"question": "Explain a quicksort optimization", "rounds": 3}
```
Fixed-round mode.
```json
{"question": "Design a secure data sharing policy", "consensus": true, "max_rounds": 8, "similarity_threshold": 0.88}
```
Consensus-seeking mode.

`GET /api/recommend_models?question=integrate%20a%20polynomial`
Returns math-oriented model suggestions.

## Requirements

- Python 3.8+
- Ollama installed and running
- Pulled local models (e.g., llama3:8b, phi3.5:mini)

## Security Notes

- No external API keys are required
- All generation happens locally via your Ollama server

## Roadmap / Ideas
- Embedding-based consensus scoring for semantic agreement
- Weighted voting (assign expertise weights per domain)
- Persistent debate history & caching
- Automatic model pulling if missing (with user confirmation)

## License
MIT