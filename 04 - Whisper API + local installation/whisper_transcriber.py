import subprocess
import whisper
import os

os.environ["PATH"] += os.pathsep + "/opt/homebrew/Cellar/ffmpeg/7.1_3/bin"

def extract_audio_segment(input_file, output_file, start_time, duration):
    try:
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", start_time,
            "-t", str(duration),
            "-c", "copy",
            output_file
        ]

        subprocess.run(command, check=True)
        print(f"The extracted segment is saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error has occurred: {e}")
    except FileNotFoundError:
        print("Ffmpeg is not installed or not found in PATH.")

def transcribe_audio(file_path):
    try:
        model = whisper.load_model("base")
        print("Transcribing the audio...")
        result = model.transcribe(file_path)
        print("Transcription is completed.")

        with open("transcription_with_timestamps.txt", "w") as f:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

        print("Transcription with timestamps saved to 'transcription_with_timestamps.txt'.")

    except Exception as e:
        print(f"An error has occurred during transcription: {e}")

if __name__ == "__main__":
    input_audio = "./recording.mp3"        # Input audio file
    output_audio = "./extracted.mp3"       # Output audio file for extracted segment
    start_time = "00:10:00"                # Start time (HH:MM:SS)
    duration = 600                         # Duration in seconds (10 minutes)

    extract_audio_segment(input_audio, output_audio, start_time, duration)

    if os.path.exists(output_audio):
        transcribe_audio(output_audio)
    else:
        print("The extracted audio segment is not found.")
