import whisper
import subprocess
import ffmpeg

def extract_audio_segment(input_file, output_file, start_time, end_time):
    """
    Extracts a specific segment from an audio file using FFmpeg.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the extracted audio segment.
        start_time (str): Start time in the format 'hh:mm:ss' or 'mm:ss'.
        end_time (str): End time in the format 'hh:mm:ss' or 'mm:ss'.

    Returns:
        None
    """
    # ffmpeg_path = "C:/ffmpeg/bin/ffmpeg"
    # command = [
    #     ffmpeg_path, "-i", input_file,
    #     "-ss", start_time,
    #     "-to", end_time,
    #     "-c", "copy", output_file, "-y"
    # ]
    (
    ffmpeg
    .input(input_file, ss=start_time, to=end_time)
    .output(output_file, codec='copy')
    .run(overwrite_output=True)
    )

    # subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)




def transcribe_audio(file_path, model_name="base"):
    """
    Transcribes an audio file using Whisper.

    Args:
        file_path (str): Path to the audio file.
        model_name (str): Whisper model name (e.g., 'base', 'small', 'medium', 'large').

    Returns:
        str: The transcribed text.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path)
    return result["text"]


if __name__ == "__main__":
    # Input audio file
    input_audio = "recording.mp3"

    # Extracted segment
    output_audio = "segment.mp3"
    start_time = "00:02:20"  # Start time (hh:mm:ss or mm:ss)
    end_time = "00:03:40"    # End time (hh:mm:ss or mm:ss)

    try:
        # Step 1: Extract the segment
        print("Extracting audio segment...")
        extract_audio_segment(input_audio, output_audio, start_time, end_time)
        print(f"Segment extracted to: {output_audio}")

        # Step 2: Transcribe the extracted segment
        print("Transcribing audio segment...")
        transcription = transcribe_audio(output_audio, model_name="base")
        print("\nTranscription:\n")
        print(transcription)

    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg processing: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
