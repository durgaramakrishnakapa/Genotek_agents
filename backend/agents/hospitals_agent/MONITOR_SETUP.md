# Hospital Watchlist Auto-Monitor Setup

This guide explains how to keep the watchlist automatically synchronized with validated hospital projects.

## 🚀 Quick Start

### Windows
```bash
# Double-click or run:
start_monitor.bat
```

### Command Line (All Platforms)
```bash
python auto_watchlist.py --monitor
```

## 🔄 How It Works

The auto-monitor continuously watches `final_data.json` for changes:

1. **Checks every 10 seconds** if the file has been modified
2. **Automatically updates** `watchlist_data.json` when changes detected
3. **Frontend refreshes every 5 seconds** to show latest data
4. **Result**: Near real-time updates (5-15 second delay max)

## 📊 What You'll See

```
🔄 Auto Watchlist Monitor - Starting...
📁 Monitoring: C:\...\hospitals_agent\final_data.json
🚀 Initial watchlist update...
✅ Watchlist updated successfully
....📝 final_data.json updated at 2026-02-07 13:21:01
🔄 Updating watchlist...
✅ Watchlist updated successfully
```

- **Dots (...)**: Checking for changes (no updates needed)
- **Update message**: File changed, watchlist updated

## 🎯 Complete Workflow

### 1. Start the Monitor (Once)
```bash
python auto_watchlist.py --monitor
```
Leave this running in a terminal/command prompt.

### 2. Run Your Agents (As Needed)
```bash
# Find new hospital projects
python agent.py

# Validate projects
python final_validator.py
```

### 3. Watch the Magic ✨
- Monitor detects the change in `final_data.json`
- Automatically updates `watchlist_data.json`
- Frontend refreshes within 5 seconds
- New projects appear in the watchlist!

## 🖥️ Running in Background

### Windows (Background Process)
```bash
# Start in new window
start python auto_watchlist.py --monitor

# Or use Task Scheduler for automatic startup
```

### Linux/Mac (Background Process)
```bash
# Run in background
nohup python auto_watchlist.py --monitor > monitor.log 2>&1 &

# Check if running
ps aux | grep auto_watchlist

# Stop
pkill -f auto_watchlist
```

## 🔧 Configuration

### Change Check Interval
Edit `auto_watchlist.py`, line ~35:
```python
time.sleep(10)  # Change to desired seconds
```

### Change Frontend Refresh Rate
Edit `frontend/client/src/hooks/use-watchlist.ts`:
```typescript
refetchInterval: 5000, // Change to desired milliseconds
```

## 📈 Performance

- **CPU Usage**: Minimal (~0.1% when idle)
- **Memory**: ~20-30 MB
- **Network**: None (local file monitoring)
- **Disk I/O**: Minimal (only reads on change)

## 🛑 Stopping the Monitor

- **Interactive**: Press `Ctrl+C`
- **Background**: Use task manager or `pkill` command

## 🔍 Troubleshooting

### Monitor Not Detecting Changes
1. Check file path is correct
2. Ensure you have read permissions
3. Verify `final_data.json` exists

### Frontend Not Updating
1. Check browser console for errors
2. Verify API endpoint is accessible: `http://localhost:5000/api/agents/hospitals/watchlist`
3. Clear browser cache and refresh

### High CPU Usage
1. Increase check interval (default: 10 seconds)
2. Check for file system issues
3. Restart the monitor

## 💡 Tips

1. **Development**: Keep monitor running while testing
2. **Production**: Use system service or task scheduler
3. **Multiple Agents**: Can run one monitor per agent type
4. **Logging**: Redirect output to file for debugging

## 🎯 Expected Behavior

**Timeline from validation to frontend:**
1. `final_validator.py` completes → `final_data.json` updated
2. Monitor detects change (0-10 seconds)
3. Watchlist updated (1-2 seconds)
4. Frontend polls API (0-5 seconds)
5. **Total delay: 1-17 seconds** (typically 5-10 seconds)

## 📝 Notes

- Monitor runs indefinitely until stopped
- Safe to restart anytime (no data loss)
- Multiple instances can run simultaneously (not recommended)
- Works with any text editor or script updating `final_data.json`
