"""FastAPI backend for Local Ollama AI Chat Application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama_client
import config

app = FastAPI(title="Local Ollama Chat API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Request model for chat messages."""
    prompt: str


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    response: str


@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Local Ollama Chat API is running"}


@app.get("/config")
async def get_config():
    """Get current configuration."""
    return {
        "ollama_endpoint": config.OLLAMA_ENDPOINT,
        "model": config.MODEL_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return AI response from Ollama."""
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        response_text = await ollama_client.generate_response(request.prompt)
        return ChatResponse(response=response_text)
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
