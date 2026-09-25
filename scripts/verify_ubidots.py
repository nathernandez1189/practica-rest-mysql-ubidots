#!/usr/bin/env python3
"""Envía una muestra controlada y comprueba su lectura real, sin registrar el token."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from testUbidots import post_request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["normal", "alerta", "recuperacion"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    token = os.environ.get("UBIDOTS_TOKEN")
    if not token:
        parser.error("Configura UBIDOTS_TOKEN en el entorno local")
    device = os.environ.get("UBIDOTS_DEVICE", "equipo-rest")
    alarm = args.stage == "alerta"
    payload = {
        "temperature": 34 if alarm else 24,
        "humidity": 78 if alarm else 65,
        "position": {"value": 1, "context": {"lat": 4.711, "lng": -74.0721}},
        "luminosity": 820 if alarm else 550,
        "pressure": 754 if alarm else 750,
    }
    code, body = post_request(payload, token, device)
    assert all(body[key][0]["status_code"] == 201 for key in payload), body
    url = f"https://industrial.api.ubidots.com/api/v2.0/devices/~{device}/_/values/last"
    values = None
    for attempt in range(5):
        response = requests.get(url, headers={"X-Auth-Token": token}, timeout=20,
                                allow_redirects=False)
        response.raise_for_status()
        values = response.json()
        scalar_ok = all(values.get(k, {}).get("value") == v
                        for k, v in payload.items() if k != "position")
        position_ok = values.get("position", {}).get("context") == payload["position"]["context"]
        if scalar_ok and position_ok:
            break
        if attempt < 4:
            time.sleep(2)
    else:
        raise RuntimeError("Los valores consultados no coinciden con la muestra enviada")
    result = {"utc": datetime.now(timezone.utc).isoformat(), "stage": args.stage,
              "device": device, "payload": payload, "http_status": code,
              "response": body, "readback": values, "verified": True}
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
