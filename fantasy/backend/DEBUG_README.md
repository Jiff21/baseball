# Fantasy Baseball Server Debugging

This document explains how to see the detailed debugging output from the Python server calculations.

## 🔍 What's Included in Debug Output

The server now provides comprehensive debugging for each team calculation:

### 📊 Raw Team Stats
Shows the actual database values for each team:
```
📊 RAW TEAM STATS vs LEFTIES:
   ERA: 3.45
   WHIP: 1.23
   K/9: 8.7
   BB/9: 2.1
   HR/9: 1.2
   Hits/9: 8.5
```

### 🧮 Per_9 Calculations
Shows step-by-step math for converting per-9 stats to expected values:
```
🧮 PER_9 CALCULATIONS:
   Innings Factor: 6/9 = 0.6667
   Expected Hits: (8.5 * 0.6667) / 9 = 0.629630
   Expected Walks: (2.1 * 0.6667) / 9 = 0.155556
   Expected Strikeouts: (8.7 * 0.6667) / 9 = 0.644444
   Expected Home Runs: (1.2 * 0.6667) / 9 = 0.088889
   Expected Runs: (3.45 * 0.6667) / 9 = 0.255556
```

### ⚾ Hit Breakdown
Shows how hits are distributed into singles, doubles, triples:
```
⚾ HIT BREAKDOWN (Distribution):
   Expected Singles: 0.629630 * 0.75 = 0.472222
   Expected Doubles: 0.629630 * 0.20 = 0.125926
   Expected Triples: 0.629630 * 0.03 = 0.018889
   Expected Home Runs: 0.088889 (from HR/9 stat)
```

### 💰 Fantasy Points Calculation
Shows individual stat contributions to total points:
```
💰 FANTASY POINTS CALCULATION:
   Scoring Settings: {'S': 1, 'D': 2, 'T': 3, 'HR': 4, 'BB': 1, 'R': 1, 'RBI': 1, 'SO': -1}
   Singles: 0.472222 * 1 = 0.472222
   Doubles: 0.125926 * 2 = 0.251852
   Triples: 0.018889 * 3 = 0.056667
   Home Runs: 0.088889 * 4 = 0.355556
   Walks: 0.155556 * 1 = 0.155556
   Runs: 0.255556 * 1 = 0.255556
   Strikeouts: 0.644444 * -1 = -0.644444
   RBI: 0.255556 * 1 = 0.255556
   TOTAL BATTING POINTS: 1.157521
```

### 📊 Summary Statistics
Shows overall calculation results:
```
📊 CALCULATION SUMMARY:
   Total teams processed: 30
   Highest expected points: LAD (2.456)
   Lowest expected points: COL (1.123)
   Average expected points: 1.789
```

## 🚀 How to See Debug Output

### Method 1: Run the Test Script
```bash
cd fantasy/backend
python test_debug.py
```

### Method 2: Start the Server and Make API Calls
1. Start the Flask server:
```bash
cd fantasy/backend
python app.py
```

2. Make API calls to trigger calculations:
```bash
# Calculate for all teams
curl -X POST http://localhost:8000/api/calculate-expected \
  -H "Content-Type: application/json" \
  -d '{
    "handedness": "Lefty",
    "inning": 6,
    "league_type": "ESPN"
  }'

# Calculate for specific team
curl -X POST http://localhost:8000/api/calculate-team-expected \
  -H "Content-Type: application/json" \
  -d '{
    "team_abbreviation": "HOU",
    "handedness": "Lefty", 
    "inning": 6,
    "league_type": "ESPN"
  }'
```

3. Watch the server console output for detailed debugging information.

### Method 3: Frontend Triggers
When you use the frontend application, every calculation request will trigger the debug output in the Python server console.

## 📝 Notes

- **Wins/Losses**: The current database model doesn't include wins/losses fields, but the frontend expects them. Debug output includes warnings about this.
- **Log Level**: Debug output uses `logger.info()` so it's visible with the default INFO logging level.
- **Performance**: The detailed logging adds minimal overhead but provides valuable insights into calculations.

## 🔧 Customizing Debug Output

To modify the debug output, edit the `calculate_expected_points()` method in `fantasy/backend/services.py`.

The logging uses emojis and formatting to make it easy to scan through the output and find specific information.
