"""Simulador de cinco variables. --dry-run no envía datos ni necesita token."""
import argparse
import json
import os
import random
import re
import sys
import time
import requests


def build_payload():
    return {
        "temperature": round(random.uniform(18, 35), 1),
        "humidity": round(random.uniform(35, 85), 1),
        "position": {"value": 1, "context": {
            "lat": round(4.711 + random.uniform(-0.002, 0.002), 6),
            "lng": round(-74.0721 + random.uniform(-0.002, 0.002), 6),
        }},
        "luminosity": random.randint(100, 1000),
        "pressure": round(random.uniform(745, 755), 1),
    }


def post_request(payload, token, device="machine", base_url="https://industrial.api.ubidots.com"):
    if base_url not in ("https://industrial.api.ubidots.com", "https://things.ubidots.com"):
        raise ValueError("Usa uno de los endpoints HTTPS oficiales de Ubidots")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", device):
        raise ValueError("La etiqueta del dispositivo debe usar letras minúsculas, números, guiones o guiones bajos")
    response = requests.post(
        f"{base_url}/api/v1.6/devices/{device}/",
        headers={"X-Auth-Token": token, "Content-Type": "application/json"},
        json=payload, timeout=20, allow_redirects=False,
    )
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"Ubidots respondió HTTP {response.status_code}; revisa cuenta, token y límites")
    body = response.json()
    # Un HTTP 200 puede contener errores por variable: verificarlos antes de afirmar recepción.
    def statuses(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "status_code" and isinstance(item, int):
                    yield item
                else:
                    yield from statuses(item)
        elif isinstance(value, list):
            for item in value:
                yield from statuses(item)
    if any(status >= 400 for status in statuses(body)):
        raise RuntimeError("Ubidots informó un error en al menos una variable")
    return response.status_code, body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--count", type=int, default=1, help="Cantidad finita de envíos")
    parser.add_argument("--interval", type=float, default=15, help="Segundos entre envíos")
    args = parser.parse_args()
    if args.count < 1 or args.interval < 1:
        parser.error("count e interval deben ser al menos 1")
    token = os.environ.get("UBIDOTS_TOKEN")
    if not args.dry_run and not token:
        parser.error("Configura UBIDOTS_TOKEN en tu terminal; no lo escribas en el código")
    for index in range(args.count):
        payload = build_payload()
        print(json.dumps(payload, ensure_ascii=False))
        if args.dry_run:
            print("SIMULACIÓN LOCAL: no se enviaron datos a Ubidots")
        else:
            try:
                code, body = post_request(payload, token,
                    os.environ.get("UBIDOTS_DEVICE", "machine"),
                    os.environ.get("UBIDOTS_URL", "https://industrial.api.ubidots.com"))
                print(f"HTTP {code}: {json.dumps(body)}")
            except (requests.RequestException, ValueError, RuntimeError) as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 1
        if index + 1 < args.count:
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
