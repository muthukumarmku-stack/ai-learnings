# Local Ollama AI Chat Application

A full-stack chat application that runs entirely on your local machine, using **Ollama** (Qwen 3.6 model) for AI-powered responses — no cloud APIs required.

## Architecture

```
┌──────────────┐       HTTP POST        ┌──────────────┐       HTTP POST        ┌───────────┐
│   Streamlit   │ ──────────────────►   │  FastAPI     │ ──────────────────►   │  Ollama   │
│  Frontend    │   localhost:8000/chat  │  Backend     │   localhost:11434     │  Local    │
│  (Port 8501) │ ◄──────────────────   │  (Port 8000) │ ◄─────────────────   │  API      │
└──────────────┘       JSON response     └──────────────┘    JSON response     └───────────┘
```

- **Backend**: FastAPI + Uvicorn, exposes a `/chat` endpoint that proxies prompts to the local Ollama API.
- **Frontend**: Streamlit web app with chat history UI, markdown rendering, and error handling.
- **AI Model**: Qwen 3.6 (served via Ollama at `http://127.0.0.1:11434/api/generate`).

## Prerequisites

1. **[Ollama](https://ollama.ai)** installed and running locally
2. **Qwen 3.6 model** pulled via Ollama:
   ```bash
   ollama pull qwen3.6:latest
   ```

## Project Structure

```
local-ollama-chat-app/
├── backend/
│   ├── config.py          # Ollama endpoint & model configuration
│   ├── main.py            # FastAPI application (health, config, chat endpoints)
│   ├── ollama_client.py   # Async HTTP client for Ollama API calls
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── app.py             # Streamlit chat interface
│   └── requirements.txt   # Frontend dependency (streamlit)
└── README.md
```

## Setup & Quick Start

### 1. Configure Ollama Endpoint

Edit `backend/config.py` if needed:

```python
OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
MODEL_NAME = "qwen3.6:latest"
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Backend dependencies:**
| Package    | Minimum Version |
|------------|-----------------|
| fastapi    | 0.115.0         |
| uvicorn    | 0.32.0          |
| httpx      | 0.27.0          |
| pydantic   | 2.9.0           |

### 3. Install Frontend Dependencies

```bash
cd frontend
pip install streamlit
```

### 4. Start the Services

Open **two terminal windows**:

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://0.0.0.0:8000`.

**Terminal 2 — Frontend:**
```bash
cd frontend
streamlit run app.py
```
The web UI will open in your browser (typically `http://localhost:8501`).

## API Endpoints

### GET `/`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Local Ollama Chat API is running"
}
```

### GET `/config`
Returns the current Ollama configuration (endpoint URL and model name).

**Response:**
```json
{
  "ollama_endpoint": "http://127.0.0.1:11434/api/generate",
  "model": "qwen3.6:latest"
}
```

### POST `/chat`
Send a chat message and receive an AI-generated response.

**Request Body:**
```json
{
  "prompt": "Explain quantum computing in simple terms."
}
```

**Response:**
```json
{
  "response": "Quantum computing uses quantum mechanical phenomena..."
}
```

**Error Responses:**
| Status Code | Condition                         |
|-------------|----------------------------------|
| 400         | Empty prompt                     |
| 503         | Cannot connect to Ollama         |
| 500         | Ollama returned an HTTP error    |

## How It Works

1. The user types a message in the Streamlit frontend.
2. The frontend sends a `POST /chat` request to the FastAPI backend with the prompt.
3. The backend forwards the prompt to Ollama's `/api/generate` endpoint using the configured model (`qwen3.6:latest`).
4. Ollama generates a response and returns it as JSON.
5. The backend proxies the response back to the frontend, which displays it in the chat UI.
6. Both user messages and AI responses are stored in the Streamlit session state for the current conversation.

## Configuration

| Setting          | Default Value              | Description                     |
|------------------|----------------------------|---------------------------------|
| `OLLAMA_HOST`    | `127.0.0.1`               | Ollama server host              |
| `OLLAMA_PORT`    | `11434`                   | Ollama server port              |
| `MODEL_NAME`     | `qwen3.6:latest`          | Ollama model to use             |
| Request Timeout  | `120.0s`                  | Maximum wait for Ollama response|

To change the model, update `MODEL_NAME` in `backend/config.py` and ensure the model is pulled in Ollama:
```bash
ollama pull <your-model>
```

## Notes

- Everything runs **100% locally** — no external API keys or cloud services.
- If Ollama takes a long time to respond, it may be loading the model for the first time. The 120s timeout handles this gracefully.
- CORS is configured to allow `*` origins so the Streamlit frontend can communicate with the backend regardless of port.

## License

(Add your license here)
