import requests
import streamlit as st
import base64
import io
from pydub import AudioSegment
from init import SARVAM_API_KEY, sarvam_tts_url

def split_hindi_text(text, max_parts=3, max_length=490, total_limit=1450):
    sentences = text.strip().split("।")
    sentences = [s.strip() + "।" for s in sentences if s.strip()]
    truncated_sentences = "".join(sentences)[:total_limit].split("।")
    truncated_sentences = [s.strip() + "।" for s in truncated_sentences if s.strip()]
    
    parts = []
    current_part = ""
    
    for sentence in truncated_sentences:
        if len(current_part) + len(sentence) <= max_length:
            current_part += sentence
        else:
            parts.append(current_part)
            current_part = sentence
            if len(parts) == max_parts - 1:
                break
    
    if current_part:
        parts.append(current_part)
    
    return parts[:max_parts]

def merge_base64_audio(audio_list):
    combined = AudioSegment.empty()

    for b64_audio in audio_list:
        audio_bytes = base64.b64decode(b64_audio)
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
        combined += audio_segment  # Concatenating audio

    # Export combined audio to bytes
    output_buffer = io.BytesIO()
    combined.export(output_buffer, format="wav")
    merged_b64_audio = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

    return merged_b64_audio

def get_audio_string(text_list):
    payload = {
        "inputs": text_list,   # make it 3 folds
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "pitch": -0.60,
        "pace": 1.5,
        "loudness": 1.5,
        "speech_sample_rate": 16000,
        "enable_preprocessing": False,
        "model": "bulbul:v1",
        "override_triplets": {}
    }
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", sarvam_tts_url, json=payload, headers=headers)
    # b64_audio_string = eval(response.text)['audios'][0]

    try:
        b64_audio_list = response.json().get("audios", [])
        b64_audio_string = merge_base64_audio(b64_audio_list)
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(response.text)
        
    return b64_audio_string

def autoplay_audio(b64_audio_string):
    md = f"""
    <audio autoplay>
    <source src="data:audio/wav;base64,{b64_audio_string}" type="audio/wav">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

