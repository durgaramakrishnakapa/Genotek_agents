"""
Web Tool for Hotel Construction Projects
Handles web searches specific to hospitality facilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import requests
import json

class HotelWebTool:
    """Web search tool specialized for hotel construction"""
    
    def __init__(self):
        from config import SERPER_API_KEY
        self.api_key = SERPER_API_KEY
        self.search_queries = [
            "hotel construction project 2024 developer contact",
            "new resort building project details",
            "luxury hotel construction contractor",
            "hospitality facility construction tender 2024"
        ]
    
    def search(self, query=None):
        """
        Search for hotel construction projects
        
        Args:
            query (str): Custom search query or use default
            
        Returns:
            dict: Search results
        """
        if query is None:
            query = self.search_queries[0]
        
        print(f"🔍 Searching: {query}")
        
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": query,
            "num": 10
        })
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            results = response.json()
            
            print(f"✅ Found {len(results.get('organic', []))} results")
            
            # Save to initial_data.json
            self.save_initial_data(results)
            
            return results
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None
    
    def save_initial_data(self, data):
        """Save raw search results to initial_data.json"""
        output_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Raw search data saved to initial_data.json")

if __name__ == "__main__":
    tool = HotelWebTool()
    tool.search()
