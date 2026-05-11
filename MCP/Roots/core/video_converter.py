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
    
    @classmethod
    def generate_output_path(cls, input_path: str, format: str) -> str:
        """Generate output path by replacing the file extension."""
        base_path = os.path.splitext(input_path)[0]
        return f"{base_path}.{format.lower()}"
    
    @classmethod
    def build_ffmpeg_command(cls, input_path: str, output_path: str, format: str) -> list:
        """Build the ffmpeg command based on format settings."""
        preset = cls.QUALITY_PRESETS["medium"]
        
        # Base command
        cmd = ["ffmpeg", "-i", input_path, "-y"]
        
        if format.lower() == "gif":
            # Special handling for GIF conversion
            cmd.extend([
                "-vf", "fps=15,scale=480:-1:flags=lanczos",
                "-c:v", "gif",
                output_path
            ])
        elif format.lower() in cls.SUPPORTED_FORMATS:
            # Standard video conversion
            cmd.extend([
                "-c:v", "libx264",
                "-preset", preset["preset"],
                "-crf", preset["crf"],
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ])
        else:
            raise ValueError(f"Unsupported output format: {format}")
            
        return cmd
    
    