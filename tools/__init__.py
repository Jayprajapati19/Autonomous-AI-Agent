"""
Tools package for AI Assistant
Contains various utility tools for web search, email, summarization, etc.
"""

from .search_tool import search_web, search_wikipedia
from .email_tool import send_email, send_simple_email
from .summarize_tool import summarize_text, summarize_url_content, summarize_multiple_texts

__all__ = [
    'search_web', 
    'search_wikipedia',
    'send_email', 
    'send_simple_email',
    'summarize_text',
    'summarize_url_content',
    'summarize_multiple_texts'
]
