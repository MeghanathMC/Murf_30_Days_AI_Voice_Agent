from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import assemblyai as aai
import httpx
import os
import shutil
from pathlib import Path

# Load environment variables
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Configure AssemblyAI
aai.settings.api_key = ASSEMBLYAI_API_KEY

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML file at root
@app.get("/")
async def get_home():
    return FileResponse(os.path.join("static", "index.html"))

# Transcription endpoint
@app.post("/transcribe/file")
async def transcribe_audio_file(file: UploadFile = File(...)):
    if not ASSEMBLYAI_API_KEY:
        raise HTTPException(status_code=500, detail="ASSEMBLYAI_API_KEY_NOT_FOUND")

    try:
        # Save the uploaded file temporarily
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe the audio file
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(str(file_path))

        # Clean up the temporary file
        os.remove(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(status_code=500, detail=transcript.error)

        return {"transcription": transcript.text}
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# TTS Request Model
class TTSRequest(BaseModel):
    text: str

# Text-to-Speech endpoint
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
        "voice_id": "en-US-natalie"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://api.murf.ai/v1/speech/generate", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return {"audio_url": data.get("audioFile", "Not Found")}
        except httpx.HTTPError as e:
            print(f"Murf API Error: {e.response.text}")
            raise HTTPException(status_code=500, detail=str(e))
