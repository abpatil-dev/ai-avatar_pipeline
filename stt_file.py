import requests
from init import SARVAM_API_KEY, sarvam_stt_url

def get_transcript(file_path):
    with open(file_path, "rb") as audio_file:
        files = {
            "model": (None, "saarika:v2"),
            "language_code": (None, "hi-IN"),
            "with_timestamps": (None, "true"),
            "with_diarization": (None, "false"),
            "file": (file_path, audio_file, "audio/wav")  # Specify the correct file type
        }

        headers = {
            "api-subscription-key": SARVAM_API_KEY
        }

        response = requests.post(sarvam_stt_url, files=files, headers=headers)

    transcript = eval(response.text)['transcript']
    return transcript