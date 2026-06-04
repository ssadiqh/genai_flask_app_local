# Configuration for Local Qwen2.5:7b via Ollama
# This replaces IBM Watson configuration from the original course

# Model parameters
PARAMETERS = {
    "temperature": 0.3,  # Lower temp for consistent responses
    "max_tokens": 256,   # Maximum tokens in response
}

# Ollama credentials (local)
CREDENTIALS = {
    "model": "qwen2.5:7b",
    "base_url": "http://localhost:11434"  # Local Ollama endpoint
}

# Model ID - We're using local Qwen instead of IBM models
QWEN_MODEL = "qwen2.5:7b"