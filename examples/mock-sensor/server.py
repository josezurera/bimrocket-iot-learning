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

ROOMS = {
    "A-101": {
        "ifcGlobalId": "DEMO_IFC_GLOBAL_ID_A101",
        "temperature_base": 22.5,
        "temperature_amplitude": 2.5,
        "temperature_phase": 0,
        "co2_base": 650,
        "co2_amplitude": 500,
        "co2_phase": 0,
    },
    "A-102": {
        "ifcGlobalId": "DEMO_IFC_GLOBAL_ID_A102",
        "temperature_base": 21.0,
        "temperature_amplitude": 1.5,
        "temperature_phase": 8,
        "co2_base": 500,
        "co2_amplitude": 350,
        "co2_phase": 12,
    },
    "A-103": {
        "ifcGlobalId": "DEMO_IFC_GLOBAL_ID_A103",
        "temperature_base": 24.0,
        "temperature_amplitude": 2.0,
        "temperature_phase": 16,
        "co2_base": 900,
        "co2_amplitude": 600,
        "co2_phase": 24,
    },
}


def build_reading(
    elapsed_seconds: float,
    offline: bool = False,
    room: str = "A-101",
) -> dict:
    """Construye una lectura reproducible a partir del tiempo transcurrido."""
    room_config = ROOMS[room]

    temperature = room_config["temperature_base"] + room_config[
        "temperature_amplitude"
    ] * math.sin((elapsed_seconds + room_config["temperature_phase"]) / 30)

    co2 = room_config["co2_base"] + room_config["co2_amplitude"] * (
        1 + math.sin((elapsed_seconds + room_config["co2_phase"]) / 20)
    ) / 2

    return {
        "room": room,
        "ifcGlobalId": room_config["ifcGlobalId"],
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

        if request.path == "/api/rooms":
            self.send_json({"rooms": sorted(ROOMS)})
            return

        if request.path.startswith("/api/rooms/"):
            room = request.path.removeprefix("/api/rooms/")

            if room not in ROOMS:
                self.send_json(
                    {"error": "unknown_room", "room": room},
                    status_code=404,
                )
                return

            query = parse_qs(request.query)
            offline = query.get("offline", ["0"])[0] == "1"
            reading = build_reading(monotonic() - START_TIME, offline, room)
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
    print(f"Salas simuladas: {', '.join(sorted(ROOMS))}")
    print("Pulsa Ctrl+C para detenerlo.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSensor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

