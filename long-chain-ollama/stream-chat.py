from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import MarkdownListOutputParser;

# 1. Initialize the Model (Think of this as injecting a @Service bean)
llm = ChatOllama(model="llama3.1:8b", temperature=0)

# 2. Create the Prompt Template (Similar to a parameterized prepared statement)
prompt = ChatPromptTemplate.from_template("{question} in java")

# 3. Create the Output Parser (Similar to mapping an Entity to a Response DTO)
parser = StrOutputParser()

# 4. Chain them together using LCEL
# Data flows left to right: Prompt -> LLM -> String Parser
chain = prompt | llm | parser

# 5. Execute the chain
print("Asking the local model...\n")

# We pass in a dictionary (map) containing the variables our template needs
response = chain.stream({
    "question": "Threads"
})

for chunk in response:
    print(chunk, end="", flush=True)

print("\n\nDone!")
