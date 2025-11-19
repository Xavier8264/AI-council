# Quick Start Guide

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd AI-council
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API keys
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

## Getting API Keys

### OpenAI (GPT-4)
- Visit: https://platform.openai.com/api-keys
- Sign up/login and create a new API key
- Add to `.env`: `OPENAI_API_KEY=sk-...`

### Anthropic (Claude)
- Visit: https://console.anthropic.com/settings/keys
- Sign up/login and create a new API key
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### Google (Gemini)
- Visit: https://makersuite.google.com/app/apikey
- Create a new API key
- Add to `.env`: `GOOGLE_API_KEY=AIza...`

### xAI (Grok)
- Visit: https://x.ai/api
- Sign up for API access
- Add to `.env`: `XAI_API_KEY=xai-...`

## Usage Example

1. Enter a question like: "What are the ethical implications of artificial general intelligence?"
2. Select at least one AI model (you can select all 4)
3. Choose the number of debate rounds (2-3 recommended)
4. Click "Start Debate"
5. Wait for the models to debate (this may take 1-2 minutes)
6. Review the debate history and final synthesized answer

## API Usage

You can also use the API directly:

```bash
curl -X POST http://localhost:8000/api/debate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should we pursue nuclear fusion energy?",
    "models": ["OpenAI (GPT-4)", "Anthropic (Claude)", "Google (Gemini)"],
    "rounds": 2
  }'
```

## Troubleshooting

**Error: API key not set**
- Make sure you created `.env` and added the API keys
- Check that the key names match exactly (e.g., `OPENAI_API_KEY`)

**Error: Module not found**
- Run `pip install -r requirements.txt` again
- Make sure you're in the correct directory

**Port 8000 already in use**
- Change the port in `main.py` (line at bottom)
- Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

**Models timing out**
- Some API calls can take 30-60 seconds
- Make sure you have a stable internet connection
- Check that your API keys have sufficient credits/quota

## Tips

- Start with 2 models and 1-2 rounds to test
- More rounds = longer wait time but potentially better synthesis
- Each model may have different response styles and perspectives
- The final answer synthesizes insights from all participants
