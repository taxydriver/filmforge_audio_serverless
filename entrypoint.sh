#!/usr/bin/env bash
set -euo pipefail

python3 /ComfyUI/main.py --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &

python3 - <<'PY'
import time
import urllib.request

url = "http://127.0.0.1:8188/"
for _ in range(180):
    try:
        urllib.request.urlopen(url, timeout=2)
        raise SystemExit(0)
    except Exception:
        time.sleep(1)
raise SystemExit("ComfyUI did not become ready")
PY

python3 /handler.py
