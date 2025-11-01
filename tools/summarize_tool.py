"""
Text summarization functionality using Groq AI
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')

def summarize_text(text, max_length=200):
    """
    Summarize text using Groq AI
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum length of summary in words
        
    Returns:
        str: Summarized text
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Create prompt for summarization
        prompt = f"""
        Please provide a concise summary of the following text in approximately {max_length} words or less:

        {text}

        Summary:
        """
        
        # Make API call
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=GROQ_MODEL,
            max_tokens=max_length * 2,  # Allow some buffer
            temperature=0.3
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"❌ Summarization error: {e}")
        return _fallback_summarize(text, max_length)

def _fallback_summarize(text, max_length):
    """
    Fallback summarization using simple text extraction
    """
    try:
        sentences = text.split('.')
        words = text.split()
        
        if len(words) <= max_length:
            return text
        
        # Take first few sentences that fit within word limit
        summary_words = []
        for sentence in sentences:
            sentence_words = sentence.split()
            if len(summary_words) + len(sentence_words) <= max_length:
                summary_words.extend(sentence_words)
            else:
                break
        
        if not summary_words:
            # If no complete sentences fit, truncate
            summary_words = words[:max_length]
        
        return ' '.join(summary_words) + ('...' if len(words) > max_length else '')
        
    except Exception as e:
        return f"Error creating summary: {str(e)}"

def summarize_url_content(url, max_length=200):
    """
    Fetch content from URL and summarize it
    
    Args:
        url (str): URL to fetch and summarize
        max_length (int): Maximum summary length
        
    Returns:
        str: Summarized content
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Fetch webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Summarize the extracted text
        return summarize_text(text, max_length)
        
    except Exception as e:
        return f"Error summarizing URL content: {str(e)}"

def summarize_multiple_texts(texts, max_length=300):
    """
    Summarize multiple texts into a single summary
    
    Args:
        texts (list): List of texts to summarize
        max_length (int): Maximum summary length
        
    Returns:
        str: Combined summary
    """
    try:
        # Combine all texts
        combined_text = ' '.join(texts)
        
        # Create a prompt for multi-text summarization
        prompt = f"""
        Please create a comprehensive summary that combines the key points from the following texts:

        {combined_text}

        Provide a unified summary in approximately {max_length} words that captures the main themes and important information from all the texts.

        Summary:
        """
        
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=GROQ_MODEL,
            max_tokens=max_length * 2,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"❌ Multi-text summarization error: {e}")
        return _fallback_summarize(combined_text, max_length)
