import os
import librosa
import torch
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import joblib


base_dir = os.path.dirname(__file__)  
model_path = os.path.join(base_dir, "random_forest_model.pkl")

clf = joblib.load(model_path)


processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
wav2vec_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")


labels = ["low", "medium", "high"]

def extract_features(file_path):
    audio, sr = librosa.load(file_path, sr=16000)  
    inputs = processor(audio, sampling_rate=sr, return_tensors="pt", padding=True)
    with torch.no_grad():
        embeddings = wav2vec_model(**inputs).last_hidden_state
    return torch.mean(embeddings, dim=1).squeeze(0).numpy()  


def classify_audio(file_path):
    try:
        features = extract_features(file_path)
        features = features.reshape(1, -1)  
        prediction = clf.predict(features)
        score = prediction[0]
        return labels[score - 1]  
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


