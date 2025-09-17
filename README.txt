Upstox commodity scraper (Railway-ready)
---------------------------------------
Files included:
- main.py         : scraper that polls Upstox every POLL_INTERVAL_MIN minutes
- requirements.txt
- Procfile
- runtime.txt
- .env.example

Usage (local):
1) pip install -r requirements.txt
2) create .env file from .env.example and set credentials
3) python main.py

Usage (Railway):
1) Create new Railway project and upload this repo/ZIP
2) Set environment variables in Railway (UPSTOX_API_KEY, UPSTOX_ACCESS_TOKEN, UPSTOX_SYMBOL)
3) Deploy and check logs
