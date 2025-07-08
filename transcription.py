import whisper

model = whisper.load_model("base")  # Or "small", "medium", etc.

def transcribe_audio(path):
    result = model.transcribe(path)
    return result["text"], result["segments"]
