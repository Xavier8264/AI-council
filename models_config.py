"""
Configuration for Ollama models used in the AI Council.

This file defines which models participate in the debate and provides
recommendations for the best performing models.
"""

# Recommended Ollama models for the AI Council
# These have been tested and provide good performance for debates
RECOMMENDED_MODELS = {
    "llama3.1": {
        "name": "Llama 3.1",
        "description": "Meta's latest Llama model - excellent for general reasoning",
        "size": "8B parameter version recommended",
        "pull_command": "ollama pull llama3.1"
    },
    "mistral": {
        "name": "Mistral",
        "description": "High-performance model with strong reasoning capabilities",
        "size": "7B parameters",
        "pull_command": "ollama pull mistral"
    },
    "gemma2": {
        "name": "Gemma 2",
        "description": "Google's Gemma 2 - strong at analytical tasks",
        "size": "9B parameter version recommended",
        "pull_command": "ollama pull gemma2"
    },
    "phi3": {
        "name": "Phi-3",
        "description": "Microsoft's Phi-3 - compact but powerful",
        "size": "3.8B parameters",
        "pull_command": "ollama pull phi3"
    },
    "qwen2.5": {
        "name": "Qwen 2.5",
        "description": "Alibaba's Qwen - excellent multilingual capabilities",
        "size": "7B parameter version recommended",
        "pull_command": "ollama pull qwen2.5"
    }
}

# Default models to use in the council
# You can modify this list to add or remove models
# Make sure these models are pulled in Ollama first!
DEFAULT_COUNCIL_MODELS = [
    "llama3.1",
    "mistral", 
    "gemma2",
    "phi3",
    "qwen2.5"
]

# Alternative model configurations you can try
ALTERNATIVE_CONFIGS = {
    "fast_council": ["llama3.1", "phi3", "gemma2"],  # Smaller, faster models
    "deep_thinkers": ["llama3.1", "mistral", "qwen2.5"],  # Better reasoning
    "minimal": ["llama3.1", "mistral"],  # Just 2 models for quick tests
}

# Consensus detection settings
CONSENSUS_SETTINGS = {
    "max_rounds": 10,  # Maximum debate rounds before forcing conclusion
    "similarity_threshold": 0.85,  # How similar responses must be (0-1)
    "min_agreement_ratio": 0.8,  # Minimum ratio of models that must agree
}

def get_active_models():
    """Get the list of models currently configured for the council."""
    return DEFAULT_COUNCIL_MODELS

def get_model_display_name(model_id):
    """Get a human-readable name for a model."""
    if model_id in RECOMMENDED_MODELS:
        return RECOMMENDED_MODELS[model_id]["name"]
    return model_id.title()

def get_consensus_settings():
    """Get the consensus detection settings."""
    return CONSENSUS_SETTINGS
