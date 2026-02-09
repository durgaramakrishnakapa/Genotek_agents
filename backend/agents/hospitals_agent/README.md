# Hospital Agent - Manual Execution

## Overview
The hospital agent consists of two main components that can be run separately:

1. **agent.py** - Searches for new hospital construction projects
2. **final_validator.py** - Validates and enriches project data

## Usage

### Step 1: Run the Agent (Search for Projects)
```bash
cd backend/agents/hospitals_agent
python agent.py
```

**What it does:**
- Searches globally for hospital construction projects (2026-2027 focus)
- Processes top 2 results with LLM
- Generates unique project IDs (HOSP_XXXXXXXXXXXX)
- Saves results to `initial_data.json`

### Step 2: Run the Final Validator (Deep Research)
```bash
cd backend/agents/hospitals_agent
python final_validator.py
```

**What it does:**
- Takes first project from `initial_data.json`
- Performs deep research with multiple targeted searches
- Field-by-field validation (2 searches per field, 8 fields per batch)
- Saves validated data to `final_data.json`

## Workflow

```
agent.py → initial_data.json → final_validator.py → final_data.json
```

## Files Generated

- **initial_data.json** - Raw search results with basic extraction
- **final_data.json** - Fully validated and enriched project data

## Manual vs Continuous

**Manual Execution (Current):**
- ✅ Full control over when to run
- ✅ Easy debugging and monitoring
- ✅ No background processes
- ✅ Run on-demand when needed

**Previous Continuous:**
- ❌ Background processes running constantly
- ❌ Harder to debug and control
- ❌ Resource intensive
- ❌ Complex process management

## API Integration

The frontend will read from:
- `/api/agents/hospitals/initial` → `initial_data.json`
- `/api/agents/hospitals/final` → `final_data.json`

Both files are updated when you run the respective scripts manually.