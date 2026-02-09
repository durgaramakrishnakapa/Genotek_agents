# Genotek AI Lead Generation Backend

**Standalone** AI-powered lead generation system for Genotek (Bijon Trading Private Limited) using SerperDev and Groq LLM.

## Features

- 🔍 **Web Search**: Uses SerperDev API to search for construction projects
- 🤖 **AI Extraction**: Groq LLM extracts detailed project information (20+ fields)
- 🎯 **Lead Classification**: AI scores and classifies leads based on fit
- ✉️ **Email Generation**: Automatically generates personalized outreach emails
- 📊 **Standalone**: No frontend connection - works independently

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. API keys are configured in `config.py`:
   - SerperDev API Key
   - Groq API Key

## Usage

Run the lead generator:
```bash
python lead_generator.py
```

This will:
1. Search for construction projects (focuses on TOP result)
2. Extract ALL available details (emails, phones, dates, contractors)
3. Classify each lead with relevance score
4. Generate personalized outreach emails
5. Print complete summary to console

## Files

- `config.py` - Configuration, API keys, and AI prompts
- `lead_generator.py` - Main lead generation logic
- `requirements.txt` - Python dependencies

## Output

Console output includes:
- Search results from SerperDev
- Detailed project information (20+ fields)
- Lead classification and scoring
- Generated outreach emails
- Summary of all generated leads

## Extracted Information

The system extracts:
- Project name, company, location, type
- Budget, start date, completion date
- Contact email, phone, website
- Project manager, key contacts
- Contractor, architect names
- Project size, features
- Material requirements

## Customization

Edit `config.py` to:
- Add more search queries
- Modify AI prompts for better extraction
- Adjust LLM temperature
- Change model settings

## Note

This backend is **completely independent** from the frontend. It generates leads and displays them in the console. The frontend uses its own static data from JSON files.
