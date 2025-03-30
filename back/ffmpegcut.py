import os
import subprocess
import math
import argparse
from datetime import datetime, timedelta

def format_time(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_video_duration(input_file):
    """Get the duration of a video file in seconds using ffprobe"""
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        input_file
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Error getting video duration: {result.stderr}")
    
    return float(result.stdout.strip())

def cut_video(input_file, output_dir, segment_length=30):
    """Cut video into segments of specified length in seconds"""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get video duration
    duration = get_video_duration(input_file)
    print(duration)
    
    # Calculate number of segments
    num_segments = math.ceil(duration / segment_length)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    print(f"Video duration: {format_time(duration)}")
    print(f"Creating {num_segments} segments of {segment_length} seconds each...")
    
    # Process each segment
    for i in range(num_segments):
        start_time = i * segment_length
        
        # Handle the last segment (may be shorter than segment_length)
        if start_time + segment_length > duration:
            end_time = duration
        else:
            end_time = start_time + segment_length
        
        output_file = os.path.join(output_dir, f"{base_name}_segment_{i+1:03d}.mp4")
        
        # Format start and end times for ffmpeg
        start_time_str = format_time(start_time)
        segment_duration = end_time - start_time
        
        # Use ffmpeg to cut the segment
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ss", start_time_str,
            "-t", str(segment_duration),
            "-c", "copy",  # Use copy to avoid re-encoding (much faster)
            "-avoid_negative_ts", "1",
            output_file
        ]
        
        print(f"Creating segment {i+1}/{num_segments}: {start_time_str} to {format_time(end_time)}")
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            print(f"Error creating segment {i+1}: {result.stderr.decode()}")
        else:
            print(f"Successfully created segment: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut a video into 30-second segments')
    parser.add_argument('C:\Users\Sapin\Documents\projets\Monte_Mo-A\back\VID_20250329_083004.mp4', help='Path to the input video file')
    parser.add_argument('--output-dir', default='output', help='Directory to save the segments (default: ./output)')
    parser.add_argument('--segment-length', type=int, default=30, help='Length of each segment in seconds (default: 30)')
    
    args = parser.parse_args()
    
    cut_video(args.input_file, args.output_dir, args.segment_length)