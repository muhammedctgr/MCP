import os
import asyncio
from pathlib import Path


class VideoConverter:
    """Handles video conversion operations using ffmpeg."""
    
    # Quality presets for video conversion
    QUALITY_PRESETS = {
        "low": {"crf": "28", "preset": "fast"},
        "medium": {"crf": "23", "preset": "medium"},
        "high": {"crf": "18", "preset": "slow"},
    }
    
    SUPPORTED_FORMATS = ["webm", "mkv", "avi", "mov", "gif"]
    
    @classmethod
    def validate_input(cls, input_path: str) -> Path:
        """Validate the input file exists and is an MP4."""
        input_file = Path(input_path)
        
        if not input_file.exists():
            raise ValueError(f"Input file not found: {input_path}")
        
        if not input_path.lower().endswith(".mp4"):
            raise ValueError("Input file must be an MP4 file")
            
        return input_file
    
    