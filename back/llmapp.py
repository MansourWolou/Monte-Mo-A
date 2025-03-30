# main.py
import os
import json
import time
import subprocess
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import numpy as np
import torch
from transformers import (
    BlipProcessor, 
    BlipForConditionalGeneration,
    WhisperProcessor, 
    WhisperForConditionalGeneration,
    pipeline
)

app = FastAPI(title="Video Search Engine API")

# Config
class Config:
    VIDEO_UPLOAD_DIR = "uploaded_videos"
    PROCESSED_DIR = "processed"
    FRAME_EXTRACT_DIR = "frames"
    SEGMENT_DURATION = 30  # seconds
    FRAMES_PER_SEGMENT = 10
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def setup_dirs(cls):
        os.makedirs(cls.VIDEO_UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.PROCESSED_DIR, exist_ok=True)
        os.makedirs(cls.FRAME_EXTRACT_DIR, exist_ok=True)

Config.setup_dirs()

# Models
class VideoModels:
    def __init__(self):
        print("Loading models...")
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(Config.DEVICE)
        
        self.whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        self.whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small").to(Config.DEVICE)
        
        self.translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
        print("Models loaded!")

models = VideoModels()

# Schemas
class VideoSegment(BaseModel):
    start_time: float
    end_time: float
    description: str
    audio_transcript: str
    score: float

class ProcessedVideo(BaseModel):
    video_id: str
    segments: List[VideoSegment]
    metadata: dict

# Core Processing Functions
def save_uploaded_video(file: UploadFile) -> str:
    timestamp = int(time.time())
    filename = f"video_{timestamp}_{file.filename}"
    filepath = os.path.join(Config.VIDEO_UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    
    return filepath

def extract_frames(video_path: str, output_dir: str) -> List[str]:
    """Extract frames using FFmpeg"""
    frame_pattern = os.path.join(output_dir, "frame_%04d.jpg")
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{Config.SEGMENT_DURATION/Config.FRAMES_PER_SEGMENT}",
        "-q:v", "2",
        frame_pattern
    ]
    
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("frame_")])

def cut_video_segment(input_path: str, output_path: str, start: float, end: float) -> bool:
    """Cut video segment using FFmpeg"""
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def generate_image_description(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = models.blip_processor(image, return_tensors="pt").to(Config.DEVICE)
    outputs = models.blip_model.generate(**inputs)
    description = models.blip_processor.decode(outputs[0], skip_special_tokens=True)
    return models.translator(description)[0]['translation_text']

def process_video(video_path: str) -> ProcessedVideo:
    """Main processing pipeline"""
    video_id = os.path.splitext(os.path.basename(video_path))[0]
    segments = []
    
    # Extract frames
    frames = extract_frames(video_path, Config.FRAME_EXTRACT_DIR)
    
    # Process each frame
    for i, frame_path in enumerate(frames):
        timestamp = i * (Config.SEGMENT_DURATION / Config.FRAMES_PER_SEGMENT)
        
        # Generate description
        description = generate_image_description(frame_path)
        
        # Create segment
        segment = VideoSegment(
            start_time=timestamp,
            end_time=timestamp + (Config.SEGMENT_DURATION / Config.FRAMES_PER_SEGMENT),
            description=description,
            audio_transcript="",  # Can be added with Whisper
            score=0.5  # Placeholder scoring
        )
        segments.append(segment)
    
    return ProcessedVideo(
        video_id=video_id,
        segments=segments,
        metadata={
            "original_filename": os.path.basename(video_path),
            "processing_date": datetime.now().isoformat(),
            "duration": len(frames) * (Config.SEGMENT_DURATION / Config.FRAMES_PER_SEGMENT)
        }
    )

# API Endpoints
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

@app.post("/process/")
async def process_uploaded_video(video_path: str):
    try:
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Video file not found")
        
        result = process_video(video_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cut/")
async def cut_video(
    input_path: str,
    start_time: float,
    end_time: float,
    output_filename: str = "cut_video.mp4"
):
    try:
        output_path = os.path.join(Config.PROCESSED_DIR, output_filename)
        success = cut_video_segment(input_path, output_path, start_time, end_time)
        
        if success:
            return FileResponse(
                output_path,
                media_type="video/mp4",
                filename=output_filename
            )
        else:
            raise HTTPException(status_code=500, detail="Video cutting failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/")
async def search_video(
    video_path: str,
    query: str,
    threshold: float = 0.3
):
    try:
        # This would use your LLM comparison logic
        # Placeholder implementation
        processed = process_video(video_path)
        matches = [
            seg for seg in processed.segments 
            if query.lower() in seg.description.lower()
        ]
        
        return {
            "query": query,
            "matches": matches,
            "total_segments": len(processed.segments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)