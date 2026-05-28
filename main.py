from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import format_transcript, transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question
import warnings, os, logging

warnings.filterwarnings("ignore")
# Suppress transformers logs
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
logging.getLogger("transformers").setLevel(logging.ERROR)

load_dotenv()

def run_pipeline(source :str, language :str = "english") -> dict:
    print("starting AI Video Assistant")

    chunks = process_input(source)

    #transcript = transcribe_all(chunks,language)
    #print(f"raw transcription (first 300 characters ) {transcript[:300]}")

    #segments = transcribe_all(chunks, language)

    #timestamped_transcript = format_transcript(segments)

    #plain_transcript = " ".join(
    #    seg["text"] for seg in segments
    #)
    
    transcript = transcribe_all(chunks, language)

    if isinstance(transcript, list):
        timestamped_transcript = format_transcript(transcript)

        plain_transcript = " ".join(
        seg["text"] for seg in transcript
        )
    else:
        plain_transcript = transcript
        timestamped_transcript = transcript
    
    print(f"raw transcription (first 300 chars): {plain_transcript[:300]}")

    title = generate_title(plain_transcript)

    summary = summarize(plain_transcript)

    action_item = extract_action_items(plain_transcript)

    decisions = extract_key_decisions(plain_transcript)
    questions = extract_questions(plain_transcript)

    rag_chain = build_rag_chain(plain_transcript)

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

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")