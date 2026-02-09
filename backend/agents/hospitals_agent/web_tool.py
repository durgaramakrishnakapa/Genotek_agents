"""
Web Tool for Hospital Construction Projects
Handles web searches specific to healthcare facilities using SerperDev API
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import requests
import json
from datetime import datetime

class HospitalWebTool:
    """Web search tool specialized for hospital construction worldwide"""
    
    def __init__(self):
        from config import SERPER_API_KEY
        self.api_key = SERPER_API_KEY
        
        # Smart search queries for SPECIFIC hospital construction projects ONLY
        # Updated for 2026 - searching for individual hospital projects, not lists
        self.search_queries = [
            '"hospital construction" "under construction" 2026 2027 -"projects worth" -"list of"',
            '"medical center" "construction started" 2026 "breaking ground" -"multiple projects"',
            '"new hospital" "construction project" 2026 2027 "expected completion" -"several"',
            '"healthcare facility" "under development" 2026 "construction begins" -"various"',
            '"hospital project" "construction" 2026 2027 "opening" -"projects include" -"among"'
        ]
    
    def search_all_queries(self):
        """
        Search using all queries and aggregate results
        
        Returns:
            list: All search results from multiple queries
        """
        all_results = []
        
        print(f"\n{'='*80}")
        print("🌍 GLOBAL HOSPITAL CONSTRUCTION SEARCH")
        print(f"{'='*80}\n")
        
        for idx, query in enumerate(self.search_queries, 1):
            print(f"\n🔍 Query {idx}/{len(self.search_queries)}: {query}")
            results = self.search_single_query(query)
            
            if results and 'organic' in results:
                all_results.extend(results['organic'])
                print(f"✅ Found {len(results['organic'])} results")
            else:
                print("⚠️ No results for this query")
        
        print(f"\n📊 Total results collected: {len(all_results)}")
        return all_results
    
    def search_single_query(self, query):
        """
        Search for hospital construction projects using SerperDev
        
        Args:
            query (str): Search query
            
        Returns:
            dict: Search results from SerperDev
        """
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": query,
            "num": 10,  # Get 10 results per query
            "gl": "us",  # Global search
            "hl": "en"   # English results
        })
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None
    
    def get_top_results(self, all_results, top_n=2):
        """
        Filter and get top N unique results - ONLY RECENT/ONGOING PROJECTS
        
        Args:
            all_results (list): All search results
            top_n (int): Number of top results to return (default 2)
            
        Returns:
            list: Top N unique results
        """
        # Keywords that indicate RECENT/ONGOING construction (2026 focus)
        positive_keywords = [
            'under construction', 'construction started', 'breaking ground',
            'construction begins', 'announced', 'planned', 'upcoming',
            'new project', 'development', 'building', '2026', '2027', '2028',
            'to be built', 'will be built', 'future', 'proposed'
        ]
        
        # Keywords that indicate COMPLETED projects or LIST ARTICLES (to exclude)
        negative_keywords = [
            'completed 2024', 'completed 2025', 'opened 2024', 'opened 2025',
            'inaugurated 2024', 'inaugurated 2025', 'grand opening 2024',
            'grand opening 2025', 'now open', 'already opened',
            'renovation', 'redevelopment', 'expansion of existing',
            # List article indicators
            'projects worth', 'list of', 'several projects', 'multiple projects',
            'various projects', 'projects include', 'among the projects',
            '15 hospital projects', '10 hospital projects', 'hospital projects worth'
        ]
        
        # Filter for recent/ongoing projects only
        filtered_results = []
        seen_urls = set()
        
        for result in all_results:
            url = result.get('link', '')
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            combined_text = f"{title} {snippet}"
            
            # Skip if URL already seen
            if url in seen_urls:
                continue
            
            # Check if it's a completed project (exclude)
            is_completed = any(keyword in combined_text for keyword in negative_keywords)
            if is_completed:
                continue
            
            # Check if it's a recent/ongoing project (include)
            is_recent = any(keyword in combined_text for keyword in positive_keywords)
            if is_recent:
                seen_urls.add(url)
                filtered_results.append(result)
        
        # Return top N results
        top_results = filtered_results[:top_n]
        
        print(f"\n🎯 Selected TOP {len(top_results)} RECENT/ONGOING hospital projects")
        for idx, result in enumerate(top_results, 1):
            print(f"   {idx}. {result.get('title', 'N/A')[:70]}...")
        
        return top_results
    
    def save_raw_results(self, results):
        """
        Save raw search results to initial_data.json
        
        Args:
            results (list): Search results to save
        """
        output_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
        
        data = {
            "note": "Raw search results from SerperDev API for hospital construction projects",
            "agent": "Hospital Construction Agent",
            "timestamp": datetime.now().isoformat(),
            "total_results": len(results),
            "data": results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Raw search data saved to initial_data.json")
        print(f"📁 Location: {output_path}")

if __name__ == "__main__":
    tool = HospitalWebTool()
    all_results = tool.search_all_queries()
    top_2 = tool.get_top_results(all_results, top_n=2)
    tool.save_raw_results(top_2)
