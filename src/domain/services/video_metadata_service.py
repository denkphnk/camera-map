from pathlib import Path
import json
import subprocess


class VideoMetadataService:
    def get_metadata(self, file_path: str) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Video file not found: {file_path}")

        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        video_stream = next(
            (
                stream
                for stream in data["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )

        if video_stream is None:
            raise ValueError("Video stream not found")

        duration = float(data["format"]["duration"])

        width = video_stream["width"]
        height = video_stream["height"]

        resolution = f"{width}x{height}"

        fps_raw = video_stream.get("avg_frame_rate", "0/1")

        numerator, denominator = fps_raw.split("/")
        fps = round(float(numerator) / float(denominator), 2)

        return {
            "duration": duration,
            "fps": fps,
            "resolution": resolution,
        }