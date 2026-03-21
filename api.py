from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import os
import librosa
from transformers import pipeline


app = FastAPI(title="DeepGuard API")

API_KEY = "deepguard123"  

print("Loading AI Model...")
classifier = pipeline(
    "audio-classification",
    model="Hemgg/Deepfake-audio-detection"
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
        # Decode base64 audio
        audio_bytes = base64.b64decode(request.audio)

        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        # Load audio safely
        audio_array, sampling_rate = librosa.load(temp_file, sr=16000)

        # Run model
        results = classifier({
            "array": audio_array,
            "sampling_rate": sampling_rate
        })

        # Pick top result
        top = max(results, key=lambda x: x["score"])
        label = top["label"].lower()
        score = float(top["score"])

        # Verdict logic
        if any(x in label for x in ["fake", "spoof", "generated", "ai"]):
            verdict = "AI_GENERATED"
        else:
            verdict = "HUMAN"

        # Final JSON
        return {
            "classification": verdict,
            "confidence_score": round(score, 4),
            "explanation": "Spectral voice analysis completed."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.get("/")
def root():
    return {"status": "DeepGuard API is Running"}
