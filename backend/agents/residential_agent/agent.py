"""
Residential Construction Projects Agent
Specialized agent for residential construction projects
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from web_tool import ResidentialWebTool
import json

class ResidentialAgent:
    """Agent specialized in residential construction projects"""
    
    def __init__(self):
        self.name = "Residential Construction Agent"
        self.specialty = "Housing & Apartment Developments"
        self.web_tool = ResidentialWebTool()
        
        # Initialize LLM
        from config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        
        print(f"✅ {self.name} initialized")
        print(f"🏘️ Specialty: {self.specialty}")
    
    def search_projects(self):
        """Search for residential construction projects"""
        print(f"\n{'='*80}")
        print(f"🔍 {self.name} - Starting Search")
        print(f"{'='*80}\n")
        
        results = self.web_tool.search()
        return results
    
    def extract_details(self, search_results):
        """Extract detailed information from search results"""
        print("\n🤖 Extracting residential project details...")
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in residential construction projects.
            Extract DETAILED information about residential construction projects.
            Focus on: project name, developer, location, budget, timeline, 
            contact information, number of units, building type, amenities."""),
            ("human", "Extract details from: {results}")
        ])
        
        chain = extraction_prompt | self.llm
        response = chain.invoke({"results": str(search_results)})
        return response.content
    
    def run(self):
        """Run the complete residential agent workflow"""
        # Search
        search_results = self.search_projects()
        
        # Extract
        details = self.extract_details(search_results)
        
        # Save to final_data.json
        self.save_results(details)
        
        print(f"\n✅ {self.name} completed")
        return details
    
    def save_results(self, details):
        """Save results to final_data.json"""
        output_path = os.path.join(os.path.dirname(__file__), "final_data.json")
        
        result = {
            "agent": self.name,
            "specialty": self.specialty,
            "timestamp": str(os.path.getmtime(__file__)),
            "results": details
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to final_data.json")

if __name__ == "__main__":
    agent = ResidentialAgent()
    agent.run()
