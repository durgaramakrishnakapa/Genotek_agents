"""
Hospital Watchlist - Monitors final_data.json and provides watchlist functionality
Automatically tracks validated hospital projects for frontend display
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, '../..'))

class HospitalWatchlist:
    """Manages hospital project watchlist from validated data"""
    
    def __init__(self):
        self.agent_name = "Hospital Watchlist Manager"
        self.final_data_path = os.path.join(current_dir, "final_data.json")
        self.watchlist_path = os.path.join(current_dir, "watchlist_data.json")
        
        print(f"\n👁️ {self.agent_name} - Monitoring validated hospital projects\n")
    
    def load_final_data(self) -> Dict[str, Any]:
        """Load validated projects from final_data.json"""
        try:
            with open(self.final_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print("⚠️ final_data.json not found")
            return {"validated_projects": []}
        except json.JSONDecodeError as e:
            print(f"⚠️ Error reading final_data.json: {e}")
            return {"validated_projects": []}
    
    def load_existing_watchlist(self) -> Dict[str, Any]:
        """Load existing watchlist data"""
        try:
            with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {
                "watchlist_projects": [],
                "last_updated": None,
                "total_watched": 0,
                "agent": self.agent_name
            }
        except json.JSONDecodeError:
            return {
                "watchlist_projects": [],
                "last_updated": None,
                "total_watched": 0,
                "agent": self.agent_name
            }
    
    def create_watchlist_entry(self, validated_project: Dict[str, Any]) -> Dict[str, Any]:
        """Convert validated project to watchlist entry"""
        project_details = validated_project.get('project_details', {})
        builder_contractor = validated_project.get('builder_contractor', {})
        construction_status = validated_project.get('construction_status', {})
        genotek_relevance = validated_project.get('genotek_relevance', {})
        
        # Extract key information for watchlist
        location = project_details.get('location', {})
        main_contractor = builder_contractor.get('main_contractor', {})
        
        watchlist_entry = {
            "project_id": validated_project.get('project_id'),
            "project_name": validated_project.get('project_name'),
            "added_to_watchlist": datetime.now().isoformat(),
            "validation_timestamp": validated_project.get('validation_timestamp'),
            "data_quality": validated_project.get('data_quality'),
            
            # Key project information
            "summary": {
                "location": f"{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}",
                "full_address": location.get('full_address', 'Address not specified'),
                "status": construction_status.get('status', 'Status unknown'),
                "confidence": construction_status.get('confidence', 'Low'),
                "completion_year": construction_status.get('completion_year', 'TBD'),
                "priority_level": genotek_relevance.get('priority_level', 'MEDIUM'),
                "recommended_action": genotek_relevance.get('recommended_action', 'MONITOR')
            },
            
            # Contractor information
            "contractor": {
                "company_name": main_contractor.get('company_name', 'Unknown'),
                "contact_email": main_contractor.get('contact_email', 'Not available'),
                "contact_phone": main_contractor.get('contact_phone', 'Not available'),
                "website": main_contractor.get('website', 'Not available'),
                "address": main_contractor.get('address', 'Not available')
            },
            
            # Genotek opportunities
            "opportunities": {
                "material_opportunities": genotek_relevance.get('material_opportunities', []),
                "priority_level": genotek_relevance.get('priority_level', 'MEDIUM'),
                "recommended_action": genotek_relevance.get('recommended_action', 'MONITOR')
            },
            
            # Watchlist metadata
            "watchlist_status": "ACTIVE",
            "last_checked": datetime.now().isoformat(),
            "notes": f"Auto-added from validation on {validated_project.get('validation_timestamp', 'unknown date')}",
            
            # Full validated data reference
            "full_data": validated_project
        }
        
        return watchlist_entry
    
    def update_watchlist(self) -> Dict[str, Any]:
        """Update watchlist with new validated projects"""
        print("🔍 Checking for new validated hospital projects...")
        
        # Load data
        final_data = self.load_final_data()
        existing_watchlist = self.load_existing_watchlist()
        
        validated_projects = final_data.get('validated_projects', [])
        existing_project_ids = {p.get('project_id') for p in existing_watchlist.get('watchlist_projects', [])}
        
        new_projects_added = 0
        updated_projects = []
        
        # Process each validated project
        for validated_project in validated_projects:
            project_id = validated_project.get('project_id')
            
            if project_id not in existing_project_ids:
                # New project - add to watchlist
                watchlist_entry = self.create_watchlist_entry(validated_project)
                updated_projects.append(watchlist_entry)
                new_projects_added += 1
                print(f"➕ Added to watchlist: {validated_project.get('project_name', 'Unknown')} ({project_id})")
            else:
                # Existing project - update with latest data
                for i, existing_project in enumerate(existing_watchlist.get('watchlist_projects', [])):
                    if existing_project.get('project_id') == project_id:
                        # Update existing entry with new validation data
                        updated_entry = self.create_watchlist_entry(validated_project)
                        updated_entry['added_to_watchlist'] = existing_project.get('added_to_watchlist')  # Keep original add date
                        updated_entry['notes'] = f"Updated from validation on {validated_project.get('validation_timestamp', 'unknown date')}"
                        updated_projects.append(updated_entry)
                        print(f"🔄 Updated watchlist: {validated_project.get('project_name', 'Unknown')} ({project_id})")
                        break
        
        # Add any existing projects that weren't updated
        for existing_project in existing_watchlist.get('watchlist_projects', []):
            if existing_project.get('project_id') not in {p.get('project_id') for p in updated_projects}:
                updated_projects.append(existing_project)
        
        # Create updated watchlist
        updated_watchlist = {
            "watchlist_projects": updated_projects,
            "last_updated": datetime.now().isoformat(),
            "total_watched": len(updated_projects),
            "agent": self.agent_name,
            "statistics": {
                "total_projects": len(updated_projects),
                "active_projects": len([p for p in updated_projects if p.get('watchlist_status') == 'ACTIVE']),
                "high_priority": len([p for p in updated_projects if p.get('opportunities', {}).get('priority_level') == 'HIGH']),
                "medium_priority": len([p for p in updated_projects if p.get('opportunities', {}).get('priority_level') == 'MEDIUM']),
                "low_priority": len([p for p in updated_projects if p.get('opportunities', {}).get('priority_level') == 'LOW']),
                "new_projects_this_update": new_projects_added
            }
        }
        
        return updated_watchlist
    
    def save_watchlist(self, watchlist_data: Dict[str, Any]) -> None:
        """Save watchlist data to file"""
        try:
            with open(self.watchlist_path, 'w', encoding='utf-8') as f:
                json.dump(watchlist_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Watchlist saved: {self.watchlist_path}")
        except Exception as e:
            print(f"❌ Error saving watchlist: {e}")
    
    def get_watchlist_summary(self, watchlist_data: Dict[str, Any]) -> None:
        """Print watchlist summary"""
        stats = watchlist_data.get('statistics', {})
        projects = watchlist_data.get('watchlist_projects', [])
        
        print(f"\n📊 Hospital Watchlist Summary:")
        print(f"   Total Projects: {stats.get('total_projects', 0)}")
        print(f"   Active Projects: {stats.get('active_projects', 0)}")
        print(f"   High Priority: {stats.get('high_priority', 0)}")
        print(f"   Medium Priority: {stats.get('medium_priority', 0)}")
        print(f"   Low Priority: {stats.get('low_priority', 0)}")
        print(f"   New This Update: {stats.get('new_projects_this_update', 0)}")
        print(f"   Last Updated: {watchlist_data.get('last_updated', 'Never')}")
        
        if projects:
            print(f"\n📋 Watched Projects:")
            for project in projects:
                priority = project.get('opportunities', {}).get('priority_level', 'MEDIUM')
                priority_icon = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
                print(f"   {priority_icon} {project.get('project_name', 'Unknown')} - {project.get('summary', {}).get('location', 'Unknown location')}")
    
    def run(self) -> Dict[str, Any]:
        """Run watchlist update process"""
        print("🚀 Starting hospital watchlist update...")
        
        # Update watchlist with latest validated data
        updated_watchlist = self.update_watchlist()
        
        # Save updated watchlist
        self.save_watchlist(updated_watchlist)
        
        # Show summary
        self.get_watchlist_summary(updated_watchlist)
        
        print(f"\n✅ Watchlist update completed")
        return updated_watchlist

if __name__ == "__main__":
    watchlist = HospitalWatchlist()
    watchlist.run()