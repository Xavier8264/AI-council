# AI Council - Multi-LLM Debate Platform

A local web application that orchestrates multiple LLMs (OpenAI, Anthropic, Google, xAI) to debate questions and produce synthesized answers.

## Features

- 🤖 Multi-model debate system (GPT-4, Claude, Gemini, Grok)
- 🔄 Configurable debate rounds
- 🎨 Clean, responsive web interface
- 🔒 Secure local execution with API keys in .env
- ⚡ Fast async API calls with httpx

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **HTTP Client**: httpx
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Server**: Uvicorn
- **Config**: python-dotenv

## Quick Start

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

## How It Works

1. **Round 1**: Each LLM provides an initial response to the question
2. **Additional Rounds**: Models review each other's responses, critique weaknesses, and refine their answers
3. **Synthesis**: Claude generates a final answer integrating the best points from all perspectives

## Customization

### Change Models

Edit `llm_clients.py` to modify which specific models are used:
- OpenAI: Currently using `gpt-4o-mini` (line 17)
- Anthropic: Currently using `claude-3-5-sonnet-20241022` (line 44)
- Google: Currently using `gemini-1.5-flash` (line 70)
- xAI: Currently using `grok-beta` (line 96)

### Adjust Debate Logic

Edit `debate_engine.py` to:
- Modify prompts
- Change debate flow
- Add additional rounds or synthesis steps

## Requirements

- Python 3.8+
- Active API keys for at least one LLM provider
- Internet connection for API calls

## Security Notes

- Never commit your `.env` file
- API keys are loaded from environment variables only
- All API calls are made from the backend (keys never exposed to frontend)

## License

MIT