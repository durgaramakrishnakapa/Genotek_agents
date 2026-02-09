"""
Configuration file for Genotek AI Lead Generation Platform
Copy this file to config.py and add your actual API keys
"""

# SerperDev API Configuration
# Get your API key from: https://serper.dev/
SERPER_API_KEY = "your_serper_api_key_here"

# Groq API Configuration  
# Get your API key from: https://console.groq.com/
GROQ_API_KEY = "your_groq_api_key_here"

# LLM Model Configuration
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model to use
LLM_TEMPERATURE = 0.1  # Lower = more deterministic

# Search Configuration
MAX_SEARCH_RESULTS = 10  # Maximum results per search query
SEARCH_TIMEOUT = 30  # Timeout in seconds for search requests

# Agent Configuration
AGENT_SEARCH_QUERIES = 5  # Number of search queries per agent run
TOP_RESULTS_TO_PROCESS = 2  # Number of top results to process with LLM

# Validation Configuration
VALIDATION_SEARCHES_PER_FIELD = 2  # Number of searches per field during validation
VALIDATION_BATCH_SIZE = 8  # Number of fields to validate in parallel
MIN_SEARCH_ATTEMPTS = 2  # Minimum search attempts before giving up
MAX_SEARCH_ATTEMPTS = 3  # Maximum search attempts per field

# Watchlist Configuration
WATCHLIST_CHECK_INTERVAL = 10  # Seconds between file change checks
FRONTEND_REFRESH_INTERVAL = 5000  # Milliseconds between frontend API polls

# Project Year Filter
TARGET_YEARS = [2026, 2027]  # Only include projects for these years
EXCLUDE_COMPLETED_BEFORE = 2026  # Exclude projects completed before this year

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = False  # Set to True to log to files
LOG_FILE_PATH = "logs/"  # Directory for log files

# API Rate Limiting
RATE_LIMIT_DELAY = 1  # Seconds to wait between API calls
MAX_RETRIES = 3  # Maximum number of retries for failed API calls

# Notes:
# 1. Never commit config.py with actual API keys to version control
# 2. Keep this example file updated when adding new configuration options
# 3. API keys should be kept secure and not shared publicly
