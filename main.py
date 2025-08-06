from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import File, UploadFile
import shutil
from pathlib import Path
import httpx
import os

load_dotenv()

MURF_API_KEY =os.getenv("MURF_API_KEY")
app = FastAPI()

#upload audio file to directory

UPLOAD_DIR= Path("uploads")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = file_path.stat().st_size

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file_size
    }

# Serve static files (JS, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML file
@app.get("/")
async def get_home():
    return FileResponse(os.path.join("static", "index.html"))




class TTSRequest(BaseModel):
    text: str


@app.post("/tts")
async def generate_tts(request: TTSRequest):
    if not MURF_API_KEY:
        raise HTTPException(status_code=500, detail="MURF_API_KEY_NOT_FOUND")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY
    }

    payload = {
        "text": request.text,
        "style": "Conversational",
        "multiNativeLocale": "en-US",
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 1.0,
        "language": "en-US",
        "voice_id": "en-US-natalie"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.murf.ai/v1/speech/generate",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            print("✅ Murf API Raw Response:", data)

            # ✅ Extract audioFile instead of audio_url
            return {"audio_url": data.get("audioFile", "Not found")}
        
        except httpx.HTTPError as e:
            print("❌ Murf API Error Response:", e.response.text)
            raise HTTPException(status_code=500, detail=str(e))
