# AI Council - Multi-LLM Debate & Consensus Platform

A local application that orchestrates multiple LLMs (remote APIs and optional local Ollama models) to debate questions, iteratively refine answers, and optionally pursue unanimous consensus.

## Features

- 🤖 Multi-model debate system (GPT-4, Claude, Gemini, Grok + Ollama models)
- 🔄 Two modes: Fixed rounds OR consensus-seeking loop
- 🎨 Clean, responsive web interface
- 🔒 Secure local execution with API keys in .env
- ⚡ Fast async API calls with httpx
- 🧩 Pluggable model registry (easy to add more providers)
- 🏠 Optional offline / local-only mode via `OLLAMA_ONLY=1`
- 🧠 Automatic Ollama model recommendations per question domain

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **HTTP Client**: httpx
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Server**: Uvicorn
- **Config**: python-dotenv

## Quick Start (Remote API Models)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_actual_openai_key
ANTHROPIC_API_KEY=your_actual_anthropic_key
GOOGLE_API_KEY=your_actual_google_key
XAI_API_KEY=your_actual_xai_key
```

**Note**: You need at least one API key configured for the app to work.

### 3. Create Static Files

Run the setup script to create the frontend files:

```bash
python setup_static.py
```

This creates the `static/` directory with:
- `index.html` - Main web interface
- `script.js` - Frontend logic
- `style.css` - Styling

### 4. Run the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

### 5. Open in Browser

Navigate to: http://localhost:8000

## Project Structure

```
AI-council/
├── main.py              # FastAPI app and endpoints
├── debate_engine.py     # Debate orchestration logic
├── llm_clients.py       # LLM API client functions
├── static/
│   ├── index.html       # Frontend HTML
│   ├── script.js        # Frontend JavaScript
│   └── style.css        # Styling
├── setup_static.py      # Helper script to create static files
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .env                 # Your actual API keys (gitignored)
└── README.md           # This file
```

## Usage

1. Enter your question in the text area
2. Select the number of debate rounds (1-5)
3. Click "Start Debate"
4. Watch as the AI models debate and synthesize a final answer

## API Endpoints

- `GET /` - Serve the web interface
- `POST /api/debate` - Run a debate
- `GET /api/health` - Check configuration status

## How It Works (Debate Modes)

### Fixed-Round Debate
1. **Round 1**: Each model provides an initial response
2. **Refinement Rounds**: Each model critiques others and improves its answer
3. **Synthesis**: A designated synthesizer model (Claude if available, else first model) combines strongest points

### Consensus-Seeking Debate
Iterates until either all model responses are sufficiently similar (pairwise similarity threshold) or `max_rounds` is reached. Each round nudges models toward shared agreement while retaining accuracy.

Consensus is detected with a simple textual similarity heuristic (difflib `SequenceMatcher`). Adjustable threshold via `similarity_threshold` (default 0.85).

## Customization

### Model Configuration (`models.json`)
On first run a `models.json` file is created. Example:
```json
{
	"models": [
		{"name": "OpenAI GPT-4o Mini", "provider": "openai", "model": "gpt-4o-mini", "mode": "remote"},
		{"name": "Anthropic Claude 3.5 Sonnet", "provider": "anthropic", "model": "claude-3-5-sonnet-20241022", "mode": "remote"},
		{"name": "Google Gemini 1.5 Flash", "provider": "google", "model": "gemini-1.5-flash", "mode": "remote"},
		{"name": "xAI Grok Beta", "provider": "xai", "model": "grok-beta", "mode": "remote"}
	]
}
```
Add local Ollama models by appending entries:
```json
{"name": "Llama3 8B", "provider": "ollama", "model": "llama3:8b", "mode": "ollama"}
```

Set `OLLAMA_ONLY=1` in `.env` to restrict the council to local models only (offline mode).

### Adding New Providers
Implement a new async function in `llm_clients.py` then add its metadata to `models.json`.

### Adjust Debate & Consensus Logic
See `debate_engine.py`:
- Modify prompt wording
- Tweak consensus similarity threshold (API param)
- Change synthesis strategy

### Ollama Integration
Install Ollama (https://ollama.com) and pull desired models, e.g.:
```bash
ollama pull llama3:8b
ollama pull phi3.5:mini
```
Then add them to `models.json` as shown above.

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
- Optional: Remote API keys (OpenAI, Anthropic, Google, xAI)
- Optional: Ollama installed for local models
- Internet connection (unless using `OLLAMA_ONLY=1` + local models)

## Security Notes

- Never commit your `.env` file
- API keys are loaded from environment variables only
- All API calls are made from the backend (keys never exposed to frontend)

## Roadmap / Ideas
- Embedding-based consensus scoring for semantic agreement
- Weighted voting (assign expertise weights per domain)
- Persistent debate history & caching
- Automatic model pulling if missing (with user confirmation)

## License
MIT