"""Client for interacting with the local Ollama API."""

import httpx
from config import OLLAMA_ENDPOINT, MODEL_NAME


async def generate_response(prompt: str) -> str:
    """Send a prompt to Ollama and return the generated response.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        The AI-generated response string.
        
    Raises:
        httpx.HTTPError: If there is a network or HTTP error.
        Exception: If Ollama returns an error status.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(OLLAMA_ENDPOINT, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
    except httpx.ConnectError:
        raise ConnectionError(
            "Cannot connect to Ollama. Make sure Ollama is running on "
            f"{OLLAMA_ENDPOINT}"
        )
    except httpx.HTTPStatusError as exc:
        raise Exception(f"Ollama HTTP error: {exc.response.status_code} - {exc.response.text}")
    except httpx.TimeoutException:
        raise Exception("Ollama request timed out. The model may be loading.")
