import requests
import time
import random
import threading
import os

# Fetch API URL from environment variable, default to localhost
API_URL = os.getenv('API_URL', 'http://127.0.0.1:5000')

def simulate_users():
    """Simulate users making requests to the API endpoints"""
    endpoints = [
        f'{API_URL}/api/fast',
        f'{API_URL}/api/slow'
    ]
    
    while True:
        url = random.choices(endpoints, weights=[80, 20])[0]
        try:
            response = requests.get(url, timeout=5)
            print(f"[USER] Pinged: {url} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[WARN] Connection error. Waiting for API at {API_URL}...")
            time.sleep(2)
        except requests.exceptions.Timeout:
            print(f"[WARN] Request timeout for {url}")
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(2)
        
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == '__main__':
    print(f"[INFO] Starting traffic generator...")
    print(f"[INFO] API URL: {API_URL}")
    
    # Start 3 threads to simulate concurrent users
    for i in range(3):
        thread = threading.Thread(target=simulate_users, daemon=True)
        thread.start()
        print(f"[INFO] Started user simulation thread {i+1}")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Traffic generator stopped.")
