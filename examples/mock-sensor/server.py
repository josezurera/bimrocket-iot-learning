"""Sensor REST simulado para los laboratorios de BIMROCKET."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import monotonic
from urllib.parse import parse_qs, urlparse


START_TIME = monotonic()


def build_reading(elapsed_seconds: float, offline: bool = False) -> dict:
    """Construye una lectura reproducible a partir del tiempo transcurrido."""
    temperature = 22.5 + 2.5 * math.sin(elapsed_seconds / 30)
    co2 = 650 + 500 * (1 + math.sin(elapsed_seconds / 20)) / 2

    return {
        "room": "A-101",
        "ifcGlobalId": "DEMO_IFC_GLOBAL_ID_A101",
        "temperature": round(temperature, 1),
        "co2": round(co2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "offline" if offline else "online",
    }


class SensorHandler(BaseHTTPRequestHandler):
    """Expone la lectura simulada mediante HTTP y JSON."""

    def do_GET(self) -> None:  # noqa: N802 - nombre exigido por BaseHTTPRequestHandler
        request = urlparse(self.path)

        if request.path == "/health":
            self.send_json({"status": "ok"})
            return

        if request.path == "/api/rooms/A-101":
            query = parse_qs(request.query)
            offline = query.get("offline", ["0"])[0] == "1"
            reading = build_reading(monotonic() - START_TIME, offline)
            self.send_json(reading)
            return

        self.send_json(
            {"error": "not_found", "path": request.path},
            status_code=404,
        )

    def send_json(self, payload: dict, status_code: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8001, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), SensorHandler)
    print(f"Sensor disponible en http://{args.host}:{args.port}/api/rooms/A-101")
    print("Pulsa Ctrl+C para detenerlo.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSensor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

