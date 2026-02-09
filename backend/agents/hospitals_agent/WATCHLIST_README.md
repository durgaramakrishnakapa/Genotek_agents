# Hospital Watchlist System

The Hospital Watchlist system automatically monitors validated hospital construction projects and provides a dedicated interface for tracking high-value opportunities for Genotek.

## 🎯 Purpose

- **Automatic Monitoring**: Tracks all validated hospital projects from `final_data.json`
- **Priority Management**: Categorizes projects by priority (HIGH/MEDIUM/LOW)
- **Contact Tracking**: Maintains contractor contact information for outreach
- **Opportunity Assessment**: Identifies material opportunities for Genotek
- **Frontend Integration**: Provides real-time data to the web interface

## 📁 Files

### Core Components
- `watchlist.py` - Main watchlist manager class
- `auto_watchlist.py` - Automation script for updates
- `watchlist_data.json` - Generated watchlist data (auto-created)

### Frontend Integration
- `/api/agents/hospitals/watchlist` - API endpoint
- `frontend/client/src/hooks/use-watchlist.ts` - React hook
- `frontend/client/src/pages/Watchlist.tsx` - Watchlist page

## 🚀 Usage

### Manual Update
```bash
python watchlist.py
```

### Single Update (with status)
```bash
python auto_watchlist.py
```

### Continuous Monitoring
```bash
python auto_watchlist.py --monitor
```

## 📊 Data Structure

### Watchlist Entry
```json
{
  "project_id": "HOSP_FF13A04BC26D",
  "project_name": "Ballarat Base Hospital",
  "added_to_watchlist": "2026-02-07T13:30:37.851177",
  "validation_timestamp": "2026-02-07T13:21:01.891219",
  "data_quality": "VALIDATED",
  "summary": {
    "location": "Ballarat, Australia",
    "full_address": "1 Drummond Street North, Ballarat, VIC 3350",
    "status": "Under Construction",
    "confidence": "High",
    "completion_year": "2027",
    "priority_level": "MEDIUM",
    "recommended_action": "EARLY ENGAGEMENT"
  },
  "contractor": {
    "company_name": "H. Troon",
    "contact_email": "info@htroon.com.au",
    "contact_phone": "03 5339 2208",
    "website": "www.htroon.com.au",
    "address": "833 Creswick Road, Ballarat 3355"
  },
  "opportunities": {
    "material_opportunities": [
      "Hospital construction materials",
      "Medical facility flooring",
      "Healthcare-grade materials"
    ],
    "priority_level": "MEDIUM",
    "recommended_action": "EARLY ENGAGEMENT"
  },
  "watchlist_status": "ACTIVE",
  "last_checked": "2026-02-07T13:30:37.851177",
  "notes": "Auto-added from validation on 2026-02-07T13:21:01.891219",
  "full_data": { /* Complete validated project data */ }
}
```

### Statistics
```json
{
  "statistics": {
    "total_projects": 1,
    "active_projects": 1,
    "high_priority": 0,
    "medium_priority": 1,
    "low_priority": 0,
    "new_projects_this_update": 0
  }
}
```

## 🔄 Workflow

1. **Hospital Agent** finds and processes projects → `initial_data.json`
2. **Final Validator** validates projects → `final_data.json`
3. **Watchlist Manager** monitors `final_data.json` → `watchlist_data.json`
4. **Frontend** displays watchlist via API endpoint
5. **Users** can view, filter, and manage watchlist projects

## 🎨 Frontend Features

### Watchlist Page (`/watchlist`)
- **Real-time Updates**: Refreshes every 30 seconds
- **Priority Filtering**: Filter by HIGH/MEDIUM/LOW priority
- **Detailed View**: Complete project information in modal
- **Contact Information**: Direct access to contractor details
- **Material Opportunities**: Genotek-specific opportunities
- **Status Tracking**: Validation status and confidence levels

### Integration Points
- **Lead Generation**: Validated hospital projects link to watchlist
- **Navigation**: Dedicated watchlist menu item
- **API**: RESTful endpoint for data access

## 🔧 Configuration

### Auto-Update Frequency
- **Manual**: Run scripts as needed
- **Monitoring**: 10-second check interval (configurable)
- **Frontend**: 30-second refresh interval

### Priority Levels
- **HIGH**: Immediate outreach required
- **MEDIUM**: Early engagement recommended  
- **LOW**: Future opportunity monitoring

## 📈 Benefits

1. **Automated Tracking**: No manual project management needed
2. **Real-time Updates**: Always current with latest validations
3. **Priority Focus**: Highlights high-value opportunities
4. **Contact Ready**: Immediate access to contractor information
5. **Opportunity Mapping**: Clear material opportunities identified
6. **Scalable**: Handles growing number of validated projects

## 🔮 Future Enhancements

- **Email Alerts**: Notify on new high-priority projects
- **CRM Integration**: Export contacts to external systems
- **Automated Outreach**: Template generation for initial contact
- **Progress Tracking**: Monitor engagement status
- **Multi-Agent**: Extend to other construction categories

## 🚨 Important Notes

- Only **validated** hospital projects appear in watchlist
- Watchlist updates automatically when `final_data.json` changes
- Frontend refreshes every 30 seconds for real-time experience
- All contractor contact information is preserved for outreach
- Priority levels guide engagement strategy recommendations