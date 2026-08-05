"""Streamlit frontend for Local Ollama AI Chat Application."""

import streamlit as st
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="Local Ollama Chat", page_icon="🤖", layout="centered")
st.title("🤖 Local Ollama AI Chat")
st.caption("Powered by Qwen 3.6 · Runs completely locally")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show loading indicator
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Thinking...")

    # Send request to backend
    ai_response = ""
    try:
        response = httpx.post(
            f"{API_BASE_URL}/chat",
            json={"prompt": prompt},
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        ai_response = data["response"]
    except httpx.ConnectError:
        ai_response = "❌ **Connection Error:** Cannot reach the backend API. Make sure the FastAPI server is running on port 8000."
    except httpx.HTTPStatusError as exc:
        ai_response = f"❌ **Server Error:** {exc.response.status_code} – {exc.response.text}"
    except Exception as exc:
        ai_response = f"❌ **Error:** {str(exc)}"

    # Display AI response
    placeholder.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Add a sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This application runs entirely on your local machine.

    **Tech stack:**
    - Backend: FastAPI + Uvicorn
    - Frontend: Streamlit
    - AI Model: Qwen 3.6 (via Ollama)

    **Prerequisites:**
    1. [Ollama](https://ollama.ai) installed and running
    2. `qwen3.6` model pulled (`ollama pull qwen3.6`)
    3. Backend dependencies installed
    4. Streamlit installed

    **Quick start:**
    ```bash
    # Terminal 1 – start backend
    cd backend && pip install -r requirements.txt
    uvicorn main:app --reload

    # Terminal 2 – start frontend
    cd frontend && pip install streamlit
    streamlit run app.py
    ```
    """)
