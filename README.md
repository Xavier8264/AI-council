# AI Council Debate 🤖

A LOCAL web application that orchestrates multiple LLMs (OpenAI, Anthropic, Google, xAI) to debate questions and produce synthesized answers.

## Features

- 🎯 Multi-LLM debate orchestration
- 🔄 Configurable debate rounds
- 🎨 Clean, responsive web interface
- 🔐 Secure API key management via environment variables
- ⚡ Async/await for efficient concurrent API calls

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **HTTP Client**: httpx
- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks)
- **Server**: uvicorn
- **Config**: python-dotenv for environment variable management

## Project Structure

```
AI-council/
├── main.py              # FastAPI application and endpoints
├── debate_engine.py     # Debate orchestration logic
├── llm_clients.py       # LLM provider API clients
├── static/
│   ├── index.html      # Web interface
│   ├── script.js       # Frontend logic
│   └── style.css       # Styling
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-council
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
XAI_API_KEY=xai-...
```

**Note**: You need at least one API key to use the application. Models without API keys will show error messages.

### 4. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

### 5. Access the Web Interface

Open your browser and navigate to:

```
http://localhost:8000
```

## Usage

1. **Enter a Question**: Type your question in the text area
2. **Select AI Models**: Choose which LLMs should participate in the debate
3. **Choose Rounds**: Select the number of debate rounds (1-5)
4. **Start Debate**: Click the button to begin

The application will:
- Send your question to all selected models
- Collect their initial responses
- Share responses between models for subsequent rounds
- Generate a final synthesized answer

## API Endpoints

- `GET /` - Serve the web interface
- `GET /api/models` - Get list of available AI models
- `POST /api/debate` - Start a debate with selected models
- `GET /api/health` - Health check endpoint

## API Request Example

```bash
curl -X POST http://localhost:8000/api/debate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the meaning of life?",
    "models": ["OpenAI (GPT-4)", "Anthropic (Claude)"],
    "rounds": 2
  }'
```

## Security

- ✅ No API keys in source code
- ✅ Environment variables for all sensitive data
- ✅ `.env` excluded from version control
- ✅ Input validation on all endpoints
- ✅ HTML escaping to prevent XSS

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Individual LLM Clients

```python
import asyncio
from llm_clients import call_openai

async def test():
    response = await call_openai("What is 2+2?")
    print(response)

asyncio.run(test())
```

## Troubleshooting

**Models not responding**: Check that your API keys are correctly set in `.env`

**Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Port already in use**: Change the port in `main.py` or when running uvicorn

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.