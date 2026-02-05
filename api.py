from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import os
import librosa
import numpy as np


app = FastAPI(title="DeepGuard API")


API_KEY = "deepguard123"


class AudioRequest(BaseModel):
    audio: str  # Base64 encoded audio


def analyze_audio_signal(audio_array, sr):
    duration = len(audio_array) / sr
    energy = np.mean(np.abs(audio_array))

    # Heuristic rules
    if duration < 1.0:
        return "Understanding", 0.3, "Audio too short for reliable voice characteristics."

    if energy < 0.01:
        return "AI_GENERATED", 0.75, "Low natural energy variation detected in voice signal."

    return "HUMAN", 0.85, "Natural speech energy and duration detected."

=
@app.post("/analyze")
async def analyze_audio(
    request: AudioRequest,
    authorization: str = Header(None)
):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    temp_file = "temp_audio.wav"

    try:
        audio_bytes = base64.b64decode(request.audio)
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        audio_array, sr = librosa.load(temp_file, sr=16000)

        classification, confidence, explanation = analyze_audio_signal(audio_array, sr)

        return {
            "classification": classification,
            "confidence_score": confidence,
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.get("/")
def root():
    return {"status": "DeepGuard API is Running"}
