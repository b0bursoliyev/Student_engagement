import os
import subprocess
from pathlib import Path


def split_video_ffmpeg(input_path, output_dir, interval=7):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"

    command = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-c", "copy", "-map", "0",
        "-f", "segment", "-segment_time", str(interval),
        str(output_pattern)
    ]

    print(f"Processing: {input_path}")
    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"✅ Segments saved to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Skipping {input_path} — ffmpeg error:\n{e.stderr.decode(errors='ignore')[:300]}")



def process_directory(input_dir, output_dir, interval=7):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    for file in input_dir.rglob("*"):
        if file.suffix.lower() in {".mp4", ".avi", ".mov", ".mkv"}:
            rel_path = file.parent.relative_to(input_dir)
            file_output_dir = output_dir / rel_path
            split_video_ffmpeg(file, file_output_dir, interval)


if __name__ == "__main__":
    input_base_dir = "videos/individual_participants/individual_participants_audio_all"
    output_base_dir = "videos/split_videos"

    if not os.path.exists(input_base_dir):
        print(f"❌ Error: Input directory '{input_base_dir}' does not exist.")
    else:
        process_directory(input_base_dir, output_base_dir, interval=7)
        print("\n🎉 Video splitting completed!")
