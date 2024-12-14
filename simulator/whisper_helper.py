import os
import whisper

def transcribeAudio(filepath):
    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    return result["text"]
  