@echo off
echo ========================================
echo Hospital Watchlist Auto-Monitor
echo ========================================
echo.
echo Starting continuous monitoring...
echo The watchlist will update automatically when final_data.json changes
echo Press Ctrl+C to stop
echo.
python auto_watchlist.py --monitor
