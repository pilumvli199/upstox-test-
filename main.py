# main.py
# Upstox commodity scraper - fetches LTP every 1 minute for a configured symbol

import os, time, traceback
from datetime import datetime
import schedule
from dotenv import load_dotenv
try:
    from upstox_api.api import Upstox
except Exception:
    Upstox = None

load_dotenv()

API_KEY = os.getenv('UPSTOX_API_KEY')
ACCESS_TOKEN = os.getenv('UPSTOX_ACCESS_TOKEN')
SYMBOL = os.getenv('UPSTOX_SYMBOL', 'CRUDEOIL')  # default
POLL_INTERVAL_MIN = int(os.getenv('POLL_INTERVAL_MIN', '1'))

if not (API_KEY and ACCESS_TOKEN):
    print('Missing UPSTOX_API_KEY or UPSTOX_ACCESS_TOKEN in environment. Exiting.')
    raise SystemExit(1)

# init client
u = None
if Upstox is not None:
    try:
        u = Upstox(API_KEY, ACCESS_TOKEN)
        print('[INFO] Upstox client initialized')
    except Exception as e:
        print('[WARN] Failed to initialize Upstox client:', e)
else:
    print('[WARN] upstox library not importable at runtime; check requirements.')

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def try_get_instrument_by_symbol(symbol):
    candidates = [
        ('MCX_FO', symbol),
        ('MCX', symbol),
        ('NSE_COMMODITY', symbol),
        ('NSE', symbol),
    ]
    for exch, sym in candidates:
        try:
            if not u:
                continue
            inst = u.get_instrument_by_symbol(exch, sym)
            if inst:
                print(f'[{now()}] Resolved instrument via ({exch},{sym}):', inst)
                return inst
        except Exception as e:
            print(f'[{now()}] get_instrument_by_symbol({exch},{sym}) failed: {e}')
    return None

def fetch_and_log():
    try:
        print('\n' + '='*40)
        print(f'[{now()}] Fetching data for symbol: {SYMBOL}')
        if u is None:
            print('Upstox client not available.')
            return
        inst = try_get_instrument_by_symbol(SYMBOL)
        if not inst:
            print(f'[{now()}] Could not resolve instrument for {SYMBOL}')
            return
        try:
            ltp_resp = u.get_live_feed(inst, Upstox.LiveFeedType.LTP)
            print(f'[{now()}] LTP:', ltp_resp)
        except Exception as e:
            print(f'[{now()}] LTP fetch failed:', e)
        try:
            candles = u.get_ohlc(inst, 'minute', 1)
            print(f'[{now()}] Recent candles:', candles)
        except Exception as e:
            print(f'[{now()}] Candles fetch failed:', e)
        print('='*40 + '\n')
    except Exception as e:
        print(f'[{now()}] Unexpected error:', e)
        traceback.print_exc()

schedule.every(POLL_INTERVAL_MIN).minutes.do(fetch_and_log)

print(f'[INFO] Starting Upstox commodity scraper for {SYMBOL} every {POLL_INTERVAL_MIN} min')
fetch_and_log()

while True:
    schedule.run_pending()
    time.sleep(1)
