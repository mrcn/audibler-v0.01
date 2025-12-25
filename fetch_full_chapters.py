#!/usr/bin/env python3
"""Fetch complete full text of Inadequate Equilibria chapters"""

import requests
from bs4 import BeautifulSoup
import time
import json

chapters = [
    {
        "number": 1,
        "title": "Inadequacy and Modesty",
        "url": "https://equilibriabook.com/inadequacy-and-modesty/"
    },
    {
        "number": 2,
        "title": "An Equilibrium of No Free Energy",
        "url": "https://equilibriabook.com/an-equilibrium-of-no-free-energy/"
    },
    {
        "number": 3,
        "title": "Moloch's Toolbox",
        "url": "https://equilibriabook.com/molochs-toolbox/"
    },
    {
        "number": 4,
        "title": "Living in an Inadequate World",
        "url": "https://equilibriabook.com/living-in-an-inadequate-world/"
    },
    {
        "number": 5,
        "title": "Blind Empiricism",
        "url": "https://equilibriabook.com/blind-empiricism/"
    },
    {
        "number": 6,
        "title": "Against Modest Epistemology",
        "url": "https://equilibriabook.com/against-modest-epistemology/"
    },
    {
        "number": 7,
        "title": "Status Regulation and Anxious Underconfidence",
        "url": "https://equilibriabook.com/status-regulation-and-anxious-underconfidence/"
    },
    {
        "number": 8,
        "title": "Conclusion",
        "url": "https://equilibriabook.com/conclusion/"
    }
]

def fetch_chapter(url, retries=5):
    """Fetch chapter content with retry logic"""
    for i in range(retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Attempt {i+1} failed: {e}")
            if i < retries - 1:
                wait_time = 3 * (2 ** i)  # Exponential backoff: 3, 6, 12, 24
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
    return None

def extract_full_content(html):
    """Extract complete chapter content from HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    # Try multiple selectors to find the main content
    content = None

    # Try common content selectors
    selectors = [
        'article.post',
        'div.entry-content',
        'article',
        'main',
        'div.post-content',
        'div.content',
        '.post-body'
    ]

    for selector in selectors:
        content = soup.select_one(selector)
        if content:
            break

    if not content:
        print("  Could not find content area, trying body")
        content = soup.body

    if content:
        # Remove unwanted elements
        for element in content.select('script, style, nav, header, footer, .navigation, .comments, .sidebar'):
            element.decompose()

        # Get HTML content preserving structure
        return str(content)

    return None

results = {}

print("Fetching full chapter content...\n")

for chapter in chapters:
    print(f"Fetching Chapter {chapter['number']}: {chapter['title']}...")
    html = fetch_chapter(chapter['url'])

    if html:
        content = extract_full_content(html)
        if content:
            results[chapter['number']] = {
                'title': chapter['title'],
                'content': content,
                'word_count': len(content.split())
            }
            print(f"  ✓ Successfully fetched (~{results[chapter['number']]['word_count']} words)")
        else:
            print(f"  ✗ Could not extract content")
    else:
        print(f"  ✗ Failed to fetch")

    time.sleep(2)  # Be polite to the server

# Save results
with open('full_chapters.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"Successfully fetched {len(results)}/8 chapters")
print(f"Total word count: {sum(r['word_count'] for r in results.values())}")
print(f"Results saved to: full_chapters.json")
