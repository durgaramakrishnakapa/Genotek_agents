"""
Genotek AI Lead Generation System
Uses SerperDev for search and Groq LLM for processing
Standalone backend - no frontend connection
"""

import requests
import json
import os
import re
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import (
    SERPER_API_KEY,
    GROQ_API_KEY,
    SEARCH_QUERIES,
    LLM_MODEL,
    LLM_TEMPERATURE,
    EXTRACTION_SYSTEM_PROMPT,
    CLASSIFICATION_SYSTEM_PROMPT,
    EMAIL_GENERATION_SYSTEM_PROMPT
)


class GenotekLeadGenerator:
    """Main class for lead generation and processing"""
    
    def __init__(self):
        """Initialize the lead generator with API keys and LLM"""
        self.serper_api_key = SERPER_API_KEY
        self.groq_api_key = GROQ_API_KEY
        self.generated_leads = []
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        
        print("✅ Genotek Lead Generator initialized (Standalone Mode)")
        print(f"📊 Using model: {LLM_MODEL}")
        print("-" * 80)
    
    def search_with_serper(self, query):
        """
        Search using SerperDev API
        
        Args:
            query (str): Search query
            
        Returns:
            dict: Search results
        """
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": query,
            "num": 10  # Number of results
        })
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error searching with SerperDev: {e}")
            return None
    
    def extract_project_info(self, search_results):
        """
        Extract structured project information from search results using LLM
        FOCUSES ON TOP RESULT ONLY for maximum detail extraction
        
        Args:
            search_results (dict): Raw search results from SerperDev
            
        Returns:
            str: Extracted project information
        """
        # Prepare search results text - ONLY TOP RESULT
        results_text = ""
        
        if "organic" in search_results and len(search_results["organic"]) > 0:
            # Get ONLY the first result for detailed analysis
            top_result = search_results["organic"][0]
            results_text = f"""
TOP SEARCH RESULT (Focus on this ONLY):

Title: {top_result.get('title', 'N/A')}
Link: {top_result.get('link', 'N/A')}
Snippet: {top_result.get('snippet', 'N/A')}

ADDITIONAL CONTEXT (if available):
"""
            # Add a bit of context from 2nd result if available
            if len(search_results["organic"]) > 1:
                second_result = search_results["organic"][1]
                results_text += f"\n2nd Result Title: {second_result.get('title', 'N/A')}"
                results_text += f"\n2nd Result Snippet: {second_result.get('snippet', 'N/A')}\n"
        
        # Create prompt for extraction
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", EXTRACTION_SYSTEM_PROMPT),
            ("human", "Extract DETAILED construction project information from the TOP search result:\n\n{results}")
        ])
        
        # Create chain and invoke
        chain = extraction_prompt | self.llm
        
        try:
            response = chain.invoke({"results": results_text})
            return response.content
        except Exception as e:
            print(f"❌ Error extracting project info: {e}")
            return "Error extracting information"
    
    def classify_lead(self, project_info):
        """
        Classify and score the lead for Genotek's business
        
        Args:
            project_info (str): Extracted project information
            
        Returns:
            str: Classification and scoring
        """
        classification_prompt = ChatPromptTemplate.from_messages([
            ("system", CLASSIFICATION_SYSTEM_PROMPT),
            ("human", "Analyze this construction project for Genotek:\n\n{project}")
        ])
        
        chain = classification_prompt | self.llm
        
        try:
            response = chain.invoke({"project": project_info})
            return response.content
        except Exception as e:
            print(f"❌ Error classifying lead: {e}")
            return "Error classifying lead"
    
    def generate_outreach_email(self, project_info, classification):
        """
        Generate personalized outreach email
        
        Args:
            project_info (str): Project information
            classification (str): Lead classification
            
        Returns:
            str: Generated email
        """
        email_prompt = ChatPromptTemplate.from_messages([
            ("system", EMAIL_GENERATION_SYSTEM_PROMPT),
            ("human", """Generate a professional outreach email for this project:

PROJECT INFO:
{project}

ANALYSIS:
{analysis}

Write a compelling email that highlights Genotek's relevant materials and expertise.""")
        ])
        
        chain = email_prompt | self.llm
        
        try:
            response = chain.invoke({
                "project": project_info,
                "analysis": classification
            })
            return response.content
        except Exception as e:
            print(f"❌ Error generating email: {e}")
            return "Error generating email"
    
    def parse_extracted_info(self, project_info):
        """
        Parse the extracted project information into structured data
        Enhanced to extract ALL available fields
        
        Args:
            project_info (str): Raw extracted information
            
        Returns:
            dict: Structured lead data
        """
        def extract_field(field_name, text, default="Not found"):
            """Helper to extract field value"""
            pattern = rf"{field_name}:\s*(.+?)(?:\n|$)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Don't return if it says "not found" or similar
                if value and "not found" not in value.lower() and "not available" not in value.lower() and "n/a" not in value.lower():
                    return value
            return default
        
        # Extract all fields
        lead_data = {
            "projectName": extract_field("Project Name", project_info, "Unknown Project"),
            "company": extract_field("Company", project_info, "Unknown Company"),
            "location": extract_field("Location", project_info, "Unknown Location"),
            "projectType": extract_field("Project Type", project_info, "Commercial"),
            "status": extract_field("Status", project_info, "New"),
            "budget": extract_field("Budget", project_info, "Not specified"),
            "timeline": f"{extract_field('Start Date', project_info, 'TBD')} - {extract_field('Completion Date', project_info, 'TBD')}",
            "source": "AI Discovery",
            "email": extract_field("Email", project_info, "contact@example.com"),
            "phone": extract_field("Phone", project_info, "Not available"),
            "website": extract_field("Website", project_info, "Not available"),
            "description": extract_field("Description", project_info, project_info[:300] + "..."),
            "aiConfidence": 85,
            "foundDate": datetime.now().strftime("%Y-%m-%d"),
            "keyContacts": [],
            "tags": ["AI Generated", "New Lead"],
            "materialNeeds": [],
            "projectSize": extract_field("Project Size", project_info, "Not specified"),
            "contractor": extract_field("Contractor", project_info, "Not specified"),
            "architect": extract_field("Architect", project_info, "Not specified"),
            "startDate": extract_field("Start Date", project_info, "Not specified"),
            "completionDate": extract_field("Completion Date", project_info, "Not specified")
        }
        
        # Extract key contacts
        project_manager = extract_field("Project Manager", project_info, None)
        key_contact = extract_field("Key Contact", project_info, None)
        
        if project_manager and project_manager != "Not found":
            lead_data["keyContacts"].append(project_manager)
        if key_contact and key_contact != "Not found":
            lead_data["keyContacts"].append(key_contact)
        
        if not lead_data["keyContacts"]:
            lead_data["keyContacts"] = ["Contact information pending"]
        
        # Extract material needs
        material_needs = extract_field("Material Needs", project_info, None)
        if material_needs and material_needs != "Not found":
            lead_data["materialNeeds"] = [material_needs]
        else:
            lead_data["materialNeeds"] = ["To be determined"]
        
        # Extract key features as tags
        key_features = extract_field("Key Features", project_info, None)
        if key_features and key_features != "Not found":
            lead_data["tags"].append(key_features[:50])  # Add first 50 chars as tag
        
        return lead_data
    
    def parse_classification(self, classification):
        """
        Parse classification to extract confidence score
        
        Args:
            classification (str): Classification text
            
        Returns:
            int: Confidence score
        """
        # Try to extract relevance score
        match = re.search(r"(?:Relevance Score|Score):\s*(\d+)", classification)
        if match:
            return int(match.group(1))
        return 85  # Default score
    
    def process_single_query(self, query):
        """
        Process a single search query through the entire pipeline
        
        Args:
            query (str): Search query
        """
        print(f"\n{'='*80}")
        print(f"🔍 SEARCHING: {query}")
        print(f"{'='*80}\n")
        
        # Step 1: Search with SerperDev
        print("📡 Step 1: Searching with SerperDev...")
        search_results = self.search_with_serper(query)
        
        if not search_results:
            print("❌ No search results found")
            return
        
        num_results = len(search_results.get('organic', []))
        print(f"✅ Found {num_results} results")
        
        if num_results > 0:
            top_result = search_results['organic'][0]
            print(f"🎯 Focusing on TOP result: {top_result.get('title', 'N/A')[:80]}...")
            print(f"🔗 URL: {top_result.get('link', 'N/A')}")
        
        # Step 2: Extract project information
        print("\n🤖 Step 2: Extracting project information with AI...")
        project_info = self.extract_project_info(search_results)
        print("\n📋 EXTRACTED PROJECT INFO:")
        print("-" * 80)
        print(project_info)
        
        # Step 3: Classify and score the lead
        print("\n🎯 Step 3: Classifying lead for Genotek...")
        classification = self.classify_lead(project_info)
        print("\n📊 LEAD CLASSIFICATION:")
        print("-" * 80)
        print(classification)
        
        # Step 4: Generate outreach email
        print("\n✉️ Step 4: Generating personalized outreach email...")
        email = self.generate_outreach_email(project_info, classification)
        print("\n📧 GENERATED EMAIL:")
        print("-" * 80)
        print(email)
        print("-" * 80)
        
        # Step 5: Parse and store in memory
        print("\n💾 Step 5: Storing lead data...")
        lead_data = self.parse_extracted_info(project_info)
        lead_data["aiConfidence"] = self.parse_classification(classification)
        
        # Store email for later use
        lead_data["generatedEmail"] = email
        
        # Store in memory only
        self.generated_leads.append(lead_data)
        print(f"✅ Lead stored in memory (Total: {len(self.generated_leads)})")
    
    def run_lead_generation(self, num_queries=3):
        """
        Run the complete lead generation process
        
        Args:
            num_queries (int): Number of search queries to process
        """
        print("\n" + "="*80)
        print("🚀 GENOTEK AI LEAD GENERATION SYSTEM")
        print("="*80)
        print(f"📍 Company: Bijon Trading Private Limited (Genotek)")
        print(f"🎯 Focus: Specialized materials for commercial construction")
        print(f"🔢 Processing {num_queries} search queries")
        print("="*80)
        
        # Process queries
        for i, query in enumerate(SEARCH_QUERIES[:num_queries], 1):
            self.process_single_query(query)
            
            if i < num_queries:
                print("\n" + "🔄 Moving to next query...\n")
        
        print("\n" + "="*80)
        print("✅ LEAD GENERATION COMPLETE")
        print("="*80)
        print(f"📊 Total leads generated: {len(self.generated_leads)}")
        print("="*80)
        
        # Print summary of all leads
        if self.generated_leads:
            print("\n📋 GENERATED LEADS SUMMARY:")
            print("-" * 80)
            for idx, lead in enumerate(self.generated_leads, 1):
                print(f"\n{idx}. {lead['projectName']}")
                print(f"   Company: {lead['company']}")
                print(f"   Location: {lead['location']}")
                print(f"   Budget: {lead['budget']}")
                print(f"   Email: {lead['email']}")
                print(f"   Phone: {lead['phone']}")
                print(f"   AI Confidence: {lead['aiConfidence']}%")
            print("-" * 80)


def main():
    """Main function to run the lead generator"""
    # Initialize the lead generator
    generator = GenotekLeadGenerator()
    
    # Run lead generation (process 2 queries for demo)
    generator.run_lead_generation(num_queries=2)


if __name__ == "__main__":
    main()
