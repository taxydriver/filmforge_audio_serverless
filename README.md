# filmforge_audio_serverless

RunPod serverless worker for Stable Audio 2.5 generation using ComfyUI.

## Input

```json
{
  "input": {
    "prompt": "cinematic emotional trailer score, no vocals",
    "seconds": 30,
    "seed": 42,
    "steps": 8
  }
}
```

- `seconds`: clamped to `1..190`
- `steps`: clamped to `4..8` (optional, default `8`)

## Output

```json
{
  "audio_base64": "<base64 mp3>",
  "format": "mp3"
}
```

## Files

- `Dockerfile`
- `entrypoint.sh`
- `handler.py`
- `workflows/audio_trailer.json`

## Build

Build the worker image:

```bash
docker build -t filmforge-audio .
```

## Runtime Env

Stable Audio 2.5 in this worker uses Comfy API Nodes and requires one of:

- `COMFY_API_KEY`
- `COMFY_ORG_AUTH_TOKEN`
