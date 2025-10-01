import os
import wave
import contextlib
from tqdm import tqdm
import argparse


def split_audio(input_path, output_dir, segment_seconds=7):
    """Split an audio file into fixed-length segments with progress tracking."""
    os.makedirs(output_dir, exist_ok=True)

    try:
        with contextlib.closing(wave.open(input_path, 'rb')) as audio_file:
            # Get audio properties
            n_channels = audio_file.getnchannels()
            sample_width = audio_file.getsampwidth()
            frame_rate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            duration = n_frames / float(frame_rate)

            print(f"\nProcessing: {os.path.basename(input_path)}")
            print(f"Duration: {duration:.1f}s, Sample Rate: {frame_rate}Hz, Channels: {n_channels}")

            frames_per_segment = int(segment_seconds * frame_rate)
            total_segments = (n_frames + frames_per_segment - 1) // frames_per_segment

            base_name = os.path.splitext(os.path.basename(input_path))[0]
            segment_num = 0

            with tqdm(total=total_segments, desc="Creating segments", unit="segment") as pbar:
                while True:
                    output_path = os.path.join(output_dir, f"{base_name}_segment_{segment_num:04d}.wav")

                    # Read frames for this segment
                    frames = audio_file.readframes(frames_per_segment)
                    if not frames:
                        break

                    # Write the segment
                    with wave.open(output_path, 'wb') as segment_file:
                        segment_file.setnchannels(n_channels)
                        segment_file.setsampwidth(sample_width)
                        segment_file.setframerate(frame_rate)
                        segment_file.writeframes(frames)

                    segment_num += 1
                    pbar.update(1)
                    pbar.set_postfix({"Current": os.path.basename(output_path)})

            print(f"\n✅ Split into {segment_num} segments in '{output_dir}'")

    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")


def process_audios(input_dir, output_base_dir, segment_seconds=7):
    """Process all audio files in the input directory with progress tracking."""
    audio_exts = ('.wav', '.mp3', '.aac', '.flac', '.ogg', '.m4a', '.WAV', '.MP3', '.AAC')
    os.makedirs(output_base_dir, exist_ok=True)

    # Get list of audio files
    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(audio_exts)]

    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return

    print(f"\nFound {len(audio_files)} audio files to process")
    print("=" * 50)

    # Process each audio file with progress bar
    for filename in tqdm(audio_files, desc="Processing audio files", unit="file"):
        input_path = os.path.join(input_dir, filename)
        audio_name = os.path.splitext(filename)[0]
        output_dir = os.path.join(output_base_dir, audio_name)

        split_audio(input_path, output_dir, segment_seconds)

    print("\n" + "=" * 50)
    print("✅ All audio files processed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split audio files into fixed-length segments.')
    parser.add_argument('--input-dir', default='audio/all_participants_audio',
                        help='Directory containing audio files to process')
    parser.add_argument('--output-dir', default='output_audio_segments',
                        help='Directory to save the output segments')
    parser.add_argument('--segment-length', type=int, default=7,
                        help='Length of each segment in seconds (default: 7)')

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
    else:
        process_audios(args.input_dir, args.output_dir, args.segment_length)