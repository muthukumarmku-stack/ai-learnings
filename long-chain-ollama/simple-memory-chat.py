from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Initialize the Model (Think of this as injecting a @Service bean)
llm = ChatOllama(model="llama3.1:8b", temperature=0)

# 2. Create the Prompt Template (Similar to a parameterized prepared statement)
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Remember the conversation."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# 3. Create the Output Parser (Similar to mapping an Entity to a Response DTO)
parser = StrOutputParser()

# 4. Chain them together using LCEL
# Data flows left to right: Prompt -> LLM -> String Parser
chain = prompt | llm | parser

# Store conversations by session ID
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# We pass in a dictionary (map) containing the variables our template needs
chat_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 5. Execute the chain
print("Asking the local model...\n")
session_id = "default"

while True:
    user_input = input("Enter your question (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    response = chat_chain.stream(
        {
            "question": user_input
        },
        {
            "configurable": {"session_id": session_id}
        })

    for chunk in response:
        print(chunk, end="", flush=True)

    print("\n")

print("\n\nDone!")
