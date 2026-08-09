import ollama

while True:
    prompt = input("YOU>> ")
    if prompt.lower() == "quit":
        break

    response = ollama.chat(
        model="qwen3.6:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }

        ])
    print("\nAI>> ",response["message"]["content"])
