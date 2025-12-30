from fastapi import FastAPI, Query
import requests
from datetime import datetime

app = FastAPI()

@app.get("/vehicle")
def vehicle_details(rc: str = Query(..., example="UP80AB1234")):

    url = f"https://vehicleinfo.app/rc-details/{rc}?rc_no={rc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-IN,en-US;q=0.9"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return {
                "error": True,
                "message": "Site blocked or unavailable",
                "status": r.status_code
            }

        html = r.text

        if len(html) < 500:
            return {
                "error": True,
                "message": "Invalid response"
            }

        return {
            "success": True,
            "rc_number": rc,
            "source": "vehicleinfo.app",
            "fetched_at": datetime.utcnow().isoformat(),
            "html_length": len(html)
        }

    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }
