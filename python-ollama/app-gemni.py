
from google import genai
import config

client = genai.Client(
    api_key=config.GEMINI_API_KEY
)

response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents="what is the object oriented programming?"
)
        
print(response.text)
