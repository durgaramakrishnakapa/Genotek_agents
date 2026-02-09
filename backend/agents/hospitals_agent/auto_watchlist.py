"""
Auto Watchlist Updater - Monitors final_data.json and automatically updates watchlist
Run this script periodically or after validation to keep watchlist current
"""

import os
import sys
import time
import json
from datetime import datetime
from watchlist import HospitalWatchlist

def monitor_final_data():
    """Monitor final_data.json for changes and update watchlist"""
    watchlist = HospitalWatchlist()
    final_data_path = watchlist.final_data_path
    
    print("🔄 Auto Watchlist Monitor - Starting...")
    print(f"📁 Monitoring: {final_data_path}")
    
    last_modified = None
    
    while True:
        try:
            if os.path.exists(final_data_path):
                current_modified = os.path.getmtime(final_data_path)
                
                if last_modified is None:
                    # First run
                    print("🚀 Initial watchlist update...")
                    watchlist.run()
                    last_modified = current_modified
                elif current_modified > last_modified:
                    # File has been modified
                    print(f"\n📝 final_data.json updated at {datetime.fromtimestamp(current_modified)}")
                    print("🔄 Updating watchlist...")
                    watchlist.run()
                    last_modified = current_modified
                else:
                    # No changes
                    print(".", end="", flush=True)
            else:
                print("⚠️ final_data.json not found, waiting...")
            
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Auto watchlist monitor stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(30)  # Wait longer on error

def run_once():
    """Run watchlist update once and exit"""
    print("🔄 Single Watchlist Update")
    watchlist = HospitalWatchlist()
    result = watchlist.run()
    
    if result:
        print(f"\n✅ Watchlist updated successfully")
        print(f"📊 Total projects: {result.get('statistics', {}).get('total_projects', 0)}")
        return True
    else:
        print(f"\n❌ Watchlist update failed")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_final_data()
    else:
        run_once()