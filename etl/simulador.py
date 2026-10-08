import json, os, random
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-5))  # hora de Colombia
inicio = datetime(2026, 10, 5, 6, 0, tzinfo=TZ)
os.makedirs("data", exist_ok=True)
random.seed(42)

with open("data/lecturas.jsonl", "w", encoding="utf-8") as f:
    for i in range(144):  # 12 h, una lectura cada 5 min
        for device_id in [1, 2]:  # los dos dispositivos
            msg = {
                "device_id": device_id,
                "ts": (inicio + timedelta(minutes=5 * i)).isoformat(),
                "p_ac": round(random.uniform(0, 5.0), 3),          # kW
                "irradiancia": round(random.uniform(0, 1000), 1),  # W/m2
                "temp_modulo": round(random.uniform(18, 60), 1),   # grados C
                "voltaje_dc": round(random.uniform(200, 600), 1),  # V (campo nuevo)
            }
            if random.random() < 0.03:
                msg["alarma"] = "GRID_FAULT"
            f.write(json.dumps(msg) + "\n")
