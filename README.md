# AI Video & Meeting Assistant

![Architecture Diagram](file:///C:/Users/Sanath/.gemini/antigravity/brain/c5152766-424e-417b-9147-28cfd7f1d2a7/architecture_diagram_1779684254006.png)

## Overview

This project is a **Streamlit‑based AI Video Assistant** that extracts audio from YouTube videos (or local video files), transcribes the content, generates a concise summary and title, extracts actionable insights (action items, key decisions, open questions), and provides an interactive RAG‑powered chat interface to query the meeting transcript.

Built with modern Python libraries, the application showcases end‑to‑end AI pipelines, from audio processing to large‑language‑model (LLM) summarisation and Retrieval‑Augmented Generation (RAG).

## Features

- **Audio extraction & chunking** – Handles long videos by splitting audio into manageable chunks.
- **Automatic transcription** – Uses Whisper‑based transcription for multilingual support.
- **Smart summarisation & title generation** – Provides high‑level overview of the meeting.
- **Insight extraction** – Detects action items, key decisions, and unanswered questions.
- **RAG knowledge base** – Indexes the transcript for accurate question‑answering.
- **Downloadable PDF summary** – One‑click export of the title and summary.
- **Interactive chat** – Ask follow‑up questions about the meeting transcript.
- **Responsive UI** – Streamlit tabs and status indicators for a smooth user experience.

## Architecture

The system consists of several modular components:

- `app.py` – Streamlit UI and pipeline orchestration.  
- `utils/audio_processor.py` – Downloads video/audio and splits it into uniform 30‑second chunks.  
- `core/transcriber.py` – Wraps Whisper transcription for each chunk.  
- `core/summarize.py` – Generates a title and summary using LLM prompts.  
- `core/extractor.py` – Pulls out action items, decisions, and questions.  
- `core/rag_engine.py` – Builds a vector store (e.g., FAISS) and defines the RAG chain for Q&A.  
- `vector_db/` – Stores the persisted embeddings for the transcript.  
- `downloads/` – Holds original and chunked audio files.  

The architecture diagram above visualises the data flow and module interactions.

##Images

<img width="1326" height="843" alt="Screenshot 2026-05-26 123324" src="https://github.com/user-attachments/assets/bb73073a-8a59-4cad-8a7a-fae162751a59" />
<img width="1539" height="831" alt="Screenshot 2026-05-26 123308" src="https://github.com/user-attachments/assets/d7403154-182a-499a-bf05-cff552c06938" />
<img width="1420" height="810" alt="Screenshot 2026-05-26 123220" src="https://github.com/user-attachments/assets/a9da2119-1c55-4e30-a43d-4f9a3ec72f0a" />

## Installation

1. **Clone the repository**  
   ```bash
   git clone <repo-url>
   cd VideoAgent
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r Requirements.txt
   ```
4. **Configure environment variables**
   - Create a `.env` file at the project root.
   - Add your OpenAI API key and any other service credentials:
     ```
     OPENAI_API_KEY=your_openai_key_here
     ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

- Enter a YouTube URL or local file path in the sidebar.
- Choose the language (English or Hinglish).
- Click **Analyze Video** to start processing.
- Explore the generated tabs for summary, action items, decisions, questions, and full transcript.
- Use the chat box at the bottom to ask follow‑up questions about the meeting.

## Project Structure

```
VideoAgent/
├─ app.py                 # Streamlit UI & pipeline orchestration
├─ core/                  # Core AI processing modules
│   ├─ transcriber.py
│   ├─ summarize.py
│   ├─ extractor.py
│   └─ rag_engine.py
├─ utils/                 # Helper utilities
│   └─ audio_processor.py
├─ vector_db/             # Persisted embeddings for RAG
├─ downloads/             # Raw and chunked audio files
├─ Requirements.txt       # Python dependencies
├─ .env.example           # Example env file
└─ README.md              # Project documentation (this file)
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Ensure code passes linting (`ruff`) and unit tests.
4. Open a Pull Request with a clear description of changes.

## License

This project is licensed under the MIT License.
>>>>>>> 622cf01 (A1: updated files)
