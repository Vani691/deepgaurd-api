from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI(title="DeepGuard API")

API_KEY = "deepguard123"

class AudioRequest(BaseModel):
    audio: str  

@app.post("/analyze")
async def analyze_audio(
    request: AudioRequest,
    authorization: str = Header(None)
):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
       
        audio_bytes = base64.b64decode(request.audio)

        audio_size_kb = len(audio_bytes) / 1024

        if audio_size_kb < 50:
            verdict = "AI_GENERATED"
            confidence = 0.70
            explanation = "Audio payload too small; likely synthetic or clipped."
        else:
            verdict = "HUMAN"
            confidence = 0.80
            explanation = "Audio payload size consistent with natural speech."

        return {
            "classification": verdict,
            "confidence_score": confidence,
            "explanation": explanation
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio input")

@app.get("/")
def root():
    return {"status": "DeepGuard API is Running"}
