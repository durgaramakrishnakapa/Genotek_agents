"""
Final Validation Agent for Shopping Mall Construction Projects
Deep research and validation agent that thoroughly investigates each project
"""

import sys
import os
import json
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
spec = importlib.util.spec_from_file_location("shopping_malls_web_tool_validator", web_tool_path)
web_tool_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_tool_module)
ShoppingMallWebTool = web_tool_module.ShoppingMallWebTool

class FinalValidationAgent:
    """
    Powerful validation agent that deeply researches construction projects
    Uses multiple searches and LLM analysis to validate and enrich data
    """
    
    def __init__(self):
        self.name = "Final Validation Agent"
        self.specialty = "Deep Project Research & Validation"
        self.web_tool = ShoppingMallWebTool()
        
        # Initialize LLM
        from config import GROQ_API_KEY, LLM_MODEL
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=0.1  # Very low for accuracy
        )
        
        print(f"\n{'='*80}")
        print(f"🔍 {self.name} INITIALIZED")
        print(f"{'='*80}")
        print(f"🎯 Mission: Deep research and validation of construction projects")
        print(f"📅 Year: 2026 - Validating FUTURE/ONGOING projects only")
        print(f"🔬 Capability: Multi-source verification and data enrichment")
        print(f"❌ Excluding: Projects completed in 2024-2025")
        print(f"{'='*80}\n")
    
    def load_initial_data(self):
        """Load projects from initial_data.json"""
        input_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            projects = data.get('projects', [])
            print(f"📂 Loaded {len(projects)} projects from initial_data.json")
            return projects
        except Exception as e:
            print(f"❌ Error loading initial_data.json: {e}")
            return []
    
    def deep_research_project(self, project):
        """
        Perform deep research on a single project using multiple searches
        
        Args:
            project (dict): Project data from initial_data.json
            
        Returns:
            dict: Comprehensive validated project data
        """
        project_id = project.get('id', 'UNKNOWN')
        raw_data = project.get('raw_data', {})
        project_title = raw_data.get('title', 'Unknown Project')
        
        print(f"\n{'='*80}")
        print(f"🔬 DEEP RESEARCH: {project_id}")
        print(f"{'='*80}")
        print(f"📋 Project: {project_title}")
        print(f"{'='*80}\n")
        
        # Step 1: Extract project name for targeted search
        project_name = self.extract_project_name(raw_data)
        print(f"✅ Identified Project Name: {project_name}\n")
        
        # Step 2: Multiple targeted searches
        search_results = self.perform_multiple_searches(project_name, project_title)
        
        # Step 3: Deep analysis with LLM
        validated_data = self.deep_analysis(project_name, search_results, raw_data)
        
        # Step 4: Verify construction status
        status_verification = self.verify_construction_status(validated_data, search_results)
        
        # Step 5: Find builder/contractor information
        builder_info = self.find_builder_info(project_name, search_results)
        
        # Step 6: ITERATIVE DEEP SEARCH - Find missing information (up to 2 attempts)
        validated_data, builder_info = self.iterative_missing_data_search(
            project_name, validated_data, builder_info, max_attempts=2
        )
        
        # Step 7: Compile final validated data
        final_data = self.compile_final_data(
            project_id,
            project_name,
            validated_data,
            status_verification,
            builder_info,
            search_results
        )
        
        return final_data
    
    def extract_project_name(self, raw_data):
        """Extract the actual project name from raw data using LLM"""
        print("🔍 STEP 1: Extracting Project Name...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract the EXACT shopping mall project name from the search result.
            Return ONLY the project name, nothing else.
            If multiple projects mentioned, return the MAIN one."""),
            ("human", "Title: {title}\nSnippet: {snippet}\n\nProject name:")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "title": raw_data.get('title', ''),
            "snippet": raw_data.get('snippet', '')
        })
        
        return response.content.strip()
    
    def perform_multiple_searches(self, project_name, project_title):
        """
        Perform multiple targeted searches about the project
        
        Args:
            project_name (str): Extracted project name
            project_title (str): Original title
            
        Returns:
            dict: Aggregated search results from multiple queries
        """
        print(f"🌐 STEP 2: Performing Multiple Targeted Searches...")
        print("-" * 80)
        
        # Create targeted search queries (2026 focus)
        search_queries = [
            f'"{project_name}" shopping mall construction 2026 2027',
            f'"{project_name}" developer builder contractor under construction',
            f'"{project_name}" construction status completion date 2026 2027',
            f'"{project_name}" location address contact information',
            f'"{project_name}" budget investment cost planned'
        ]
        
        all_results = {
            'general': [],
            'builder': [],
            'status': [],
            'location': [],
            'financial': []
        }
        
        categories = ['general', 'builder', 'status', 'location', 'financial']
        
        for idx, query in enumerate(search_queries):
            print(f"\n   🔍 Search {idx+1}/5: {query[:60]}...")
            results = self.web_tool.search_single_query(query)
            
            if results and 'organic' in results:
                category = categories[idx]
                all_results[category] = results['organic'][:3]  # Top 3 per category
                print(f"   ✅ Found {len(results['organic'])} results")
            else:
                print(f"   ⚠️ No results")
        
        return all_results
    
    def deep_analysis(self, project_name, search_results, original_data):
        """
        Perform deep analysis using LLM on all search results
        
        Args:
            project_name (str): Project name
            search_results (dict): All search results
            original_data (dict): Original raw data
            
        Returns:
            dict: Comprehensive project information
        """
        print(f"\n🤖 STEP 3: Deep AI Analysis...")
        print("-" * 80)
        
        # Compile all search data
        compiled_data = self.compile_search_data(search_results)
        
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert construction project analyst.
            
Analyze ALL provided search results and extract COMPLETE information.

Extract and return JSON with these EXACT fields:
{{
  "project_name": "Exact official name",
  "location": {{
    "city": "City name",
    "state_province": "State/Province",
    "country": "Country",
    "full_address": "Complete address if available"
  }},
  "developer": {{
    "company_name": "Developer company",
    "contact_email": "Email if found",
    "contact_phone": "Phone if found",
    "website": "Website if found"
  }},
  "financial": {{
    "total_budget": "Amount with currency",
    "investment_source": "Source of funding",
    "estimated_cost": "Cost details"
  }},
  "timeline": {{
    "announcement_date": "When announced",
    "construction_start": "Start date (must be 2025 or later for ongoing projects)",
    "expected_completion": "Completion date (2026, 2027, 2028, etc.)",
    "current_phase": "Current construction phase in 2026"
  }},
  "specifications": {{
    "total_area": "Square footage/meters",
    "number_of_floors": "Floors",
    "number_of_stores": "Retail units",
    "parking_capacity": "Parking spaces",
    "anchor_tenants": ["List of major tenants"]
  }},
  "features": {{
    "key_features": ["List special features"],
    "sustainability": "Green/sustainable features",
    "technology": "Smart building features"
  }}
}}

Use "Not specified" only if truly not found in ANY search result."""),
            ("human", """Project Name: {project_name}

Original Data:
{original_data}

Search Results from Multiple Sources:
{compiled_data}

Perform deep analysis and extract ALL available information.""")
        ])
        
        chain = analysis_prompt | self.llm
        response = chain.invoke({
            "project_name": project_name,
            "original_data": json.dumps(original_data, indent=2),
            "compiled_data": compiled_data
        })
        
        try:
            # Parse JSON response
            content = response.content.strip()
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                data = json.loads(json_str)
                print("✅ Deep analysis completed")
                return data
            else:
                print("⚠️ Could not parse JSON, using raw response")
                return {"raw_analysis": content}
        except Exception as e:
            print(f"⚠️ Analysis error: {e}")
            return {"error": str(e), "raw": response.content}
    
    def compile_search_data(self, search_results):
        """Compile all search results into readable format"""
        compiled = ""
        
        for category, results in search_results.items():
            if results:
                compiled += f"\n\n=== {category.upper()} SEARCH RESULTS ===\n"
                for idx, result in enumerate(results, 1):
                    compiled += f"\n{idx}. {result.get('title', 'N/A')}\n"
                    compiled += f"   {result.get('snippet', 'N/A')}\n"
        
        return compiled
    
    def verify_construction_status(self, validated_data, search_results):
        """
        Verify if construction is actually ongoing or completed
        
        Args:
            validated_data (dict): Validated project data
            search_results (dict): Search results
            
        Returns:
            dict: Status verification
        """
        print(f"\n✔️ STEP 4: Verifying Construction Status...")
        print("-" * 80)
        
        status_prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the search results and determine the ACTUAL construction status.

IMPORTANT: We are in 2026. Projects completed in 2024-2025 should be marked as "Completed".
Focus on projects that are ONGOING in 2026 or PLANNED for 2026-2027.

Return JSON:
{{
  "status": "Under Construction in 2026" OR "Planned for 2026-2027" OR "Completed in 2024-2025" OR "Cancelled",
  "confidence": "High/Medium/Low",
  "evidence": "Key evidence from search results with dates",
  "last_update": "Most recent update date found",
  "completion_year": "Expected completion year (2026, 2027, 2028, etc.)"
}}"""),
            ("human", "Project data: {data}\n\nStatus search results: {status_results}\n\nDetermine actual status:")
        ])
        
        chain = status_prompt | self.llm
        response = chain.invoke({
            "data": json.dumps(validated_data, indent=2),
            "status_results": json.dumps(search_results.get('status', []), indent=2)
        })
        
        try:
            content = response.content.strip()
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                status = json.loads(content[start:end])
                print(f"✅ Status: {status.get('status', 'Unknown')} (Confidence: {status.get('confidence', 'Unknown')})")
                return status
            else:
                return {"status": "Unknown", "raw": content}
        except:
            return {"status": "Unknown", "error": "Parse failed"}
    
    def find_builder_info(self, project_name, search_results):
        """
        Find detailed builder/contractor information
        
        Args:
            project_name (str): Project name
            search_results (dict): Search results
            
        Returns:
            dict: Builder/contractor information
        """
        print(f"\n🏗️ STEP 5: Finding Builder/Contractor Information...")
        print("-" * 80)
        
        builder_prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract ALL information about builders, contractors, and construction companies.

Return JSON:
{{
  "main_contractor": {{
    "company_name": "Name",
    "role": "General contractor/Builder",
    "contact": "Contact info if found"
  }},
  "architect": {{
    "firm_name": "Architecture firm",
    "contact": "Contact if found"
  }},
  "other_contractors": [
    {{"company": "Name", "role": "Specialty"}}
  ],
  "construction_manager": "Company managing construction"
}}"""),
            ("human", "Project: {project_name}\n\nBuilder search results: {builder_results}\n\nExtract builder information:")
        ])
        
        chain = builder_prompt | self.llm
        response = chain.invoke({
            "project_name": project_name,
            "builder_results": json.dumps(search_results.get('builder', []), indent=2)
        })
        
        try:
            content = response.content.strip()
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                builder_info = json.loads(content[start:end])
                print(f"✅ Found builder: {builder_info.get('main_contractor', {}).get('company_name', 'Unknown')}")
                return builder_info
            else:
                return {"raw": content}
        except:
            return {"error": "Parse failed"}
    
    def iterative_missing_data_search(self, project_name, validated_data, builder_info, max_attempts=2):
        """
        FIELD-BY-FIELD validation: Each field gets 2 dedicated searches
        Process 8 fields simultaneously for efficiency
        
        Args:
            project_name (str): Project name
            validated_data (dict): Current validated data
            builder_info (dict): Current builder info
            max_attempts (int): Searches per field (default 2)
            
        Returns:
            tuple: (updated_validated_data, updated_builder_info)
        """
        print(f"\n🔄 STEP 6: FIELD-BY-FIELD DEEP VALIDATION")
        print("=" * 80)
        print(f"🎯 Strategy: 2 searches per field, 8 fields at a time")
        print(f"🔍 Each field independently verified")
        print("=" * 80)
        
        # Get all fields that need validation
        all_fields = self.get_all_fields_for_validation(validated_data, builder_info)
        
        print(f"\n📋 Total fields to validate: {len(all_fields)}")
        
        # Process fields in batches of 8
        batch_size = 8
        for batch_idx in range(0, len(all_fields), batch_size):
            batch = all_fields[batch_idx:batch_idx + batch_size]
            
            print(f"\n{'='*80}")
            print(f"📦 BATCH {batch_idx//batch_size + 1}: Processing {len(batch)} fields simultaneously")
            print(f"{'='*80}")
            
            # Process each field in the batch
            for field_info in batch:
                field_path = field_info['path']
                field_name = field_info['name']
                current_value = field_info['value']
                
                print(f"\n🔍 Field: {field_name}")
                print(f"   Path: {field_path}")
                print(f"   Current: {current_value}")
                
                # Perform 5 dedicated searches for this field
                field_value = self.validate_single_field(
                    project_name, 
                    field_name, 
                    field_path,
                    current_value,
                    searches_per_field=max_attempts
                )
                
                # Update the field if new value found
                if field_value and field_value not in ["Not specified", "Not found", "Unknown"]:
                    validated_data, builder_info = self.update_single_field(
                        validated_data, 
                        builder_info, 
                        field_path, 
                        field_value
                    )
                    print(f"   ✅ Updated: {field_value[:80]}")
                else:
                    print(f"   ⚠️ Still not found after 5 searches")
        
        print(f"\n{'='*80}")
        print(f"✅ FIELD-BY-FIELD VALIDATION COMPLETED")
        print(f"{'='*80}\n")
        
        return validated_data, builder_info
    
    def get_all_fields_for_validation(self, validated_data, builder_info):
        """
        Get ALL fields (including those with data) for validation
        Returns detailed field information for targeted searches
        
        Args:
            validated_data (dict): Validated data
            builder_info (dict): Builder info
            
        Returns:
            list: List of field dictionaries with path, name, value, category
        """
        fields = []
        
        def extract_fields(d, path="", category=""):
            for key, value in d.items():
                current_path = f"{path}.{key}" if path else key
                
                if isinstance(value, dict):
                    extract_fields(value, current_path, category or key)
                elif isinstance(value, list):
                    # Check if it's a missing list
                    if not value or (len(value) == 1 and value[0] in ["Not specified", "Not found"]):
                        fields.append({
                            'path': current_path,
                            'name': key,
                            'value': value,
                            'category': category,
                            'type': 'list',
                            'missing': True
                        })
                elif isinstance(value, str):
                    # Add field if missing OR if it needs verification
                    is_missing = value in ["Not specified", "Not found", "Unknown", ""]
                    fields.append({
                        'path': current_path,
                        'name': key,
                        'value': value,
                        'category': category,
                        'type': 'string',
                        'missing': is_missing
                    })
        
        extract_fields(validated_data, "project_details", "project")
        extract_fields(builder_info, "builder_contractor", "builder")
        
        # Prioritize missing fields first
        fields.sort(key=lambda x: (not x['missing'], x['path']))
        
        return fields
    
    def validate_single_field(self, project_name, field_name, field_path, current_value, searches_per_field=2):
        """
        Perform 2 dedicated searches for a SINGLE field
        
        Args:
            project_name (str): Project name
            field_name (str): Field name (e.g., "contact_email")
            field_path (str): Full path (e.g., "project_details.developer.contact_email")
            current_value: Current field value
            searches_per_field (int): Number of searches (default 2)
            
        Returns:
            str: Validated field value or None
        """
        print(f"      🔎 Performing {searches_per_field} dedicated searches...")
        
        # Create 2 highly targeted search queries for this specific field
        search_queries = self.create_field_specific_queries(project_name, field_name, field_path)
        
        all_results = []
        for idx, query in enumerate(search_queries[:searches_per_field], 1):
            results = self.web_tool.search_single_query(query)
            if results and 'organic' in results:
                all_results.extend(results['organic'][:2])  # Top 2 per search
                print(f"         Search {idx}: ✓ ({len(results['organic'])} results)")
        
        if not all_results:
            return None
        
        # Use LLM to extract ONLY this specific field from results
        extracted_value = self.extract_field_with_llm(
            project_name, 
            field_name, 
            field_path,
            all_results
        )
        
        return extracted_value
    
    def create_field_specific_queries(self, project_name, field_name, field_path):
        """
        Create 2 highly targeted search queries for a specific field
        
        Args:
            project_name (str): Project name
            field_name (str): Field name
            field_path (str): Full field path
            
        Returns:
            list: 2 targeted search queries
        """
        queries = []
        
        # Contact email queries
        if 'email' in field_name.lower():
            queries = [
                f'"{project_name}" contact email address',
                f'"{project_name}" developer email contact'
            ]
        
        # Phone number queries
        elif 'phone' in field_name.lower():
            queries = [
                f'"{project_name}" phone number contact',
                f'"{project_name}" developer phone'
            ]
        
        # Website queries
        elif 'website' in field_name.lower():
            queries = [
                f'"{project_name}" official website',
                f'"{project_name}" developer website URL'
            ]
        
        # Budget/cost queries
        elif 'budget' in field_name.lower() or 'cost' in field_name.lower():
            queries = [
                f'"{project_name}" construction budget cost',
                f'"{project_name}" total investment million'
            ]
        
        # Area/size queries
        elif 'area' in field_name.lower() or 'size' in field_name.lower():
            queries = [
                f'"{project_name}" square feet size',
                f'"{project_name}" total area square footage'
            ]
        
        # Contractor queries
        elif 'contractor' in field_name.lower():
            queries = [
                f'"{project_name}" general contractor',
                f'"{project_name}" construction company builder'
            ]
        
        # Architect queries
        elif 'architect' in field_name.lower():
            queries = [
                f'"{project_name}" architect design firm',
                f'"{project_name}" architectural firm'
            ]
        
        # Parking queries
        elif 'parking' in field_name.lower():
            queries = [
                f'"{project_name}" parking spaces capacity',
                f'"{project_name}" parking garage spots'
            ]
        
        # Anchor tenants queries
        elif 'tenant' in field_name.lower() or 'anchor' in field_name.lower():
            queries = [
                f'"{project_name}" anchor tenants stores',
                f'"{project_name}" major retailers tenants'
            ]
        
        # Sustainability queries
        elif 'sustainability' in field_name.lower() or 'green' in field_name.lower():
            queries = [
                f'"{project_name}" sustainable green features',
                f'"{project_name}" LEED certification green'
            ]
        
        # Technology queries
        elif 'technology' in field_name.lower():
            queries = [
                f'"{project_name}" smart building technology',
                f'"{project_name}" technology features'
            ]
        
        # Generic queries for other fields
        else:
            queries = [
                f'"{project_name}" {field_name.replace("_", " ")}',
                f'"{project_name}" details {field_name.replace("_", " ")}'
            ]
        
        return queries
    
    def extract_field_with_llm(self, project_name, field_name, field_path, search_results):
        """
        Use LLM to extract ONLY the specific field value from search results
        
        Args:
            project_name (str): Project name
            field_name (str): Field name
            field_path (str): Full field path
            search_results (list): Search results
            
        Returns:
            str: Extracted field value
        """
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a precise data extraction expert.

CRITICAL INSTRUCTIONS:
1. Extract ONLY the specific field requested
2. Return ONLY the factual value found in search results
3. If not found, return "Not specified"
4. Be precise and concise
5. No explanations, just the value

Examples:
- For email: "john@example.com"
- For phone: "+1-920-448-2800"
- For budget: "$35 million"
- For area: "9,000 square feet"
- For name: "John Smith"

Return ONLY the value, nothing else."""),
            ("human", """Project: {project_name}
Field to extract: {field_name}
Field path: {field_path}

Search Results:
{results}

Extract ONLY the {field_name} value:""")
        ])
        
        chain = extraction_prompt | self.llm
        
        try:
            response = chain.invoke({
                "project_name": project_name,
                "field_name": field_name,
                "field_path": field_path,
                "results": self.format_search_results(search_results[:10])
            })
            
            value = response.content.strip()
            
            # Clean up the response
            if value and value not in ["Not specified", "Not found", "Unknown", "N/A"]:
                return value
            
        except Exception as e:
            print(f"         ⚠️ Extraction error: {e}")
        
        return None
    
    def update_single_field(self, validated_data, builder_info, field_path, new_value):
        """
        Update a single field in the nested data structure
        
        Args:
            validated_data (dict): Project data
            builder_info (dict): Builder data
            field_path (str): Dot-separated path (e.g., "project_details.developer.contact_email")
            new_value: New value to set
            
        Returns:
            tuple: (updated_validated_data, updated_builder_info)
        """
        path_parts = field_path.split('.')
        
        # Determine which dict to update
        if path_parts[0] == "project_details":
            target = validated_data
            path_parts = path_parts[1:]  # Remove "project_details"
        elif path_parts[0] == "builder_contractor":
            target = builder_info
            path_parts = path_parts[1:]  # Remove "builder_contractor"
        else:
            return validated_data, builder_info
        
        # Navigate to the parent of the target field
        current = target
        for part in path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Update the final field
        final_key = path_parts[-1]
        current[final_key] = new_value
        
        return validated_data, builder_info
    
    def search_for_missing_fields(self, project_name, missing_fields):
        """
        Perform targeted searches for specific missing fields
        
        Args:
            project_name (str): Project name
            missing_fields (list): List of missing field paths
            
        Returns:
            dict: Search results organized by field type
        """
        print(f"\n🌐 Performing targeted searches for missing data...")
        
        # Group missing fields by category
        search_queries = []
        
        # Contact information searches
        if any('contact' in field.lower() or 'email' in field.lower() or 'phone' in field.lower() or 'website' in field.lower() for field in missing_fields):
            search_queries.extend([
                f'"{project_name}" developer contact email phone',
                f'"{project_name}" Allouez Development Group contact information',
                f'"{project_name}" project manager contact details'
            ])
        
        # Financial information searches
        if any('budget' in field.lower() or 'cost' in field.lower() or 'investment' in field.lower() for field in missing_fields):
            search_queries.extend([
                f'"{project_name}" construction budget cost investment',
                f'"{project_name}" project value total cost million'
            ])
        
        # Specifications searches
        if any('area' in field.lower() or 'size' in field.lower() or 'square' in field.lower() for field in missing_fields):
            search_queries.extend([
                f'"{project_name}" square feet size area specifications',
                f'"{project_name}" retail space size square footage'
            ])
        
        # Contractor/Builder searches
        if any('contractor' in field.lower() or 'architect' in field.lower() for field in missing_fields):
            search_queries.extend([
                f'"{project_name}" general contractor construction company',
                f'"{project_name}" architect design firm',
                f'"Allouez Development Group" contact phone email website'
            ])
        
        # Features and tenants
        if any('tenant' in field.lower() or 'feature' in field.lower() or 'sustainability' in field.lower() for field in missing_fields):
            search_queries.extend([
                f'"{project_name}" anchor tenants stores retailers',
                f'"{project_name}" features amenities sustainability green'
            ])
        
        # Perform searches
        all_results = []
        for idx, query in enumerate(search_queries[:10], 1):  # Limit to 10 searches
            print(f"   🔍 Search {idx}: {query[:60]}...")
            results = self.web_tool.search_single_query(query)
            if results and 'organic' in results:
                all_results.extend(results['organic'][:3])  # Top 3 per query
                print(f"      ✅ Found {len(results['organic'])} results")
        
        return all_results
    
    def update_with_new_findings(self, validated_data, builder_info, search_results, project_name):
        """
        Use LLM to extract missing information from new search results
        
        Args:
            validated_data (dict): Current validated data
            builder_info (dict): Current builder info
            search_results (list): New search results
            project_name (str): Project name
            
        Returns:
            tuple: (updated_validated_data, updated_builder_info)
        """
        print(f"\n🤖 Analyzing new search results with AI...")
        
        update_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting missing construction project information.

CRITICAL INSTRUCTIONS:
1. Review the CURRENT DATA and identify fields with "Not specified", "Not found", or "Unknown"
2. Search through NEW SEARCH RESULTS to find the missing information
3. Extract ONLY factual information found in the search results
4. Return COMPLETE JSON with ALL fields (keep existing data, update only missing fields)
5. If information is still not found, keep "Not specified"

Focus on finding:
- Contact information (emails, phones, websites)
- Budget/cost/investment amounts
- Project specifications (size, area, square footage)
- Contractor/architect names and contacts
- Anchor tenants and features
- Any other missing details

Return the COMPLETE updated JSON structure with all fields."""),
            ("human", """Project: {project_name}

CURRENT DATA (with missing fields):
{current_data}

CURRENT BUILDER INFO (with missing fields):
{current_builder}

NEW SEARCH RESULTS:
{new_results}

Extract missing information and return COMPLETE updated JSON.""")
        ])
        
        chain = update_prompt | self.llm
        response = chain.invoke({
            "project_name": project_name,
            "current_data": json.dumps(validated_data, indent=2),
            "current_builder": json.dumps(builder_info, indent=2),
            "new_results": self.format_search_results(search_results)
        })
        
        try:
            content = response.content.strip()
            
            # Try to extract updated validated_data
            if '"project_name"' in content and '"location"' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                updated_data = json.loads(json_str)
                
                # Merge with existing data (keep structure)
                validated_data = self.merge_data(validated_data, updated_data)
                print(f"   ✅ Updated project details")
            
            # Try to extract updated builder_info
            if '"main_contractor"' in content or '"architect"' in content:
                # Look for builder info in response
                if 'builder' in content.lower() or 'contractor' in content.lower():
                    # Extract builder section if present
                    builder_start = content.find('"main_contractor"')
                    if builder_start > 0:
                        # Find the enclosing object
                        brace_count = 0
                        for i in range(builder_start - 1, -1, -1):
                            if content[i] == '{':
                                builder_start = i
                                break
                        
                        for i in range(builder_start, len(content)):
                            if content[i] == '{':
                                brace_count += 1
                            elif content[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    builder_json = content[builder_start:i+1]
                                    updated_builder = json.loads(builder_json)
                                    builder_info = self.merge_data(builder_info, updated_builder)
                                    print(f"   ✅ Updated builder information")
                                    break
            
        except Exception as e:
            print(f"   ⚠️ Update error: {e}")
        
        return validated_data, builder_info
    
    def format_search_results(self, results):
        """Format search results for LLM analysis"""
        formatted = ""
        for idx, result in enumerate(results[:15], 1):  # Top 15 results
            formatted += f"\n{idx}. {result.get('title', 'N/A')}\n"
            formatted += f"   URL: {result.get('link', 'N/A')}\n"
            formatted += f"   {result.get('snippet', 'N/A')}\n"
        return formatted
    
    def merge_data(self, original, updates):
        """
        Merge updated data with original, replacing 'Not specified' values
        
        Args:
            original (dict): Original data
            updates (dict): Updated data
            
        Returns:
            dict: Merged data
        """
        if not isinstance(original, dict) or not isinstance(updates, dict):
            return original
        
        merged = original.copy()
        
        for key, value in updates.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key] = self.merge_data(merged[key], value)
                elif isinstance(value, str):
                    # Replace if original was "Not specified" and new value is not
                    if merged[key] in ["Not specified", "Not found", "Unknown", ""] and value not in ["Not specified", "Not found", "Unknown", ""]:
                        merged[key] = value
                elif isinstance(value, list):
                    # Replace if original was empty or ["Not specified"]
                    if not merged[key] or merged[key] == ["Not specified"] or merged[key] == ["Not found"]:
                        if value and value != ["Not specified"] and value != ["Not found"]:
                            merged[key] = value
                else:
                    merged[key] = value
            else:
                merged[key] = value
        
        return merged
    
    def compile_final_data(self, project_id, project_name, validated_data, 
                          status_verification, builder_info, search_results):
        """
        Compile all data into final structured format
        
        Args:
            project_id (str): Project ID
            project_name (str): Project name
            validated_data (dict): Validated data
            status_verification (dict): Status info
            builder_info (dict): Builder info
            search_results (dict): All search results
            
        Returns:
            dict: Final compiled data
        """
        print(f"\n📦 STEP 7: Compiling Final Validated Data...")
        print("-" * 80)
        
        final_data = {
            "project_id": project_id,
            "project_name": project_name,
            "validation_timestamp": datetime.now().isoformat(),
            "validation_agent": self.name,
            "data_quality": "VALIDATED",
            
            "project_details": validated_data,
            "construction_status": status_verification,
            "builder_contractor": builder_info,
            
            "sources": {
                "total_sources_checked": sum(len(v) for v in search_results.values()),
                "search_categories": list(search_results.keys())
            },
            
            "genotek_relevance": {
                "material_opportunities": self.identify_material_opportunities(validated_data),
                "priority_level": self.calculate_priority(validated_data, status_verification),
                "recommended_action": self.recommend_action(status_verification)
            }
        }
        
        print("✅ Final data compiled successfully")
        return final_data
    
    def identify_material_opportunities(self, validated_data):
        """Identify Genotek material opportunities"""
        opportunities = []
        
        # Check project type and size
        specs = validated_data.get('specifications', {})
        if specs.get('total_area'):
            opportunities.append("Large-scale flooring materials")
        if specs.get('number_of_floors'):
            opportunities.append("Multi-level construction materials")
        
        # Check features
        features = validated_data.get('features', {})
        if 'sustainability' in str(features):
            opportunities.append("Sustainable/eco-friendly materials")
        if 'technology' in str(features):
            opportunities.append("Smart building materials")
        
        return opportunities if opportunities else ["General commercial construction materials"]
    
    def calculate_priority(self, validated_data, status_verification):
        """Calculate priority level for Genotek (2026 context)"""
        status = status_verification.get('status', '')
        confidence = status_verification.get('confidence', '')
        completion_year = status_verification.get('completion_year', '')
        
        # High priority: Under construction in 2026 or planned for 2026-2027
        if ("Under Construction in 2026" in status or "Planned for 2026-2027" in status) and confidence == "High":
            return "HIGH"
        elif "Planned" in status or "2027" in completion_year or "2028" in completion_year:
            return "MEDIUM"
        elif "Completed" in status:
            return "SKIP - Already completed"
        else:
            return "LOW"
    
    def recommend_action(self, status_verification):
        """Recommend action for Genotek (2026 context)"""
        status = status_verification.get('status', '')
        completion_year = status_verification.get('completion_year', '')
        
        if "Under Construction in 2026" in status:
            return "IMMEDIATE OUTREACH - Project actively building in 2026"
        elif "Planned for 2026-2027" in status:
            return "EARLY ENGAGEMENT - Secure materials contract for upcoming project"
        elif "Completed in 2024-2025" in status or "Completed" in status:
            return "SKIP - Project already completed before 2026"
        else:
            return "RESEARCH MORE - Status unclear, verify timeline"
    
    def save_final_data(self, final_data):
        """Save final validated data to final_data.json"""
        output_path = os.path.join(os.path.dirname(__file__), "final_data.json")
        
        # Load existing data if any
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                if 'validated_projects' not in existing:
                    existing = {"validated_projects": []}
        except:
            existing = {"validated_projects": []}
        
        # Check if project already exists (by project_id)
        project_id = final_data.get('project_id')
        project_exists = False
        
        for idx, project in enumerate(existing['validated_projects']):
            if project.get('project_id') == project_id:
                # Update existing project
                existing['validated_projects'][idx] = final_data
                project_exists = True
                print(f"   ♻️ Updated existing project: {project_id}")
                break
        
        # Add new project if it doesn't exist
        if not project_exists:
            existing['validated_projects'].append(final_data)
            print(f"   ➕ Added new project: {project_id}")
        
        existing['last_updated'] = datetime.now().isoformat()
        existing['total_validated'] = len(existing['validated_projects'])
        
        # Save
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Final validated data saved to final_data.json")
        print(f"📁 Location: {output_path}")
    
    def run(self):
        """Run the final validation agent"""
        print(f"\n{'🚀 STARTING FINAL VALIDATION AGENT':^80}")
        print("=" * 80)
        
        # Load projects from initial_data.json
        projects = self.load_initial_data()
        
        if not projects:
            print("\n❌ No projects found in initial_data.json")
            return
        
        # Process ONLY the FIRST project
        print(f"\n🎯 Processing FIRST project only (1/{len(projects)})")
        first_project = projects[0]
        
        # Deep research and validation
        final_data = self.deep_research_project(first_project)
        
        # Save to final_data.json
        self.save_final_data(final_data)
        
        # Final summary
        print(f"\n{'='*80}")
        print(f"✅ FINAL VALIDATION COMPLETED")
        print(f"{'='*80}")
        print(f"📊 Project ID: {final_data.get('project_id', 'N/A')}")
        print(f"📋 Project: {final_data.get('project_name', 'N/A')}")
        print(f"🏗️ Status: {final_data.get('construction_status', {}).get('status', 'N/A')}")
        print(f"🎯 Priority: {final_data.get('genotek_relevance', {}).get('priority_level', 'N/A')}")
        print(f"💾 Saved to: final_data.json")
        print(f"{'='*80}\n")
        
        return final_data

if __name__ == "__main__":
    agent = FinalValidationAgent()
    agent.run()
