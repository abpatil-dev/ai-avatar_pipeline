import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

tavily_url = "https://api.tavily.com/search"
sarvam_stt_url = "https://api.sarvam.ai/speech-to-text"
sarvam_tts_url = "https://api.sarvam.ai/text-to-speech"

genai.configure(api_key = GOOGLE_API_KEY)
llm_model = ChatGoogleGenerativeAI(model = 'gemini-2.0-flash-thinking-exp-01-21', temperature = 0.1)
chat_len_limit = 10