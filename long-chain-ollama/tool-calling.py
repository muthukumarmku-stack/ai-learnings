from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

llm = ChatOllama(model="llama3.1:8b", temperature=0)

@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two numbers together."""
    return a * b


tools = [add_numbers, multiply_numbers]

agent = create_agent(
    model=llm,
    tools=tools
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Add 10 and 20, then multiply the result by 5."
        }
    ]
})

print(result["messages"][-1].content)

