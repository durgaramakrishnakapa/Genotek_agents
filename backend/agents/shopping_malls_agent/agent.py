"""
Shopping Mall Construction Projects Agent
Searches globally for recent shopping mall constructions, processes top 5 with LLM
"""

import sys
import os
import json
import hashlib
from datetime import datetime

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '../..')
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Import web_tool - will be loaded from current directory
import importlib.util
web_tool_path = os.path.join(current_dir, 'web_tool.py')
spec = importlib.util.spec_from_file_location("shopping_malls_web_tool", web_tool_path)
web_tool_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_tool_module)
ShoppingMallWebTool = web_tool_module.ShoppingMallWebTool

class ShoppingMallAgent:
    """Agent specialized in shopping mall construction projects worldwide"""
    
    def __init__(self):
        self.name = "Shopping Mall Construction Agent"
        self.specialty = "Global Retail & Commercial Facilities"
        self.web_tool = ShoppingMallWebTool()
        
        # Initialize LLM
        from config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=0.1  # Lower temperature for more accurate extraction
        )
        
        print(f"\n{'='*80}")
        print(f"✅ {self.name} INITIALIZED")
        print(f"{'='*80}")
        print(f"🏬 Specialty: {self.specialty}")
        print(f"🌍 Scope: Worldwide FUTURE/ONGOING shopping mall construction")
        print(f"📅 Year: 2026 - Searching for projects NOT YET COMPLETED")
        print(f"🎯 Target: Top 2 best projects (2026-2027 timeline)")
        print(f"{'='*80}\n")
    
    def generate_project_id(self, project_data):
        """
        Generate unique ID for each project
        
        Args:
            project_data (dict): Project information
            
        Returns:
            str: Unique project ID
        """
        # Create ID from title and link
        unique_string = f"{project_data.get('title', '')}_{project_data.get('link', '')}"
        hash_object = hashlib.md5(unique_string.encode())
        return f"MALL_{hash_object.hexdigest()[:12].upper()}"
    
    def search_projects(self):
        """Search for shopping mall construction projects globally"""
        print("🔍 STEP 1: SEARCHING FOR SHOPPING MALL PROJECTS")
        print("-" * 80)
        
        # Search using multiple queries
        all_results = self.web_tool.search_all_queries()
        
        # Get top 2 unique results (ONLY RECENT/ONGOING)
        top_2_results = self.web_tool.get_top_results(all_results, top_n=2)
        
        # Save raw results
        self.web_tool.save_raw_results(top_2_results)
        
        return top_2_results
    
    def process_with_llm(self, top_2_results):
        """
        Process each of the top 2 results with LLM to extract COMPLETE detailed information
        
        Args:
            top_2_results (list): Top 2 search results
            
        Returns:
            list: Processed projects with IDs
        """
        print(f"\n🤖 STEP 2: PROCESSING TOP 2 PROJECTS WITH AI")
        print("-" * 80)
        
        processed_projects = []
        
        for idx, result in enumerate(top_2_results, 1):
            print(f"\n📋 Processing Project {idx}/2...")
            print(f"   Title: {result.get('title', 'N/A')[:60]}...")
            
            # Generate unique ID
            project_id = self.generate_project_id(result)
            
            # Extract detailed information using LLM
            details = self.extract_project_details(result, project_id)
            
            # Skip if project is completed or extraction failed
            if details is None or details.get('status') == 'COMPLETED - SKIP':
                print(f"   ⏭️ Skipped (completed or invalid)")
                continue
            
            # Add to processed list
            processed_projects.append({
                "id": project_id,
                "raw_data": result,
                "extracted_data": details,
                "processed_at": datetime.now().isoformat()
            })
            
            print(f"   ✅ Generated ID: {project_id}")
            print(f"   📍 Location: {details.get('location', 'N/A')}")
            print(f"   🏗️ Status: {details.get('status', 'N/A')}")
        
        return processed_projects
    
    def extract_project_details(self, search_result, project_id):
        """
        Extract detailed information from a single search result using LLM
        
        Args:
            search_result (dict): Single search result
            project_id (str): Generated project ID
            
        Returns:
            dict: Extracted project details
        """
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in shopping mall construction projects worldwide.

CRITICAL INSTRUCTIONS:
1. Extract ONLY if this is a FUTURE/ONGOING construction project (under construction in 2026, planned for 2026-2027, announced for future)
2. If the project was COMPLETED in 2024 or 2025 or ALREADY OPENED, return: {{"status": "COMPLETED - SKIP"}}
3. We are in 2026 - focus on projects that are NOT YET COMPLETED
4. Extract MAXIMUM details - be thorough and precise
5. Use EXACT information from the search result - DO NOT make assumptions

Extract these fields (REQUIRED):
- project_name: EXACT name of the shopping mall
- location: City, State/Province, Country (be VERY specific)
- developer: Company developing the mall
- status: "Under Construction" OR "Planned for 2026-2027" OR "Announced" (NOT "Completed")
- budget: Exact amount with currency (e.g., "$500M", "€200M")
- timeline: "Start: [date] - Expected Completion: [date]" (must be 2026 or later)
- size: Square footage or square meters
- features: Key features, anchor tenants, special amenities
- contact_info: Any emails, phones, websites found
- contractor: Construction company name

Return ONLY valid JSON with these exact keys. If information truly not available, use "Not specified"."""),
            ("human", """Search Result:
Title: {title}
Link: {link}
Snippet: {snippet}
Date: {date}

Extract COMPLETE information about this shopping mall construction project.
Return ONLY JSON format.""")
        ])
        
        chain = extraction_prompt | self.llm
        
        try:
            response = chain.invoke({
                "title": search_result.get('title', 'N/A'),
                "link": search_result.get('link', 'N/A'),
                "snippet": search_result.get('snippet', 'N/A'),
                "date": search_result.get('date', 'N/A')
            })
            
            # Try to parse as JSON
            try:
                # Clean the response to get only JSON
                content = response.content.strip()
                # Find JSON in the response
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    details = json.loads(json_str)
                    
                    # Check if project is completed (skip it)
                    if details.get('status') == 'COMPLETED - SKIP':
                        print(f"   ⚠️ Skipping - Project already completed")
                        return None
                else:
                    details = {"raw_extraction": content}
            except Exception as parse_error:
                print(f"   ⚠️ JSON parse error: {parse_error}")
                details = {"raw_extraction": response.content}
            
            return details
            
        except Exception as e:
            print(f"   ⚠️ Extraction error: {e}")
            return {"error": str(e)}
    
    def save_to_initial_data(self, processed_projects):
        """
        Save processed projects with IDs to initial_data.json
        
        Args:
            processed_projects (list): List of processed projects
        """
        print(f"\n💾 STEP 3: SAVING TO INITIAL_DATA.JSON")
        print("-" * 80)
        
        output_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
        
        data = {
            "agent": self.name,
            "specialty": self.specialty,
            "timestamp": datetime.now().isoformat(),
            "total_projects": len(processed_projects),
            "note": "Top 2 RECENT/ONGOING shopping mall construction projects with complete information",
            "projects": processed_projects
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(processed_projects)} projects to initial_data.json")
        print(f"📁 Location: {output_path}")
        
        # Print summary
        print(f"\n📊 PROJECT IDs GENERATED:")
        for project in processed_projects:
            print(f"   • {project['id']}")
    
    def run(self):
        """Run the complete shopping mall agent workflow"""
        print(f"\n{'🚀 STARTING SHOPPING MALL AGENT':^80}")
        print("=" * 80)
        
        # Step 1: Search for projects
        top_2_results = self.search_projects()
        
        if not top_2_results:
            print("\n❌ No RECENT/ONGOING results found. Exiting.")
            return
        
        # Step 2: Process with LLM and generate IDs
        processed_projects = self.process_with_llm(top_2_results)
        
        if not processed_projects:
            print("\n❌ No valid projects after processing. All were completed or invalid.")
            return
        
        # Step 3: Save to initial_data.json
        self.save_to_initial_data(processed_projects)
        
        # Final summary
        print(f"\n{'='*80}")
        print(f"✅ {self.name} COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        print(f"📊 Total Projects Found: {len(processed_projects)}")
        print(f"💾 Data saved to: initial_data.json")
        print(f"{'='*80}\n")
        
        return processed_projects

if __name__ == "__main__":
    agent = ShoppingMallAgent()
    agent.run()
