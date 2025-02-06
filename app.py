import streamlit as st
import os
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from stt_file import get_transcript
from tts_file import split_hindi_text, get_audio_string, autoplay_audio 
from llm_file import get_chat_response, get_answer_status
from init import llm_model, chat_len_limit

from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
        AIMessage(content="नमस्ते, आप कैसे हैं।", response_metadata = {'role': 'Assistant'}),
        ]


initialize_session_state()

st.title("Voice-Based Conversational AI System 🤖")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()


for message in st.session_state.chat_history:
    with st.chat_message(message.response_metadata['role']):
        st.write(message.content)

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.wav"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = get_transcript(webm_file_path)
        if transcript:

            st.session_state.chat_history.append(HumanMessage(content = transcript, response_metadata = {'role': 'User'}))
            with st.chat_message("User"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.chat_history[-1].response_metadata['role'] != "Assistant":
    with st.chat_message("Assistant"):
        with st.spinner("Thinking🤔..."):
            chat_len = min(len(st.session_state.chat_history), chat_len_limit)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_dict = get_answer_status(llm_model, 
                        st.session_state.chat_history[-1].content, 
                        st.session_state.chat_history[(-1) * chat_len:], current_time)
            print(status_dict)
            final_response, reference_urls, image_urls, relevancy_scores = get_chat_response(llm_model, status_dict, 
                        st.session_state.chat_history[-1].content, 
                        st.session_state.chat_history[(-1) * chat_len:], current_time)
            
        with st.spinner("Generating audio response..."): 
            text_list = split_hindi_text(final_response)   
            audio_string = get_audio_string(text_list)
            autoplay_audio(audio_string)
        st.write(final_response)
        st.session_state.chat_history.append(AIMessage(content = final_response, response_metadata = {'role': 'Assistant'}))


# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")