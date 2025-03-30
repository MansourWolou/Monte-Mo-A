from typing import Union
import os
import time


from fastapi import FastAPI, UploadFile, File, HTTPException 
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="Video Search Engine API")

# Config
class Config:
    VIDEO_UPLOAD_DIR = "uploaded_videos"
    PROCESSED_DIR = "processed"
    FRAME_EXTRACT_DIR = "frames"
    SEGMENT_DURATION = 30  # seconds
    FRAMES_PER_SEGMENT = 10
    # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def setup_dirs(cls):
        os.makedirs(cls.VIDEO_UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.PROCESSED_DIR, exist_ok=True)
        os.makedirs(cls.FRAME_EXTRACT_DIR, exist_ok=True)

Config.setup_dirs()


@app.get("/")
def read_root():
    return {"Hello": "World"}

def save_uploaded_video(file: UploadFile) -> str:
    timestamp = int(time.time())
    filename = f"video_{timestamp}_{file.filename}"
    filepath = os.path.join(Config.VIDEO_UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    
    return filepath

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    try:
        video_path = save_uploaded_video(file)
        return JSONResponse({
            "status": "success",
            "video_path": video_path,
            "filename": file.filename
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/search/")
async def print_text(input_data: str):
    # Print the received text to the console
    print(f"Received text: {input_data}")
    return {"message": f"Received text: {input_data}"}


