# Example: Adding New Models to AI Council

This document shows how to add new Ollama models to your AI Council.

## Step 1: Pull the Model in Ollama

First, pull the model you want to add:

```bash
ollama pull deepseek-coder  # Example: adding DeepSeek Coder
```

Verify it's available:
```bash
ollama list
```

## Step 2: Add to models_config.py

### Option A: Quick Addition (Recommended for Testing)

Simply add the model name to `DEFAULT_COUNCIL_MODELS`:

```python
DEFAULT_COUNCIL_MODELS = [
    "llama3.1",
    "mistral", 
    "gemma2",
    "phi3",
    "qwen2.5",
    "deepseek-coder"  # Your new model
]
```

### Option B: Full Addition with Documentation

Add an entry to `RECOMMENDED_MODELS` for better documentation:

```python
RECOMMENDED_MODELS = {
    # ... existing models ...
    "deepseek-coder": {
        "name": "DeepSeek Coder",
        "description": "Specialized in code generation and analysis",
        "size": "6.7B parameters",
        "pull_command": "ollama pull deepseek-coder"
    }
}
```

Then add to `DEFAULT_COUNCIL_MODELS`:

```python
DEFAULT_COUNCIL_MODELS = [
    "llama3.1",
    "mistral", 
    "gemma2",
    "phi3",
    "qwen2.5",
    "deepseek-coder"
]
```

## Step 3: Restart the Application

```bash
# Stop the current server (Ctrl+C)
# Start it again:
python main.py
```

## Step 4: Verify in the UI

1. Open http://localhost:8000
2. Check the status banner shows your new model
3. Start a debate to see it participate

## Example Configurations

### Fast Council (2-3 small models)

```python
DEFAULT_COUNCIL_MODELS = [
    "phi3",        # 3.8B - very fast
    "gemma2:2b",   # 2B - fastest option
]
```

### Deep Thinkers (larger, more capable models)

```python
DEFAULT_COUNCIL_MODELS = [
    "llama3.1:70b",  # Needs significant RAM/VRAM
    "mixtral",        # 8x7B MoE architecture
    "qwen2.5:14b"    # Larger version
]
```

### Specialized Council (domain-specific)

```python
# For coding questions
DEFAULT_COUNCIL_MODELS = [
    "codellama",
    "deepseek-coder",
    "phind-codellama"
]
```

### Multilingual Council

```python
DEFAULT_COUNCIL_MODELS = [
    "qwen2.5",      # Excellent for Chinese
    "aya",          # Multilingual
    "llama3.1"      # Strong English
]
```

## Testing Your New Model

Test with a simple question first:

1. Question: "What is 2 + 2?"
2. Max rounds: 2
3. Verify your new model responds correctly

## Removing Models

To remove a model from the council:

1. Remove from `DEFAULT_COUNCIL_MODELS` list in `models_config.py`
2. Restart the server
3. (Optional) Remove from Ollama: `ollama rm model-name`

## Tips

1. **Start small**: Test with 2 models first
2. **Match models to task**: Use coding models for code, general models for reasoning
3. **Monitor performance**: Larger models are slower but may give better results
4. **Mix sizes**: Combine fast small models with slower large ones for balance

## Model Naming in Ollama

Ollama models can have version tags:
- `llama3.1` = `llama3.1:latest`
- `gemma2:2b` = specific 2B version
- `qwen2.5:7b` = 7B parameter version

The AI Council will match models with or without version tags.
