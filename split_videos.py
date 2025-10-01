import os
import cv2
from tqdm import tqdm


def split_video(input_path, output_dir, segment_seconds=7):
    """Split a video into fixed-length segments with progress tracking."""
    os.makedirs(output_dir, exist_ok=True)

    # Open video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps

    print(f"\nProcessing: {os.path.basename(input_path)}")
    print(f"Duration: {duration:.1f}s, Frames: {frame_count}, FPS: {fps:.2f}")
    print(f"Splitting into {segment_seconds}-second segments...")

    frames_per_segment = int(segment_seconds * fps)
    total_segments = (frame_count + frames_per_segment - 1) // frames_per_segment

    segment_num = 0
    frame_num = 0

    # Main progress bar for segments
    with tqdm(total=total_segments, desc="Creating segments", unit="segment") as pbar_segments:
        while frame_num < frame_count:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_segment_{segment_num:04d}.mp4")

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Frame progress bar for current segment
            with tqdm(total=frames_per_segment, desc=f"Segment {segment_num + 1}/{total_segments}",
                      leave=False, unit="frame") as pbar_frames:
                frames_written = 0
                while frames_written < frames_per_segment and frame_num < frame_count:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)
                    frames_written += 1
                    frame_num += 1
                    pbar_frames.update(1)

            out.release()

            if frames_written > 0:
                segment_num += 1
                pbar_segments.update(1)
                pbar_segments.set_postfix({"Current": os.path.basename(output_path)})
            elif os.path.exists(output_path):
                os.remove(output_path)

    cap.release()

    print(f"\n✅ Split into {segment_num} segments in '{output_dir}'")


def process_videos(input_dir, output_base_dir, segment_seconds=7):
    """Process all video files in the input directory with progress tracking."""
    video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.MP4', '.AVI', '.MOV', '.MKV')
    os.makedirs(output_base_dir, exist_ok=True)

    # Get list of video files
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(video_exts)]

    if not video_files:
        print(f"No video files found in {input_dir}")
        return

    print(f"\nFound {len(video_files)} videos to process")
    print("=" * 50)

    # Process each video file with progress bar
    for filename in tqdm(video_files, desc="Processing videos", unit="video"):
        input_path = os.path.join(input_dir, filename)
        video_name = os.path.splitext(filename)[0]
        output_dir = os.path.join(output_base_dir, video_name)

        split_video(input_path, output_dir, segment_seconds)

    print("\n" + "=" * 50)
    print("✅ All videos processed successfully!")


if __name__ == "__main__":
    INPUT_DIR = "videos/all_participants"
    OUTPUT_DIR = "output_segments"
    SEGMENT_LENGTH = 7  # seconds

    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' does not exist.")
    else:
        process_videos(INPUT_DIR, OUTPUT_DIR, SEGMENT_LENGTH)