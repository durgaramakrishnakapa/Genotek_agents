"""
Hotel Construction Projects Agent
Specialized agent for hospitality construction projects
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from web_tool import HotelWebTool
import json

class HotelAgent:
    """Agent specialized in hotel construction projects"""
    
    def __init__(self):
        self.name = "Hotel Construction Agent"
        self.specialty = "Hospitality & Resort Facilities"
        self.web_tool = HotelWebTool()
        
        # Initialize LLM
        from config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        
        print(f"✅ {self.name} initialized")
        print(f"🏨 Specialty: {self.specialty}")
    
    def search_projects(self):
        """Search for hotel construction projects"""
        print(f"\n{'='*80}")
        print(f"🔍 {self.name} - Starting Search")
        print(f"{'='*80}\n")
        
        results = self.web_tool.search()
        return results
    
    def extract_details(self, search_results):
        """Extract detailed information from search results"""
        print("\n🤖 Extracting hotel project details...")
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in hospitality construction projects.
            Extract DETAILED information about hotel construction projects.
            Focus on: project name, hotel brand, location, budget, timeline, 
            contact information, developer, room count, amenities, star rating."""),
            ("human", "Extract details from: {results}")
        ])
        
        chain = extraction_prompt | self.llm
        response = chain.invoke({"results": str(search_results)})
        return response.content
    
    def run(self):
        """Run the complete hotel agent workflow"""
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
    agent = HotelAgent()
    agent.run()
