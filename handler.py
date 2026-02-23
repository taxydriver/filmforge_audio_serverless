import base64
import json
import os
import time
import uuid
import urllib.request
from typing import Any, Dict

import runpod

SERVER_ADDRESS = "127.0.0.1"
CLIENT_ID = str(uuid.uuid4())


def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_json(url: str) -> Dict[str, Any]:
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def queue_prompt(prompt: Dict[str, Any]) -> str:
    url = f"http://{SERVER_ADDRESS}:8188/prompt"
    return post_json(url, {"prompt": prompt, "client_id": CLIENT_ID})["prompt_id"]


def wait_for_outputs(prompt_id: str, timeout_s: int = 3600) -> Dict[str, Any]:
    start = time.time()
    while True:
        if time.time() - start > timeout_s:
            raise TimeoutError("Audio generation timeout")

        hist = get_json(f"http://{SERVER_ADDRESS}:8188/history/{prompt_id}")
        if prompt_id in hist and hist[prompt_id].get("outputs"):
            return hist[prompt_id]

        time.sleep(2)


def load_workflow() -> Dict[str, Any]:
    with open("/workflows/audio_trailer.json", "r", encoding="utf-8") as fh:
        return json.load(fh)


def find_audio_file(history: Dict[str, Any]) -> str:
    for _node_id, node in (history.get("outputs") or {}).items():
        for key in ("audio", "audios", "files"):
            for item in node.get(key, []) or []:
                fullpath = item.get("fullpath")
                if fullpath and os.path.exists(fullpath):
                    return fullpath
    raise FileNotFoundError("Audio output file not found")


def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    inp = job.get("input") or {}
    prompt_text = inp.get("prompt")
    if not prompt_text:
        return {"error": "input.prompt is required"}

    seconds = float(inp.get("seconds", 30))
    seed = int(inp.get("seed", 42))

    wf = load_workflow()

    # Patch workflow nodes: prompt (6), duration (11), seed (3)
    wf["6"]["inputs"]["text"] = prompt_text
    wf["11"]["inputs"]["seconds"] = seconds
    wf["3"]["inputs"]["seed"] = seed

    prompt_id = queue_prompt(wf)
    history = wait_for_outputs(prompt_id)
    audio_path = find_audio_file(history)

    with open(audio_path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("utf-8")

    return {"audio_base64": b64, "format": "mp3"}


runpod.serverless.start({"handler": handler})
