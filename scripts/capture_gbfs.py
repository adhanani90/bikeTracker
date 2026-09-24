import json
import requests
import time

from datetime import datetime, timezone
from pathlib import Path

directory = Path(__file__).resolve().parent.parent / "data" / "raw"
directory.mkdir(parents=True, exist_ok=True)

status_url="https://toronto.publicbikesystem.net/customer/gbfs/v3.0/station_status"
info_url="https://toronto.publicbikesystem.net/customer/gbfs/v3.0/station_information"

while True:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    date = timestamp[:8]

    try:
        status_response = requests.get(status_url, timeout=10)
        info_response = requests.get(info_url, timeout=10)
        status_response.raise_for_status()
        info_response.raise_for_status()
    except requests.RequestException as e:
        print(f"{timestamp}: fetch failed ({e})")
        time.sleep(60)
        continue

    status_record = {"timestamp": timestamp, "raw": status_response.text}
    info_record = {"timestamp": timestamp, "raw": info_response.text}

    with open(directory / f"station_status_{date}.ndjson", "a") as f:
        f.write(json.dumps(status_record) + "\n")
    with open(directory / f"station_information_{date}.ndjson", "a") as f:
        f.write(json.dumps(info_record) + "\n")

    print(f"{timestamp}: appended status ({len(status_response.text)}B) , info ({len(info_response.text)}B)")
    time.sleep(60)
