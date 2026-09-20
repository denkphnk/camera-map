from pathlib import Path

import json
import subprocess

from subprocess import CalledProcessError


class VideoMetadataService:
    def get_metadata(
        self,
        file_path: str,
    ) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Video file not found: {file_path}",
            )
        
        with open(file_path, 'rb') as f:
            header = f.read(32)

            if b"ftyp" not in header:
                raise ValueError('Invalid mp4 file.')

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

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )
        except CalledProcessError as error:
            raise ValueError(
                "Uploaded file is not a valid video",
            ) from error

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
            raise ValueError(
                "Video stream not found",
            )

        format_name = data["format"]["format_name"]
        if "mp4" not in format_name:
            raise ValueError("Only mp4 files are allowed")

        duration = float(
            data["format"]["duration"],
        )

        width = video_stream["width"]
        height = video_stream["height"]

        resolution = (
            f"{width}x{height}"
        )

        fps_raw = video_stream.get(
            "avg_frame_rate",
            "0/1",
        )

        numerator, denominator = (
            fps_raw.split("/")
        )

        try:
            denominator_value = float(
                denominator,
            )

            if denominator_value == 0:
                fps = 0
            else:
                fps = round(
                    float(numerator)
                    / denominator_value,
                    2,
                )

        except (
            ValueError,
            ZeroDivisionError,
        ):
            fps = 0

        return {
            "duration": duration,
            "fps": fps,
            "resolution": resolution,
        }

    def extract_first_frame(
        self,
        video_path: str,
        output_path: str,
    ) -> str:
        path = Path(video_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Video file not found: {video_path}",
            )

        command = [
            "ffmpeg",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            output_path,
            "-y",
        ]

        subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return output_path