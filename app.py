import io
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
import warnings

warnings.filterwarnings("ignore")

# Import your existing core modules
from utils.audio_processor import process_input
from core.transcriber import transcribe_all, format_transcript
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

# Load environment variables
load_dotenv()

# Define the pipeline function with Streamlit status updates
def run_pipeline(source: str, language: str = "english") -> dict:
    with st.status("🚀 Processing AI Video Assistant Pipeline...", expanded=True) as status:
        st.write("Extracting and processing audio chunks...")
        chunks = process_input(source)

        #st.write("Transcribing audio...")
        #segments=transcribe_all(chunks, language)
        #transcript = transcribe_all(chunks, language)
        #timestamped_transcript = #format_transcript(segments)
        #plain_transcript = " ".join(
        #    seg["text"] for seg in segments
        #)
        
        st.write("Transcribing audio...")

        transcript = transcribe_all(chunks,  language)

        if isinstance(transcript, list):
            # English (Whisper)
            timestamped_transcript = format_transcript(transcript)

            plain_transcript = " ".join(
                seg["text"] for seg in transcript
            )
        else:
            # Hinglish (Sarvam)
            plain_transcript = transcript
            timestamped_transcript = transcript
        
        st.write("Generating title and summary...")
        title = generate_title(plain_transcript)
        summary = summarize(plain_transcript)

        st.write("Extracting key insights (Action Items, Decisions, Questions)...")
        action_item = extract_action_items(plain_transcript)
        decisions = extract_key_decisions(plain_transcript)
        questions = extract_questions(plain_transcript)
        
        st.write("Building RAG Knowledge Base...")
        rag_chain = build_rag_chain(plain_transcript)
        
        status.update(label="✅ Processing Complete!", state="complete", expanded=False)

    #return {
        #"title": title,
        #"transcript": transcript,
        #"summary": summary,
        #"action_items": action_item,
        #"key_decisions": decisions,
        #"open_questions": questions,
        #"rag_chain": rag_chain,
    #}#
    
    return {
        "title": title,
        "transcript": plain_transcript,
        "timestamped_transcript": timestamped_transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="AI Video Assistant", page_icon="🎬", layout="wide")

st.title("🎬 AI Video & Meeting Assistant")
st.markdown("Extract summaries, action items, and chat with your meeting transcripts.")

# --- Session State Initialization ---
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Configuration")
    source_input = st.text_input("Enter YouTube URL or Local File Path:")
    language_input = st.selectbox("Language:", ["english", "hinglish"])
    
    if st.button("Analyze Video", type="primary"):
        if source_input.strip():
            # Clear previous session data when running a new video
            st.session_state.processed_data = None
            st.session_state.chat_history = []
            
            # Run the pipeline and save to session state
            result = run_pipeline(source_input.strip(), language_input)
            st.session_state.processed_data = result
        else:
            st.warning("Please enter a valid URL or file path.")

# --- Main Display Area ---
if st.session_state.processed_data:
    data = st.session_state.processed_data
    
    # Display Title
    st.header(f"📌 {data['title']}")
    st.divider()
    
    # Use tabs for a clean UI layout
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Summary", 
        "✅ Action Items", 
        "🔑 Key Decisions", 
        "❓ Open Questions", 
        "📝 Full Transcript",
        "🕐 Timestamped Script"
    ])
    
    with tab1:
        st.write(data['summary'])

        # --- PDF Download Button ---
        def generate_summary_pdf(title: str, summary_text: str) -> bytes:
            pdf = FPDF()
            pdf.add_page()
            # Use a Unicode-capable TTF font (Arial from Windows system fonts)
            font_path = r"C:\Windows\Fonts\arial.ttf"
            font_path_bold = r"C:\Windows\Fonts\arialbd.ttf"
            pdf.add_font("Arial", "", font_path)
            pdf.add_font("Arial", "B", font_path_bold)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, title, ln=True, align="C")
            pdf.ln(6)
            pdf.set_font("Arial", "", 12)
            # multi_cell handles automatic line wrapping
            pdf.multi_cell(0, 7, summary_text)
            return bytes(pdf.output())

        pdf_bytes = generate_summary_pdf(data['title'], data['summary'])

        def on_download_click():
            print("pdf downloaded successfully")

        st.download_button(
            label="⬇️ Download Summary as PDF",
            data=pdf_bytes,
            file_name="summary.pdf",
            mime="application/pdf",
            on_click=on_download_click,
        )
    with tab2:
        st.write(data['action_items'])
    with tab3:
        st.write(data['key_decisions'])
    with tab4:
        st.write(data['open_questions'])
    with tab5:
        with st.container(height=400): # Scrollable container for long transcripts
            st.write(data['transcript'])
    with tab6:
        with st.container(height=400):
            st.text(data["timestamped_transcript"])
    st.divider()

    # --- Phase 2: RAG Chat UI ---
    st.subheader("💬 Chat with your meeting")
    
    # Display previous chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    if user_question := st.chat_input("Ask a question about the meeting..."):
        # Add user message to state and display it
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(data['rag_chain'], user_question)
                st.markdown(answer)
        
        # Add assistant response to state
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    # Initial welcome screen before processing
    st.info("👈 Enter a YouTube URL or file path in the sidebar to get started.")