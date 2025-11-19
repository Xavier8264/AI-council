# AI Council

A local web application that orchestrates multiple Large Language Models (OpenAI, Anthropic, Google Gemini, xAI Grok) to debate questions and produce synthesized answers.

## Features

- 🤖 **Multi-LLM Debate**: Orchestrate debates between different AI models
- 💬 **Multiple Rounds**: Configure debate rounds for deeper discussion
- 🎯 **Final Synthesis**: Get a synthesized answer based on all perspectives
- 🔒 **Local & Secure**: Runs locally with your own API keys
- 🌐 **Simple UI**: Clean, vanilla JavaScript interface

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **HTTP Client**: httpx
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Server**: Uvicorn
- **Configuration**: python-dotenv

## Project Structure

```
.
├── main.py              # FastAPI app and endpoints
├── debate_engine.py     # Debate orchestration logic
├── llm_clients.py       # LLM provider clients
├── static/
│   ├── index.html       # Frontend UI
│   ├── script.js        # Frontend logic
│   └── style.css        # Styling
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Xavier8264/AI-council.git
   cd AI-council
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
   GOOGLE_API_KEY=your-google-api-key-here
   XAI_API_KEY=your-xai-api-key-here
   ```

   **Note**: You need at least one API key configured to use the application.

## Usage

1. **Start the server**
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser**
   
   Navigate to: `http://localhost:8000`

3. **Start a debate**
   - Enter your question
   - Select which LLM models to include (at least one must have a configured API key)
   - Choose the number of debate rounds (1-5)
   - Click "Start Debate"
   - Wait for the models to debate and see the synthesized result

## API Endpoints

- `GET /` - Main web interface
- `GET /api/health` - Health check endpoint
- `GET /api/models` - List available models and their configuration status
- `POST /api/debate` - Start a debate (requires JSON body with question, models, and rounds)

## API Keys

### OpenAI
Get your API key from: https://platform.openai.com/api-keys

### Anthropic (Claude)
Get your API key from: https://console.anthropic.com/

### Google (Gemini)
Get your API key from: https://makersuite.google.com/app/apikey

### xAI (Grok)
Get your API key from: https://console.x.ai/

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- The `.env.example` file is provided as a template only
- All API keys are read from environment variables, never hardcoded

## Development

The application uses FastAPI's auto-reload feature during development. Any changes to Python files will automatically reload the server.

## License

MIT License - Feel free to use this project as you wish.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.