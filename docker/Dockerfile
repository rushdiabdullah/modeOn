FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uncomment on RunPod GPU image or extend from pytorch/pytorch:
# RUN pip install --no-cache-dir TTS==0.22.0 torch torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY api ./api
COPY tts ./tts

ENV MODEON_TTS_MODE=mock
EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
