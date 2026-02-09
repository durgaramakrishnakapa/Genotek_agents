"""
Hospital Construction Projects Agent - Optimized
Searches globally for hospital constructions, processes top 2 with LLM
"""

import sys
import os
import json
import hashlib
from datetime import datetime

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, '../..'))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Import web_tool
import importlib.util
spec = importlib.util.spec_from_file_location("hospitals_web_tool", os.path.join(current_dir, 'web_tool.py'))
web_tool_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_tool_module)
HospitalWebTool = web_tool_module.HospitalWebTool

class HospitalAgent:
    """Optimized agent for hospital construction projects"""
    
    def __init__(self):
        self.name = "Hospital Construction Agent"
        self.web_tool = HospitalWebTool()
        
        from config import GROQ_API_KEY, LLM_MODEL
        self.llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.1)
        
        print(f"\n🏥 {self.name} - Searching 2026-2027 hospital projects\n")
    
    def generate_id(self, data):
        """Generate unique project ID"""
        unique = f"{data.get('title', '')}_{data.get('link', '')}"
        return f"HOSP_{hashlib.md5(unique.encode()).hexdigest()[:12].upper()}"
    
    def extract_details(self, result):
        """Extract project details using LLM"""
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        
        # Simple prompt for better JSON generation
        prompt_text = f"""Extract hospital construction project details from:

Title: {title}
Snippet: {snippet}

Return ONLY this JSON format (no extra text):
{{
  "project_name": "hospital name",
  "location": "city, country", 
  "status": "Under Construction 2026",
  "budget": "amount",
  "timeline": "completion year"
}}

If this is a list of multiple projects, return: {{"status": "ARTICLE_LIST"}}
If completed in 2024-2025, return: {{"status": "COMPLETED"}}"""

        try:
            # Use simple invoke instead of complex prompt template
            response = self.llm.invoke([("human", prompt_text)])
            content = response.content.strip()
            
            print(f"   🔍 LLM Response: {content}")
            
            # Extract JSON
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                
                # Parse JSON
                data = json.loads(json_str)
                
                # Check status
                status = data.get('status', '')
                if status in ['ARTICLE_LIST', 'COMPLETED']:
                    print(f"   ⏭️ Skipped - {status}")
                    return None
                
                print(f"   ✅ Extracted: {data.get('project_name', 'N/A')}")
                return data
            else:
                print(f"   ⚠️ No JSON brackets found")
                return None
                
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON error: {e}")
            return None
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            return None
    
    def run(self):
        """Run optimized hospital agent"""
        print("🔍 Searching hospital projects...")
        
        # Search and get top 2 results
        all_results = self.web_tool.search_all_queries()
        top_2 = self.web_tool.get_top_results(all_results, top_n=2)
        
        if not top_2:
            print("❌ No results found")
            return []
        
        print(f"🤖 Processing {len(top_2)} projects...")
        
        # Process each result
        processed = []
        for i, result in enumerate(top_2, 1):
            print(f"   📋 Project {i}: {result.get('title', 'N/A')[:50]}...")
            
            details = self.extract_details(result)
            
            # Skip if extraction failed or project was filtered out
            if details is None:
                continue
            
            project_id = self.generate_id(result)
            processed.append({
                "id": project_id,
                "raw_data": result,
                "extracted_data": details,
                "processed_at": datetime.now().isoformat()
            })
            
            print(f"   ✅ ID: {project_id}")
            print(f"   📍 {details.get('location', 'N/A')}")
            print(f"   🏥 {details.get('project_name', 'N/A')}")
        
        # Save results
        if processed:
            output_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
            data = {
                "agent": self.name,
                "specialty": "Global Healthcare Facilities",
                "timestamp": datetime.now().isoformat(),
                "total_projects": len(processed),
                "projects": processed
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Saved {len(processed)} projects to initial_data.json")
            for p in processed:
                print(f"   • {p['id']}: {p['extracted_data'].get('project_name', 'N/A')}")
        else:
            print("\n❌ No valid projects found")
        
        return processed

if __name__ == "__main__":
    agent = HospitalAgent()
    agent.run()
