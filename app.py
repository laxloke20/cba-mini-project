from flask import Flask, jsonify, render_template
import time
import random
import json
import os
from pathlib import Path

app = Flask(__name__)

# ✅ Read PORT from environment variable
PORT = int(os.getenv("PORT", 5000))

# Path for persistent storage
DATA_DIR = Path('/app/data')
STATS_FILE = DATA_DIR / 'stats.json'

# Initialize stats dictionary
stats = {
    "fast": {"count": 0, "total_time": 0, "average_response_time": 0},
    "slow": {"count": 0, "total_time": 0, "average_response_time": 0}
}

def load_stats():
    """Load stats from JSON file if it exists"""
    global stats
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
                print(f"[INFO] Stats loaded from {STATS_FILE}")
        else:
            print(f"[INFO] Stats file not found. Using default stats.")
    except Exception as e:
        print(f"[ERROR] Could not load stats: {e}")

def save_stats():
    """Save stats to JSON file"""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Could not save stats: {e}")

# ✅ HOME ROUTE
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/fast')
def fast_api():
    global stats
    start = time.time()
    time.sleep(random.uniform(0.01, 0.05))
    duration = time.time() - start
    
    stats["fast"]["count"] += 1
    stats["fast"]["total_time"] += duration
    stats["fast"]["average_response_time"] = stats["fast"]["total_time"] / stats["fast"]["count"]
    
    save_stats()
    return jsonify({"status": "fast"})

@app.route('/api/slow')
def slow_api():
    global stats
    start = time.time()
    time.sleep(random.uniform(0.5, 2.0))
    duration = time.time() - start
    
    stats["slow"]["count"] += 1
    stats["slow"]["total_time"] += duration
    stats["slow"]["average_response_time"] = stats["slow"]["total_time"] / stats["slow"]["count"]
    
    save_stats()
    return jsonify({"status": "slow"})

@app.route('/api/stats')
def api_stats():
    return jsonify(stats)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    load_stats()
    print(f"[INFO] Starting Flask API server on port {PORT}...")
    
    # ✅ Use PORT variable here
    app.run(host='0.0.0.0', port=PORT)