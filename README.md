# Technical Report: Voice-Based Conversational AI System 🎤🤖

---
### Demo Video & Technical Report
- **Demo Video**: [View the demo here](<https://drive.google.com/file/d/1pQnedSg8YhANvEjzGR3mgGbmqrdYHTE2/view?usp=sharing>)  
  *Watch a quick walkthrough demonstrating audio recording, STT, LLM responses, and TTS playback.*  
- **Technical Report**: [Download the full report (PDF)](<https://docs.google.com/document/d/1rzgdXc0Y07AROs84Ayw45I-sYUPF0x3GUUJ8cIo-b_U/edit?usp=sharing>)  
  *Contains detailed architecture diagrams, technology stack justifications, and future enhancements.*
---

## 1. Introduction 🌟
This project implements a **Conversational AI System** that enables **voice-based interaction in Hindi**. The system encompasses several key modules to deliver a robust conversational experience:
- **Speech-to-Text (STT)**: Converts Hindi speech into text. 🎙️➡️📝  
- **Language Model (LLM)**: Generates intelligent, context-aware responses in Hindi. 🧠💬  
- **Text-to-Speech (TTS)**: Converts AI-generated text back into spoken Hindi. 📝➡️🎧  
- **Avatar Animation (Planned)**: Future scope to integrate a talking avatar with lip-sync. 🎭👄  
- **Web Interface**: A Streamlit-based UI for user interaction. 🌐🖥️  
- **Scalability Considerations**: Ensures efficient handling of concurrent users and minimal latency. ⚙️📈  

By leveraging **Sarvam AI** for STT/TTS and **Google Gemini** (through LangChain) for LLM functionality, this system aims to provide a natural, real-time, and Hindi-focused conversational experience. It also employs the **Tavily web search API** for real-time knowledge enhancement, making the chatbot more reliable and informative. 🔍📚

---

## 2. Technologies Used & Justifications 🛠️
| **Component**                 | **Technology Used**              | **Justification**                                                                       |
|-------------------------------|-----------------------------------|-----------------------------------------------------------------------------------------|
| **Speech-to-Text (STT)**      | Sarvam AI STT                    | Accurate Hindi speech recognition, optimized for Indian accents and dialects. 🇮🇳🎙️        |
| **LLM (Language Model)**      | Google Gemini 2.0 via LangChain  | Fluent, context-aware responses in Hindi; integrates easily with prompt chaining. 🔗💡       |
| **Text-to-Speech (TTS)**      | Sarvam AI Bulbul v1              | Natural, high-quality Hindi voice output with adjustable pitch, speed, and loudness. 🔊🎶 |
| **Frontend & Backend**         | Streamlit + streamlit-float      | Rapid UI prototyping; built-in widgets like audio recorder. Lightweight and efficient for handling multiple concurrent requests. 🐍⚡                 |
| **Environment Config**        | dotenv                            | Securely manages API keys without exposing them in code. 🔒🔑                             |
| **Audio Processing**          | Pydub, Base64 Encoding           | Streamlines merging and splitting audio files. 🎧✂️                                      |
| **Web Search**                | Tavily Search API                | Provides real-time factual data and updates. 🌐📰                                        |

The chosen technologies prioritize **accuracy, scalability, and ease of development**, ensuring the system can handle real-time Hindi voice interactions while maintaining a clean and modular codebase. 🧩🚀

---
## 3. Quick Start guide 🖥️🔧
### 3.1. Clone the Repository
1. Open your terminal/command prompt.
2. Navigate to the directory where you want to keep the project.
3. Run:  
   ```bash
   git clone <REPO_URL>
   cd <REPO_DIRECTORY>
   ```

### 3.2. Create and Populate Your `.env` File
1. In the root directory of the cloned repo, create a file named `.env`.
2. Add your required API keys (Sarvam AI, Tavily, Google Gemini, etc.) in key-value pairs. For example:
   ```dotenv
   SARVAM_API_KEY=<your_sarvam_key>
   TAVILY_API_KEY=<your_tavily_key>
   GOOGLE_API_KEY=<your_google_key>
   ```
3. **Note**: Make sure not to commit this file to any public repository.

### 3.3. Install Dependencies
1. Make sure you have Python 3.7+ installed.
2. Install pip dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Optional**: For an isolated environment, you can create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

### 3.4. Run the Streamlit App
1. From the project’s root directory, run the following:
   ```bash
   streamlit run app.py
   ```
2. Your default browser should open to a local URL (e.g., `http://localhost:8501`) showing the Streamlit UI.
---
## 4. Technical Implementation 🖥️🔧

### 4.1 System Architecture 🏗️
#### Frontend Layer (Streamlit) 🌐
- Floating microphone button for voice recording. 🎤  
- Displays conversation in a chat-style interface. 💬  
- Plays TTS-generated audio automatically for a seamless voice response experience. 🔊  

#### Processing Pipeline ⚙️
- **Audio Recording → STT → LLM Processing → TTS → Audio Playback** 🔄  
- Session State in Streamlit tracks the conversation context across multiple turns. 📂  

#### Data Flow & Management 📊
- Base64-encoded audio for transmission and local playback. 📦  
- JSON-formatted responses from the LLM for structured data handling. 📄  
- Error Handling with fallback logic (e.g., if STT or TTS APIs fail). 🚨  

By separating each functionality (STT, LLM, TTS), the system maintains a **modular architecture**. This design supports easy swapping of APIs or models. 🔄🔧

---

### 4.2 Speech-to-Text (STT) 🎙️➡️📝
**File:** `stt_file.py`  
**API Used:** Sarvam AI Speech-to-Text  

#### Process:
1. **Audio Capture**: Records `.wav` audio in Streamlit. 🎤  
2. **Transcription Request**: Sends the audio file to the Sarvam AI endpoint. 📤  
3. **Response**: Returns Hindi text transcription; includes timestamps if required. ⏱️  

#### Optimizations:
- **Accent Support**: Specifically tuned for Indian accents. 🇮🇳  
- **Multiple Features**: Timestamps, diarization, and partial transcripts for real-time use cases. 🎯  

---

### 4.3 Language Model (LLM) – AI Response Generation 🧠💬
**File:** `llm_file.py`  
**API Used:** Google Gemini 2.0 via LangChain  

#### Process:
1. **Input**: Receives Hindi transcript from STT. 📝  
2. **Status Check**: Determines whether the question can be answered directly or if an external search is required. 🔍  
3. **Direct Answer**: If the LLM has sufficient context, it returns a final Hindi response. 💡  
4. **Web Search Fallback**: If the LLM lacks real-time data, the system reformats the user query, calls Tavily API, and incorporates relevant search results to generate a final response. 🌐  

#### Key Features:
- **Context-Aware**: Maintains conversation history for multi-turn dialogues. 🔄  
- **Hindi-Centric**: Enforces Hindi script usage, including numbers and formatting. 🇮🇳  
- **Control Over Creativity**: Temperature set to maintain a professional and clear tone. 🎚️  

---

### 4.4 Tavily API – Real-Time Knowledge Enhancement 🌐📰
**File:** `llm_file.py` (integrated)  
**API Used:** Tavily Search API  

#### Purpose:
- **Real-Time** or up-to-date information retrieval for queries involving current events, recent news, or factual data. 📅  

#### How It Works:
1. **Unknown or Current Queries**: The LLM decides to offload the query to Tavily. 🤔  
2. **Search**: Tavily fetches relevant web articles and resources. 🔍  
3. **Data Integration**: The LLM reads the extracted content and synthesizes an accurate Hindi answer. 📝  

#### Key Benefits:
- **Reduces Hallucinations** by integrating verifiable sources. 🚫🤯  
- **Real-Time Retrieval** for the latest stock prices, news, or events. 📈📰  

**Example:**  
- **User asks**: “टीसीएस का आज का शेयर मूल्य क्या है?”  
- **Without Tavily**: LLM might say: “I don’t have current market data.”  
- **With Tavily**: LLM returns: “आज टीसीएस का शेयर मूल्य लगभग चार हज़ार एक सौ पचास रुपए है (स्रोत: एनएसई इंडिया)।” 💹

---

### 4.5 Text-to-Speech (TTS) 📝➡️🎧
**File:** `tts_file.py`  
**API Used:** Sarvam AI Bulbul v1  

#### Process:
1. **Text Input**: Receives the Hindi response from LLM. 📝  
2. **Text Splitting**: Large texts split into smaller segments to avoid API limits. ✂️  
3. **Speech Synthesis**: Transformed into natural Hindi voice with user-defined pitch, pace, and loudness. 🔊  
4. **Audio Merging**: Segments combined using Pydub to produce a single, fluid audio track. 🎧  

#### Optimizations:
- **Base64 Encoding**: Ensures efficient audio streaming and quick playback in the browser. 📦  
- **Adaptive Splitting**: Prevents abrupt voice cut-offs and ensures smooth flow. 🎶  

---

### 4.6 Web Interface 🌐🖥️
**File:** `app.py` (primary code)  
**Framework:** Streamlit  

#### Features:
- **Recording**: `audio_recorder_streamlit` captures user input. 🎤  
- **Chat Interface**: Displays user queries and LLM responses in a conversation flow. 💬  
- **Floating UI Elements**: Via `streamlit-float`, ensuring a clean user experience. 🎨  
- **Audio Playback**: Autoplay TTS output upon receiving the final answer. 🔊  

#### Why Streamlit?
- **Rapid Prototyping**: Minimal code to get a fully interactive web interface. 🚀  
- **Native Audio Components**: Simplifies capturing and playing audio directly in the browser. 🎧  

---

## 5. Challenges & Solutions 🚧🛠️
| **Challenge**                                 | **Solution**                                                                 |
|-----------------------------------------------|-------------------------------------------------------------------------------|
| Long Text Processing in TTS                   | Implemented smart text splitting to break down large responses. ✂️           |
| Latency with Multiple APIs (STT/LLM/TTS)       | Optimized by limiting conversation history and using spinners for async UI. ⏳ |
| Maintaining Consistent Hindi Output           | Enforced Hindi script usage and validated text splitting. 🇮🇳                  |
| User Experience & UI Fluidity                 | Employed floating UI elements and asynchronous spinners. 🎨🌀                  |
| Security of API Keys                          | Used `.env` with `dotenv` to avoid hardcoding credentials. 🔒                  |

---

## 6. Scalability Considerations 📈⚙️
| **Aspect**          | **Optimization Implemented**                                                         |
|---------------------|---------------------------------------------------------------------------------------|
| API Management      | Stored keys in environment variables; supports easy change or upgrade. 🔑             |
| Performance         | Minimal data storage in session state; merges done in-memory with Pydub. 💾           |
| Concurrent Sessions | Streamlit can handle multiple users in parallel. 🧑‍🤝‍🧑                                 |
| Modular Design      | Each module (STT, TTS, LLM) is loosely coupled; can be independently replaced. 🔄      |
| Caching             | Could be added (e.g., Redis) to store repeated queries. 🗄️                             |
