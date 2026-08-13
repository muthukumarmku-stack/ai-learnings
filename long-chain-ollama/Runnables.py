from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda


passthrough = RunnablePassthrough();

response = passthrough.invoke({"question": input("Enter your question (or 'exit' to quit): ")})

response2 = RunnableLambda(lambda x: x.upper()).invoke(response.get("question"))

print(response)

print(response2)
