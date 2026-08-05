"""Application configuration."""

OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
OLLAMA_ENDPOINT = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
MODEL_NAME = "qwen3.6:latest"
