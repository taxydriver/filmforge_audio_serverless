# filmforge_audio_serverless

RunPod serverless worker for Stable Audio generation using ComfyUI.

## Input

```json
{
  "input": {
    "prompt": "cinematic emotional trailer score, no vocals",
    "seconds": 30,
    "seed": 42
  }
}
```

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
