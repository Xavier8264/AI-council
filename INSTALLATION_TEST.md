# Quick Installation Test Guide

This guide is for testing the AI Council installation process.

## Prerequisites Check

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Ollama installed**
   - macOS/Linux: `curl -fsSL https://ollama.com/install.sh | sh`
   - Windows: Download from https://ollama.com
   - Verify: `ollama --version`

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Pull Ollama Models

Pull at least 2 models (more is better):

```bash
# Recommended starter set (choose 2-3):
ollama pull llama3.1      # ~5GB
ollama pull mistral       # ~4GB
ollama pull phi3          # ~2GB (lightweight option)

# Full recommended set:
ollama pull llama3.1
ollama pull mistral
ollama pull gemma2
ollama pull phi3
ollama pull qwen2.5
```

Verify models are available:
```bash
ollama list
```

### 3. Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal.

### 4. Generate Static Files

```bash
python setup_static.py
```

This creates the `static/` directory with HTML, CSS, and JavaScript files.

### 5. Start the AI Council

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

### 6. Open in Browser

Navigate to: http://localhost:8000

## Troubleshooting

### "Ollama is not running"
- Make sure `ollama serve` is running in another terminal
- Check: `curl http://localhost:11434/api/tags`

### "No configured models are available"
- Pull models: `ollama pull llama3.1`
- Verify: `ollama list`
- Check model names in `models_config.py` match your pulled models

### Models are slow
- Use smaller models (phi3, gemma2:2b)
- Reduce number of models in `models_config.py`
- Ensure GPU is being used (Ollama does this automatically if available)

### Port 8000 already in use
- Change port in main.py or use: `uvicorn main:app --port 8001`

## Testing the Debate Feature

1. Enter a simple question: "What is the best programming language for beginners?"
2. Set max rounds to 3-5
3. Click "Start Debate"
4. Watch the models debate until consensus or max rounds

Expected behavior:
- Loading spinner appears
- Models generate responses
- Consensus banner shows if agreement reached
- Final synthesis is displayed

## Customization

### Change Active Models

Edit `models_config.py`:

```python
DEFAULT_COUNCIL_MODELS = [
    "llama3.1",
    "mistral",
    # Add or remove models here
]
```

### Adjust Consensus Settings

Edit `models_config.py`:

```python
CONSENSUS_SETTINGS = {
    "max_rounds": 10,
    "min_agreement_ratio": 0.8,  # 80% of models must show agreement
    # Add more agreement phrases if needed
}
```
