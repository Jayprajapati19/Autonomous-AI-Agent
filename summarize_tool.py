# tools/summarize_tool.py
from agent import ask_llm

def summarize_text(text: str):
    return ask_llm(f"Summarize the following:\n\n{text}")
