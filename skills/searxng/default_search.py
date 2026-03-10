#!/usr/bin/env python3
"""
SearxNG Default Search Adapter
Replaces Brave Search with self-hosted SearxNG for all OpenClaw queries
"""

import sys
import os
sys.path.insert(0, '/data/.openclaw/workspace/skills/searxng')

from searxng_search import search, format_results
from typing import List, Dict, Optional


def web_search(
    query: str,
    count: int = 5,
    country: str = "US",
    freshness: Optional[str] = None,
    search_lang: str = "en",
    ui_lang: str = "en"
) -> List[Dict]:
    """
    Search using SearxNG (replaces Brave Search)
    
    Args:
        query: Search query
        count: Number of results (1-20)
        country: 2-letter country code for region-specific results
        freshness: Filter by time (pd=past day, pw=week, pm=month, py=year)
        search_lang: Language for search results
        ui_lang: Language for UI elements
    
    Returns:
        List of search results with title, url, description
    """
    # Map freshness to SearxNG time ranges if needed
    # Note: SearxNG handles this through engine-specific parameters
    
    # Perform search
    results = search(query, categories="general", num_results=min(count, 20))
    
    # Format to match Brave API output format for compatibility
    formatted_results = []
    for result in results:
        if "error" in result:
            continue
            
        formatted_results.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "description": result.get("content", ""),
            "site_name": result.get("engine", "searxng"),
            "published": None,  # SearxNG doesn't always provide this
        })
    
    return formatted_results


def search_images(query: str, count: int = 10) -> List[Dict]:
    """Search for images using SearxNG"""
    results = search(query, categories="images", num_results=count)
    return results


def search_news(query: str, count: int = 10) -> List[Dict]:
    """Search for news using SearxNG"""
    results = search(query, categories="news", num_results=count)
    return results


# Backwards compatibility alias
searx_search = web_search


if __name__ == "__main__":
    # Test the adapter
    print("Testing SearxNG default search adapter...\n")
    
    query = "Dale Carnegie leadership training"
    print(f"Query: {query}\n")
    
    results = web_search(query, count=5)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   {result['description'][:100]}...")
        print()
    
    print(f"\n✅ SearxNG returned {len(results)} results")
