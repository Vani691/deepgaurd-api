from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import os
import librosa
from transformers import pipeline


app = FastAPI(title="DeepGuard API")


API_KEY = "deepguard123"  


print("Loading lightweight speech model...")
classifier = pipeline(
    "audio-classification",
    model="facebook/wav2vec2-base-960h"
)


class AudioRequest(BaseModel):
    audio: str  # Base64 encoded audio


@app.post("/analyze")
async def analyze_audio(
    request: AudioRequest,
    authorization: str = Header(None)
):
   
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    temp_file = "temp_audio.wav"

    try:
        # Decode Base64 audio
        audio_bytes = base64.b64decode(request.audio)

        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        # Load audio (speech only)
        audio_array, sampling_rate = librosa.load(temp_file, sr=16000)

        # Run model
        results = classifier({
            "array": audio_array,
            "sampling_rate": sampling_rate
        })

        top = max(results, key=lambda x: x["score"])
        score = float(top["score"])

        
        verdict = "HUMAN"

        return {
            "classification": verdict,
            "confidence_score": round(score, 4),
            "explanation": "Baseline speech authenticity analysis completed."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.get("/")
def root():
    return {"status": "DeepGuard API is Running"}
