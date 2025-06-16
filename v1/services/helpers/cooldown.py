import requests
import time
import functools
from json.decoder import JSONDecodeError

# Simple in-memory breaker state (per process!)
breaker_state = {
    "failures": 0,
    "threshold": 10,         # max failures before blocking
    "blocked_until": 0,      # timestamp until when this is blocked
    "cooldown": 5 * 60       # 5 minutes in seconds
}

def circuit_breaker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()

        # If blocked, skip the call
        if breaker_state["blocked_until"] > now:
            return {"error": "Service temporarily unavailable due to repeated failures. Try again later."}

        try:
            result = func(*args, **kwargs)
            # If success, reset failures
            breaker_state["failures"] = 0
            return result
        except Exception as e:
            print(f"[Circuit Breaker] Exception: {e}")
            # Count failure
            breaker_state["failures"] += 1
            if breaker_state["failures"] >= breaker_state["threshold"]:
                breaker_state["blocked_until"] = now + breaker_state["cooldown"]
                print(f"[Circuit Breaker] Service blocked for {breaker_state['cooldown']}s due to too many failures.")
            return {"error": f"Exception: {str(e)}"}
    return wrapper