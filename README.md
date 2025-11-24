# AI Council - Offline Multi-LLM Debate Platform

An offline web application that orchestrates multiple local LLMs via Ollama to debate questions until they reach unanimous consent and produce synthesized answers.

## Features

- 🤖 Multi-model debate system using local Ollama models
- 🔄 Automatic consensus detection - debates continue until models agree
- 🎨 Clean, responsive web interface
- 🔒 Fully offline and private - no API keys or internet required
- ⚡ Fast local inference with Ollama
- 🔧 Easy model configuration and expansion

## Recommended Models

The AI Council works best with these Ollama models:

- **llama3.1** - Meta's latest Llama model, excellent for general reasoning
- **mistral** - High-performance model with strong reasoning capabilities
- **gemma2** - Google's Gemma 2, strong at analytical tasks
- **phi3** - Microsoft's Phi-3, compact but powerful
- **qwen2.5** - Alibaba's Qwen, excellent multilingual capabilities

## Tech Stack

- **Backend**: Python 3 + FastAPI
- **LLM Engine**: Ollama (local inference)
- **HTTP Client**: httpx
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Server**: Uvicorn
- **Config**: python-dotenv

## Prerequisites

### 1. Install Ollama

First, install Ollama on your system:

- **macOS/Linux**: 
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows**: Download from [ollama.com](https://ollama.com)

### 2. Start Ollama

```bash
ollama serve
```

Leave this running in a terminal. Ollama will start on `http://localhost:11434`.

### 3. Pull Recommended Models

Pull at least 2-3 models for a good debate (more models = richer perspectives):

```bash
ollama pull llama3.1
ollama pull mistral
ollama pull gemma2
ollama pull phi3
ollama pull qwen2.5
```

**Note**: Each model is several GB. Start with 2-3 models if storage is limited.

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Models (Optional)

The default configuration uses 5 recommended models. To customize:

Edit `models_config.py` and modify the `DEFAULT_COUNCIL_MODELS` list:

```python
DEFAULT_COUNCIL_MODELS = [
    "llama3.1",
    "mistral", 
    "gemma2"  # Use fewer models for faster debates
]
```

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
├── debate_engine.py     # Debate orchestration with consensus logic
├── ollama_client.py     # Ollama API client functions
├── models_config.py     # Model configuration and recommendations
├── llm_clients.py       # Legacy API clients (deprecated)
├── static/
│   ├── index.html       # Frontend HTML
│   ├── script.js        # Frontend JavaScript
│   └── style.css        # Styling
├── setup_static.py      # Helper script to create static files
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md           # This file
```

## Usage

1. Make sure Ollama is running with `ollama serve`
2. Enter your question in the text area
3. Set the maximum number of debate rounds (1-20)
4. Click "Start Debate"
5. Watch as the AI models debate and work towards consensus
6. The debate automatically stops when consensus is reached or max rounds hit

## How It Works

### Unanimous Consent Mechanism

1. **Round 1**: Each LLM provides an initial response to the question
2. **Subsequent Rounds**: Models review each other's responses, identify agreements and disagreements, and refine their positions
3. **Consensus Detection**: After each round, the system checks for consensus by looking for agreement indicators in responses
4. **Automatic Termination**: Debate stops when:
   - Consensus is reached (80%+ of models show agreement), OR
   - Maximum rounds reached (default: 10)
5. **Synthesis**: The first model generates a final answer integrating all perspectives

### Consensus Detection

The system detects consensus by analyzing responses for:
- Agreement phrases ("I agree", "I concur", "consensus", etc.)
- Alignment indicators ("as others mentioned", "building on", etc.)
- Consistent conclusions across models

When 80% or more of the models show these agreement patterns, consensus is declared.

## API Endpoints

- `GET /` - Serve the web interface
- `POST /api/debate` - Run a debate with consensus detection
- `GET /api/health` - Check Ollama status and available models
- `GET /api/models/recommended` - Get recommended model list

## Customization

### Add New Models

1. Pull the model in Ollama:
   ```bash
   ollama pull <model-name>
   ```

2. Add to `models_config.py`:
   ```python
   DEFAULT_COUNCIL_MODELS = [
       "llama3.1",
       "mistral",
       "your-new-model"  # Add here
   ]
   ```

3. (Optional) Add to recommendations:
   ```python
   RECOMMENDED_MODELS = {
       "your-new-model": {
           "name": "Your Model Name",
           "description": "Description",
           "size": "7B parameters",
           "pull_command": "ollama pull your-new-model"
       }
   }
   ```

### Adjust Consensus Settings

Edit `models_config.py`:

```python
CONSENSUS_SETTINGS = {
    "max_rounds": 10,           # Maximum debate rounds
    "similarity_threshold": 0.85,  # Similarity threshold (unused currently)
    "min_agreement_ratio": 0.8,    # Min % of models showing agreement
}
```

### Use Alternative Model Configurations

The `models_config.py` includes pre-configured alternatives:

```python
# In models_config.py, change DEFAULT_COUNCIL_MODELS to:
DEFAULT_COUNCIL_MODELS = ALTERNATIVE_CONFIGS["fast_council"]  # Smaller, faster
# or
DEFAULT_COUNCIL_MODELS = ALTERNATIVE_CONFIGS["deep_thinkers"]  # Better reasoning
# or  
DEFAULT_COUNCIL_MODELS = ALTERNATIVE_CONFIGS["minimal"]  # Just 2 models
```

### Change Debate Prompts

Edit `debate_engine.py` to modify:
- Initial round prompts
- Refinement prompts
- Consensus-seeking language
- Synthesis instructions

## Requirements

- Python 3.8+
- Ollama installed and running
- At least 2-3 models pulled in Ollama
- 8GB+ RAM recommended (depending on models used)

## Troubleshooting

### "Ollama is not running"
- Make sure Ollama is started: `ollama serve`
- Check it's accessible: `curl http://localhost:11434/api/tags`

### "No configured models are available"
- Pull the models: `ollama pull llama3.1 && ollama pull mistral`
- Check available models: `ollama list`
- Verify model names in `models_config.py` match exactly

### Models are slow
- Use smaller models (phi3, gemma2:2b)
- Reduce the number of models in `DEFAULT_COUNCIL_MODELS`
- Ensure your system has enough RAM

### Consensus never reached
- This is normal for complex/subjective questions
- The system will stop at max_rounds and synthesize available perspectives
- Try adjusting `min_agreement_ratio` in `models_config.py`

## Performance Tips

1. **Start small**: Begin with 2-3 smaller models (phi3, mistral)
2. **GPU acceleration**: Ollama automatically uses GPU if available
3. **Model selection**: Mix different model families for diverse perspectives
4. **Round limits**: Set reasonable max_rounds (5-10) to avoid long waits

## Privacy & Security

- ✅ Fully offline - no data sent to external servers
- ✅ All processing happens locally
- ✅ No API keys or accounts needed
- ✅ Your questions and debates stay on your machine

## License

MIT