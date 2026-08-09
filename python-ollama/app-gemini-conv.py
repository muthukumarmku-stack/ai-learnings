from google import genai
import config

client = genai.Client(
    api_key=config.GEMINI_API_KEY
)

chat = client.chats.create(
    model=config.GEMINI_MODEL
)

while True:
    prompt = input("\nYou: ")
    if prompt == "quit":
        break
    response = chat.send_message(prompt)
    print("\nAI:",end="")

    for chunk in response:
        if hasattr(chunk, 'text'):
            print(chunk.text, end="", flush=True)

    print()
print("Bye..")
