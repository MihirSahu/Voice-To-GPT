import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = os.getenv("MODEL_ENGINE")
prompt = input("Enter your prompt: ")
max_tokens = 50

response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[{"content": prompt, "role": "user"}],
    max_tokens=max_tokens,
)

print(response.choices[0].message.content)