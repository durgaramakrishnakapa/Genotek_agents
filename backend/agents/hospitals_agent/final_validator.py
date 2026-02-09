"""
Hospital Final Validation Agent - Optimized
Deep research and validation with 2 searches per field, 8 fields per batch
"""

import sys
import os
import json
from datetime import datetime

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, '../..'))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Import web_tool
import importlib.util
spec = importlib.util.spec_from_file_location("hospitals_web_tool_validator", os.path.join(current_dir, 'web_tool.py'))
web_tool_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_tool_module)
HospitalWebTool = web_tool_module.HospitalWebTool

class FinalValidationAgent:
    """Optimized validation agent for hospital projects"""
    
    def __init__(self):
        self.name = "Hospital Final Validation Agent"
        self.web_tool = HospitalWebTool()
        
        from config import GROQ_API_KEY, LLM_MODEL
        self.llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.1)
        
        print(f"\n🔬 {self.name} - Deep research with 2 searches per field\n")
    
    def load_projects(self):
        """Load projects from initial_data.json"""
        try:
            with open(os.path.join(os.path.dirname(__file__), "initial_data.json"), 'r') as f:
                data = json.load(f)
            return data.get('projects', [])
        except:
            return []
    
    def extract_project_name(self, raw_data):
        """Extract project name using LLM"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract the EXACT hospital project name. Return ONLY the name."),
            ("human", "Title: {title}\nSnippet: {snippet}\n\nProject name:")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                title=raw_data.get('title', ''),
                snippet=raw_data.get('snippet', '')
            ))
            return response.content.strip()
        except:
            return raw_data.get('title', 'Unknown Project')
    
    def search_multiple(self, project_name):
        """Perform 5 targeted searches"""
        queries = [
            f'"{project_name}" hospital construction 2026 2027',
            f'"{project_name}" developer builder contractor',
            f'"{project_name}" construction status completion',
            f'"{project_name}" location address contact',
            f'"{project_name}" budget investment cost'
        ]
        
        results = {'general': [], 'builder': [], 'status': [], 'location': [], 'financial': []}
        categories = ['general', 'builder', 'status', 'location', 'financial']
        
        for i, query in enumerate(queries):
            search_results = self.web_tool.search_single_query(query)
            if search_results and 'organic' in search_results:
                results[categories[i]] = search_results['organic'][:3]
        
        return results
    
    def deep_analysis(self, project_name, search_results):
        """Analyze all search results with LLM"""
        compiled_data = ""
        for category, results in search_results.items():
            if results:
                compiled_data += f"\n=== {category.upper()} ===\n"
                for r in results:
                    compiled_data += f"{r.get('title', '')}\n{r.get('snippet', '')}\n\n"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract complete hospital project information from search results.

Return ONLY valid JSON with these EXACT fields (no extra text before or after):
{
  "project_name": "Official hospital name",
  "location": {
    "city": "City",
    "state_province": "State/Province", 
    "country": "Country",
    "full_address": "Complete address if available"
  },
  "developer": {
    "company_name": "Developer company",
    "contact_email": "Email if found",
    "contact_phone": "Phone if found",
    "website": "Website if found"
  },
  "financial": {
    "total_budget": "Amount with currency",
    "investment_source": "Funding source",
    "estimated_cost": "Cost details"
  },
  "timeline": {
    "construction_start": "Start date",
    "expected_completion": "Completion date (2026+)",
    "current_phase": "Current phase in 2026"
  },
  "specifications": {
    "total_area": "Square footage",
    "number_of_floors": "Floors",
    "bed_capacity": "Number of beds",
    "departments": ["List of departments"]
  },
  "features": {
    "key_features": ["Special features"],
    "sustainability": "Green features",
    "technology": "Smart building tech"
  }
}

Use "Not specified" if not found. Return ONLY the JSON object."""),
            ("human", "Project: {name}\n\nSearch Results:\n{data}\n\nExtract complete information:")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                name=project_name,
                data=compiled_data
            ))
            
            content = response.content.strip()
            print(f"   🔍 Analysis response length: {len(content)} chars")
            
            # Clean the content - remove any text before first { and after last }
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                
                # Try to parse JSON
                data = json.loads(json_str)
                location = data.get('location', {})
                city = location.get('city', 'N/A')
                country = location.get('country', 'N/A')
                print(f"   ✅ Extracted location: {city}, {country}")
                return data
            else:
                print(f"   ⚠️ No JSON brackets found in response")
                
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON parsing error: {str(e)[:100]}")
        except Exception as e:
            print(f"   ⚠️ Analysis error: {str(e)[:100]}")
        
        return {}
    
    def verify_status(self, validated_data, search_results):
        """Verify construction status"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Determine construction status. We are in 2026.

Return JSON:
{
  "status": "Under Construction in 2026" OR "Planned for 2026-2027" OR "Completed in 2024-2025",
  "confidence": "High/Medium/Low",
  "evidence": "Key evidence with dates",
  "completion_year": "Expected year (2026, 2027, 2028)"
}"""),
            ("human", "Project: {data}\n\nStatus results: {status}\n\nDetermine status:")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                data=json.dumps(validated_data, indent=2),
                status=json.dumps(search_results.get('status', []), indent=2)
            ))
            
            content = response.content.strip()
            if '{' in content:
                start, end = content.find('{'), content.rfind('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return {"status": "Unknown", "confidence": "Low"}
    
    def find_builder_info(self, search_results):
        """Find builder/contractor information"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract builder/contractor information.

Return JSON:
{
  "main_contractor": {
    "company_name": "Name",
    "role": "General contractor/Builder",
    "contact": "Contact if found"
  },
  "architect": {
    "firm_name": "Architecture firm",
    "contact": "Contact if found"
  },
  "other_contractors": [{"company": "Name", "role": "Specialty"}],
  "construction_manager": "Company managing construction"
}"""),
            ("human", "Builder search results: {results}\n\nExtract builder info:")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                results=json.dumps(search_results.get('builder', []), indent=2)
            ))
            
            content = response.content.strip()
            if '{' in content:
                start, end = content.find('{'), content.rfind('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return {"main_contractor": {"company_name": "Not found"}}
    
    def find_contractor_contacts(self, builder_info):
        """Find detailed contact information for the contractor with persistent search (min 2, max 3 attempts)"""
        contractor_name = builder_info.get('main_contractor', {}).get('company_name', '')
        if not contractor_name or contractor_name in ["Not found", "Not specified"]:
            return builder_info
        
        print(f"📞 Searching contact details for contractor: {contractor_name}")
        
        # Targeted searches for contractor contact information
        contact_queries = [
            f'"{contractor_name}" construction company contact email phone',
            f'"{contractor_name}" contractor contact details website address',
            f'"{contractor_name}" construction contact information phone email'
        ]
        
        all_contact_results = []
        attempts_made = 0
        min_attempts = 2
        max_attempts = 3
        found_contacts = False
        
        while attempts_made < max_attempts and (not found_contacts or attempts_made < min_attempts):
            query = contact_queries[attempts_made] if attempts_made < len(contact_queries) else contact_queries[-1]
            print(f"   🔍 Contact search attempt {attempts_made + 1}: {query[:50]}...")
            
            results = self.web_tool.search_single_query(query)
            attempts_made += 1
            
            if results and 'organic' in results:
                all_contact_results.extend(results['organic'][:3])  # Top 3 per attempt
                print(f"   ✅ Found {len(results['organic'])} results")
                
                # Try to extract contact details from current results
                if len(all_contact_results) >= 3:  # Have enough data to try extraction
                    contact_prompt = f"""Extract contact information for "{contractor_name}" construction company from search results.

Search Results:
{self.format_contact_results(all_contact_results[-6:])}

Return JSON:
{{
  "contact_email": "email address if found",
  "contact_phone": "phone number if found", 
  "website": "website URL if found",
  "address": "business address if found"
}}

Use "Not found" if information not available."""

                    try:
                        response = self.llm.invoke([("human", contact_prompt)])
                        content = response.content.strip()
                        
                        # Clean JSON extraction
                        if '{' in content and '}' in content:
                            start, end = content.find('{'), content.rfind('}') + 1
                            json_str = content[start:end]
                            contact_data = json.loads(json_str)
                            
                            # Check if we found meaningful contact data
                            meaningful_contacts = 0
                            main_contractor = builder_info.get('main_contractor', {})
                            
                            for key, value in contact_data.items():
                                if value and value not in ["Not found", "Not specified", "Unknown"]:
                                    main_contractor[key] = value
                                    meaningful_contacts += 1
                                    print(f"   ✅ Found {key}: {value[:50]}...")
                            
                            if meaningful_contacts >= 1:  # Found at least one contact detail
                                builder_info['main_contractor'] = main_contractor
                                found_contacts = True
                                break
                                
                    except Exception as e:
                        print(f"   ⚠️ Contact extraction error: {e}")
            else:
                print(f"   ⚠️ No results on attempt {attempts_made}")
        
        if not found_contacts:
            print(f"   ⚠️ Contact details not found after {attempts_made} attempts")
        
        return builder_info
    
    def format_contact_results(self, results):
        """Format search results for contact extraction"""
        formatted = ""
        for i, result in enumerate(results[:5], 1):
            formatted += f"\n{i}. {result.get('title', 'N/A')}\n"
            formatted += f"   {result.get('snippet', 'N/A')}\n"
        return formatted
    
    def find_project_location(self, project_name, validated_data):
        """Find specific location information for the hospital project with persistent search (min 2, max 3 attempts)"""
        location_queries = [
            f'"{project_name}" hospital location address city',
            f'"{project_name}" construction site location where built',
            f'"{project_name}" hospital address location construction project'
        ]
        
        print(f"📍 Searching specific location for: {project_name}")
        
        all_location_results = []
        attempts_made = 0
        min_attempts = 2
        max_attempts = 3
        found_location = False
        
        while attempts_made < max_attempts and (not found_location or attempts_made < min_attempts):
            query = location_queries[attempts_made] if attempts_made < len(location_queries) else location_queries[-1]
            print(f"   🔍 Location search attempt {attempts_made + 1}: {query[:50]}...")
            
            results = self.web_tool.search_single_query(query)
            attempts_made += 1
            
            if results and 'organic' in results:
                all_location_results.extend(results['organic'][:3])  # Top 3 per attempt
                print(f"   ✅ Found {len(results['organic'])} results")
                
                # Try to extract location from current results
                if len(all_location_results) >= 3:  # Have enough data to try extraction
                    location_prompt = f"""Extract the EXACT location where "{project_name}" hospital is being built.

Search Results:
{self.format_contact_results(all_location_results[-6:])}  

Return ONLY this JSON format:
{{
  "city": "City name",
  "state_province": "State/Province/Region",
  "country": "Country",
  "full_address": "Complete project address if available"
}}

Focus on WHERE the hospital construction is taking place. Use "Not specified" if not found."""

                    try:
                        response = self.llm.invoke([("human", location_prompt)])
                        content = response.content.strip()
                        
                        # Clean JSON extraction
                        if '{' in content and '}' in content:
                            start, end = content.find('{'), content.rfind('}') + 1
                            json_str = content[start:end]
                            location_data = json.loads(json_str)
                            
                            # Check if we found meaningful location data
                            meaningful_fields = 0
                            for key, value in location_data.items():
                                if value and value not in ["Not specified", "Unknown", "N/A"]:
                                    meaningful_fields += 1
                            
                            if meaningful_fields >= 2:  # At least city and country
                                validated_data['location'] = location_data
                                city = location_data.get('city', 'N/A')
                                country = location_data.get('country', 'N/A')
                                print(f"   ✅ Found location: {city}, {country}")
                                found_location = True
                                break
                        
                    except Exception as e:
                        print(f"   ⚠️ Location extraction error: {e}")
            else:
                print(f"   ⚠️ No results on attempt {attempts_made}")
        
        if not found_location:
            print(f"   ⚠️ Location not found after {attempts_made} attempts")
        
        return validated_data
    
    def validate_missing_fields(self, project_name, validated_data, builder_info):
        """Field-by-field validation with persistent search (min 2, max 3 attempts), 8 fields per batch"""
        print("🔄 Field-by-field validation (2 searches per field, 8 fields per batch)")
        
        # Get all missing fields
        missing_fields = []
        
        def extract_missing(d, path=""):
            for key, value in d.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    extract_missing(value, current_path)
                elif isinstance(value, str) and value in ["Not specified", "Not found", "Unknown", ""]:
                    missing_fields.append({'path': current_path, 'name': key, 'value': value})
        
        extract_missing(validated_data, "project_details")
        extract_missing(builder_info, "builder_contractor")
        
        # Add specific contractor contact fields if contractor is found
        contractor_name = builder_info.get('main_contractor', {}).get('company_name', '')
        if contractor_name and contractor_name not in ["Not specified", "Not found", "Unknown"]:
            # Add contractor contact fields for targeted search
            missing_fields.extend([
                {'path': 'builder_contractor.main_contractor.contact_email', 'name': 'contact_email', 'value': 'Not specified'},
                {'path': 'builder_contractor.main_contractor.contact_phone', 'name': 'contact_phone', 'value': 'Not specified'},
                {'path': 'builder_contractor.main_contractor.website', 'name': 'website', 'value': 'Not specified'},
                {'path': 'builder_contractor.main_contractor.address', 'name': 'address', 'value': 'Not specified'}
            ])
        
        print(f"📋 Found {len(missing_fields)} missing fields")
        
        # Process in batches of 8
        for i in range(0, len(missing_fields), 8):
            batch = missing_fields[i:i+8]
            print(f"\n📦 BATCH {i//8 + 1}: Processing {len(batch)} fields")
            
            for field in batch:
                field_name = field['name']
                print(f"🔍 {field_name}: ", end="")
                
                # Create targeted queries based on field type and contractor name
                if field_name in ['contact_email', 'contact_phone', 'website', 'address'] and contractor_name:
                    queries = [
                        f'"{contractor_name}" contact email phone website address',
                        f'"{contractor_name}" construction company contact details',
                        f'"{contractor_name}" contractor contact information'
                    ]
                else:
                    queries = [
                        f'"{project_name}" {field_name.replace("_", " ")}',
                        f'"{project_name}" hospital {field_name.replace("_", " ")}',
                        f'"{project_name}" construction {field_name.replace("_", " ")}'
                    ]
                
                # Persistent search - minimum 2, maximum 3 attempts
                found_value = None
                attempts_made = 0
                min_attempts = 2
                max_attempts = 3
                
                while attempts_made < max_attempts and (found_value is None or attempts_made < min_attempts):
                    query = queries[attempts_made] if attempts_made < len(queries) else queries[-1]
                    results = self.web_tool.search_single_query(query)
                    attempts_made += 1
                    
                    if results and 'organic' in results:
                        # Enhanced LLM extraction for contact details
                        for result_idx in range(min(2, len(results['organic']))):  # Try top 2 results
                            try:
                                snippet = results['organic'][result_idx].get('snippet', '')
                                title = results['organic'][result_idx].get('title', '')
                                combined_text = f"{title} {snippet}"
                                
                                if field_name == 'contact_email':
                                    extract_prompt = f"Extract ONLY the email address for {contractor_name} from: {combined_text}. Return only the email or 'Not found'."
                                elif field_name == 'contact_phone':
                                    extract_prompt = f"Extract ONLY the phone number for {contractor_name} from: {combined_text}. Return only the phone or 'Not found'."
                                elif field_name == 'website':
                                    extract_prompt = f"Extract ONLY the website URL for {contractor_name} from: {combined_text}. Return only the URL or 'Not found'."
                                elif field_name == 'address':
                                    extract_prompt = f"Extract ONLY the business address for {contractor_name} from: {combined_text}. Return only the address or 'Not found'."
                                elif field_name == 'company_name':
                                    extract_prompt = f"Extract ONLY the construction company or contractor name for {project_name} from: {combined_text}. Return only the company name or 'Not found'."
                                else:
                                    extract_prompt = f"Extract ONLY the {field_name.replace('_', ' ')} for {project_name} from: {combined_text}. Return only the value or 'Not found'."
                                
                                response = self.llm.invoke([("human", extract_prompt)])
                                value = response.content.strip()
                                
                                if value and value not in ["Not specified", "Not found", "Unknown", "N/A", "There is no company name mentioned in the given text."]:
                                    found_value = value[:200]  # Limit length
                                    print(f"✅ {found_value[:50]}...")
                                    break
                            except Exception as e:
                                continue
                    
                    # Only show attempt status if we haven't found anything yet
                    if found_value is None:
                        print(f"⚠️ Attempt {attempts_made}: Not found")
                
                # Update the field if found
                if found_value:
                    self.update_field(validated_data, builder_info, field['path'], found_value)
                else:
                    print(f"⚠️ Not found after {attempts_made} attempts")
        
        return validated_data, builder_info
    
    def update_field(self, validated_data, builder_info, field_path, new_value):
        """Update a single field in nested data"""
        parts = field_path.split('.')
        
        if parts[0] == "project_details":
            target = validated_data
            parts = parts[1:]
        elif parts[0] == "builder_contractor":
            target = builder_info
            parts = parts[1:]
        else:
            return
        
        # Navigate to parent
        current = target
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Update field
        current[parts[-1]] = new_value
    
    def compile_final_data(self, project_id, project_name, validated_data, status, builder_info, search_results):
        """Compile final validated data"""
        return {
            "project_id": project_id,
            "project_name": project_name,
            "validation_timestamp": datetime.now().isoformat(),
            "validation_agent": self.name,
            "data_quality": "VALIDATED",
            "project_details": validated_data,
            "construction_status": status,
            "builder_contractor": builder_info,
            "sources": {
                "total_sources_checked": sum(len(v) for v in search_results.values()),
                "search_categories": list(search_results.keys())
            },
            "genotek_relevance": {
                "material_opportunities": ["Hospital construction materials", "Medical facility flooring", "Healthcare-grade materials"],
                "priority_level": "HIGH" if "Under Construction in 2026" in status.get('status', '') else "MEDIUM",
                "recommended_action": "IMMEDIATE OUTREACH" if "Under Construction in 2026" in status.get('status', '') else "EARLY ENGAGEMENT"
            }
        }
    
    def save_final_data(self, final_data):
        """Save to final_data.json"""
        output_path = os.path.join(os.path.dirname(__file__), "final_data.json")
        
        try:
            with open(output_path, 'r') as f:
                existing = json.load(f)
        except:
            existing = {"validated_projects": []}
        
        # Update or add project
        project_id = final_data.get('project_id')
        for i, project in enumerate(existing.get('validated_projects', [])):
            if project.get('project_id') == project_id:
                existing['validated_projects'][i] = final_data
                print(f"♻️ Updated: {project_id}")
                break
        else:
            existing['validated_projects'].append(final_data)
            print(f"➕ Added: {project_id}")
        
        existing['last_updated'] = datetime.now().isoformat()
        existing['total_validated'] = len(existing['validated_projects'])
        
        with open(output_path, 'w') as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {output_path}")
        print(f"📊 Total projects: {existing['total_validated']}")
    
    def run(self):
        """Run optimized validation"""
        print("🚀 Starting hospital validation...")
        
        projects = self.load_projects()
        if not projects:
            print("❌ No projects found")
            return
        
        # Process first project only
        project = projects[0]
        project_id = project.get('id', 'UNKNOWN')
        raw_data = project.get('raw_data', {})
        
        print(f"🔬 Validating: {project_id}")
        
        # Extract project name
        project_name = self.extract_project_name(raw_data)
        print(f"📋 Project: {project_name}")
        
        # Multiple searches
        search_results = self.search_multiple(project_name)
        
        # Deep analysis
        validated_data = self.deep_analysis(project_name, search_results)
        
        # Verify status
        status = self.verify_status(validated_data, search_results)
        
        # Find builder info
        builder_info = self.find_builder_info(search_results)
        
        # Field-by-field validation
        validated_data, builder_info = self.validate_missing_fields(project_name, validated_data, builder_info)
        
        # Enhanced location search if location is missing
        if not validated_data.get('location', {}).get('city') or validated_data.get('location', {}).get('city') in ["Not specified", "Unknown"]:
            print(f"\n📍 Searching specific location for: {project_name}")
            validated_data = self.find_project_location(project_name, validated_data)
        
        # Enhanced contractor contact search (after field validation)
        contractor_name = builder_info.get('main_contractor', {}).get('company_name', '')
        if contractor_name and contractor_name not in ["Not found", "Not specified", "Unknown"]:
            print(f"\n📞 Searching contact details for contractor: {contractor_name}")
            builder_info = self.find_contractor_contacts(builder_info)
        
        # Compile and save
        final_data = self.compile_final_data(project_id, project_name, validated_data, status, builder_info, search_results)
        self.save_final_data(final_data)
        
        print(f"\n✅ Validation completed: {project_name}")
        print(f"🎯 Priority: {final_data['genotek_relevance']['priority_level']}")
        
        return final_data

if __name__ == "__main__":
    agent = FinalValidationAgent()
    agent.run()
