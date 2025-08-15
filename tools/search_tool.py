"""
Web search functionality with multiple fallback methods
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import quote_plus

def search_web(query, num_results=5):
    """
    Search the web using multiple methods with fallbacks
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
        
    Returns:
        list: List of search results with title, url, and snippet
    """
    print(f"🔍 Searching for: {query}")
    
    # Try multiple search methods in order
    search_methods = [
        _search_with_requests,
        _search_duckduckgo_api,
        _search_wikipedia_fallback,
        _search_basic_scraping
    ]
    
    for i, method in enumerate(search_methods):
        try:
            print(f"Trying search method {i+1}...")
            results = method(query, num_results)
            if results and len(results) > 0 and "Error" not in results[0].get('title', ''):
                print(f"✅ Search successful with method {i+1}")
                return results
        except Exception as e:
            print(f"❌ Method {i+1} failed: {str(e)}")
            continue
    
    # If all methods fail, return a helpful error
    return [{
        'title': 'Search Unavailable',
        'url': '',
        'snippet': f'Unable to search for "{query}" at this time. Please try again later or check your internet connection.'
    }]

def _search_with_requests(query, num_results):
    """
    Search using requests with multiple user agents and delays
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Add random delay to avoid rate limiting
    time.sleep(random.uniform(1, 3))
    
    # Try Bing search first (less restrictive)
    try:
        search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return _parse_bing_results(response.content, num_results)
    except:
        pass
    
    # Fallback to Google
    try:
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return _parse_google_results(response.content, num_results)
    except:
        pass
    
    raise Exception("Request-based search failed")

def _parse_bing_results(html_content, num_results):
    """Parse Bing search results"""
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    search_results = soup.find_all('li', class_='b_algo')[:num_results]
    
    for result in search_results:
        try:
            title_elem = result.find('h2')
            link_elem = title_elem.find('a') if title_elem else None
            snippet_elem = result.find('p') or result.find('div', class_='b_caption')
            
            if title_elem and link_elem:
                title = title_elem.get_text().strip()
                url = link_elem.get('href', '')
                snippet = snippet_elem.get_text().strip() if snippet_elem else 'No description available'
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                })
        except:
            continue
    
    return results if results else []

def _parse_google_results(html_content, num_results):
    """Parse Google search results"""
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    # Try different Google result selectors
    selectors = [
        'div.g',
        'div[data-ved]',
        'div.rc'
    ]
    
    for selector in selectors:
        search_results = soup.select(selector)[:num_results]
        if search_results:
            break
    
    for result in search_results:
        try:
            title_elem = result.find('h3')
            link_elem = result.find('a')
            snippet_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
            
            if title_elem and link_elem:
                title = title_elem.get_text().strip()
                url = link_elem.get('href', '')
                snippet = snippet_elem.get_text().strip() if snippet_elem else 'No description available'
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                })
        except:
            continue
    
    return results if results else []

def _search_duckduckgo_api(query, num_results):
    """
    Try DuckDuckGo instant answer API (different from HTML scraping)
    """
    try:
        # DuckDuckGo instant answer API
        api_url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        
        headers = {
            'User-Agent': 'AI Assistant Search Bot 1.0'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        results = []
        
        # Check for instant answer
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'DuckDuckGo Result'),
                'url': data.get('AbstractURL', ''),
                'snippet': data.get('AbstractText', '')[:300]
            })
        
        # Check for related topics
        for topic in data.get('RelatedTopics', [])[:num_results-len(results)]:
            if isinstance(topic, dict) and topic.get('Text'):
                results.append({
                    'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' ').title(),
                    'url': topic.get('FirstURL', ''),
                    'snippet': topic.get('Text', '')[:200]
                })
        
        return results if results else []
        
    except Exception as e:
        raise Exception(f"DuckDuckGo API search failed: {str(e)}")

def _search_wikipedia_fallback(query, num_results):
    """
    Use Wikipedia search as fallback
    """
    try:
        import wikipedia
        
        # Search Wikipedia
        search_results = wikipedia.search(query, results=num_results)
        results = []
        
        for title in search_results[:num_results]:
            try:
                page = wikipedia.page(title)
                summary = wikipedia.summary(title, sentences=2)
                
                results.append({
                    'title': page.title,
                    'url': page.url,
                    'snippet': summary
                })
            except:
                continue
        
        return results if results else []
        
    except Exception as e:
        raise Exception(f"Wikipedia search failed: {str(e)}")

def _search_basic_scraping(query, num_results):
    """
    Basic web scraping with minimal requests
    """
    try:
        # Use a search aggregator or alternative search engine
        search_url = f"https://searx.space/search?q={quote_plus(query)}&format=json"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AI Assistant/1.0)'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                results = []
                
                for result in data.get('results', [])[:num_results]:
                    results.append({
                        'title': result.get('title', 'No title'),
                        'url': result.get('url', ''),
                        'snippet': result.get('content', 'No description')[:200]
                    })
                
                return results if results else []
            except:
                pass
        
        # Final fallback - create a mock result with search suggestion
        return [{
            'title': f'Search: {query}',
            'url': f'https://www.google.com/search?q={quote_plus(query)}',
            'snippet': f'Click to search for "{query}" on Google. Direct search is temporarily unavailable.'
        }]
        
    except Exception as e:
        raise Exception(f"Basic scraping failed: {str(e)}")

def search_wikipedia(query):
    """
    Search Wikipedia specifically
    """
    try:
        import wikipedia
        
        page = wikipedia.page(query)
        summary = wikipedia.summary(query, sentences=3)
        
        return {
            'title': page.title,
            'url': page.url,
            'summary': summary,
            'content': page.content[:1000] + '...' if len(page.content) > 1000 else page.content
        }
    except Exception as e:
        return {
            'title': 'Wikipedia Search Error',
            'url': '',
            'summary': f'Error searching Wikipedia: {str(e)}',
            'content': ''
        }
