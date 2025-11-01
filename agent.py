# agent.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Allow model to be configured via environment, with a sane default
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
