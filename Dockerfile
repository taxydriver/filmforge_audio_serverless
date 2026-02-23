FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget ffmpeg python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install runpod websocket-client requests

WORKDIR /

# Install ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /ComfyUI
RUN pip3 install -r /ComfyUI/requirements.txt

# Download Stable Audio model
RUN mkdir -p /ComfyUI/models/checkpoints
RUN wget -q https://huggingface.co/stabilityai/stable-audio-open-1.0/resolve/main/stable-audio-open-1.0.safetensors \
    -O /ComfyUI/models/checkpoints/stable-audio-open-1.0.safetensors

# Download T5 encoder
RUN mkdir -p /ComfyUI/models/clip
RUN wget -q https://huggingface.co/stabilityai/stable-audio-open-1.0/resolve/main/t5-base.safetensors \
    -O /ComfyUI/models/clip/t5-base.safetensors

COPY workflows /workflows
COPY handler.py /handler.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
