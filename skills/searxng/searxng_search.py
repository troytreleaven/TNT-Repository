#!/usr/bin/env python3
"""
SearxNG Search Skill for OpenClaw
Privacy-respecting metasearch engine integration
"""

import requests
import json
import sys
from typing import List, Dict, Optional

SEARXNG_URL = "http://127.0.0.1:8888"


def search(query: str, categories: str = "general", num_results: int = 10) -> List[Dict]:
    """
    Search using SearxNG
    
    Args:
        query: Search query
        categories: Search category (general, images, news, videos, etc.)
        num_results: Number of results to return
    
    Returns:
        List of search results
    """
    try:
        response = requests.get(
            f"{SEARXNG_URL}/search",
            params={
                "q": query,
                "format": "json",
                "categories": categories,
                "language": "en"
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])[:num_results]
        return results
    except Exception as e:
        return [{"error": str(e), "title": "Search failed", "url": ""}]


def format_results(results: List[Dict]) -> str:
    """Format search results for display"""
    if not results:
        return "No results found."
    
    output = []
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        content = result.get("content", "")
        engine = result.get("engine", "unknown")
        
        output.append(f"{i}. **{title}**")
        output.append(f"   {url}")
        if content:
            output.append(f"   {content[:150]}...")
        output.append(f"   Source: {engine}")
        output.append("")
    
    return "\n".join(output)


def search_images(query: str, num_results: int = 10) -> List[Dict]:
    """Search for images"""
    return search(query, categories="images", num_results=num_results)


def search_news(query: str, num_results: int = 10) -> List[Dict]:
    """Search for news"""
    return search(query, categories="news", num_results=num_results)


def search_videos(query: str, num_results: int = 10) -> List[Dict]:
    """Search for videos"""
    return search(query, categories="videos", num_results=num_results)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 searxng_search.py <query> [category] [num_results]")
        print("Categories: general, images, news, videos, it, science")
        sys.exit(1)
    
    query = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "general"
    num_results = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    results = search(query, category, num_results)
    print(format_results(results))


if __name__ == "__main__":
    main()
