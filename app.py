import tkinter as tk
from tkinter import filedialog
from transcription import transcribe_audio
from audio_utils import convert_to_wav
import threading
import time
import os
import simpleaudio as sa
from pydub.playback import _play_with_simpleaudio as play  # faster backend
from pydub import AudioSegment

AUDIO_FILE = "Feeling_Unsupported,_Misunderstood,_or_Doubted.mp3"
OUTPUT_TXT = "transcription_output.txt"

def play_audio(path):
    audio = AudioSegment.from_file(path)
    raw_data = audio.raw_data
    play_obj = sa.play_buffer(raw_data,
                              num_channels=audio.channels,
                              bytes_per_sample=audio.sample_width,
                              sample_rate=audio.frame_rate)
    return play_obj, time.time()

def show_subtitles(text_segments, text_widget, start_time):
    for segment in text_segments:
        segment_start = segment['start']
        text = segment['text'].strip()

        # Wait until it's time to display this subtitle
        while time.time() - start_time < segment_start:
            time.sleep(0.01)

        # Update subtitle display
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text)
        text_widget.update()

def run_transcription(audio_path, text_widget):
    wav_path = convert_to_wav(audio_path)
    full_text, segments = transcribe_audio(wav_path)

    # Save transcription
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(full_text)

    # Start audio and record actual start time
    play_obj, start_time = play_audio(audio_path)

    # Start subtitles now that we know audio is playing
    threading.Thread(target=show_subtitles, args=(segments, text_widget, start_time), daemon=True).start()


def build_ui():
    root = tk.Tk()
    root.title("🎧 Podcast Subtitle Viewer")
    root.geometry("800x300")
    root.configure(bg="#f5f5f5")

    title = tk.Label(root, text="Podcast Subtitle Viewer 🎙", font=("Helvetica", 18, "bold"),
                     bg="#f5f5f5", fg="#333")
    title.pack(pady=10)

    subtitle_box = tk.Text(root, height=4, font=("Helvetica", 16), wrap=tk.WORD,
                           bg="#fff", fg="#222")
    subtitle_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    button = tk.Button(root, text="▶ Transcribe & Play Podcast", font=("Helvetica", 14),
                       bg="#007acc", fg="white",
                       command=lambda: run_transcription(AUDIO_FILE, subtitle_box))
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_ui()
