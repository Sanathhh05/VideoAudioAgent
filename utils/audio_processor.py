
import yt_dlp 
from pydub import AudioSegment 
import os

download_directory = "downloads"
os.makedirs(download_directory, exist_ok=True)

def download_audio_from_youtube(url:str) -> str:
    output_path = os.path.join(download_directory, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    return audio_file_path



def convert_audio_to_wav(input_file:str) -> str:
    """Convert an audio/video file to WAV format using pydub."""
    output_path=os.path.split(input_file)[0]+"_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio=audio.set_channels(1).set_frame_rate(16000)  # Convert to mono and set frame rate to 16kHz for better compatibility with speech recognition models 
    
    audio.export(output_path, format='wav')
    return output_path



def chunk_audio(wav_path:str, chunk_mins:int=10)->list:
    audio=AudioSegment.from_wav(wav_path)
    chunk_length_ms=chunk_mins*60*1000
    
    chunks=[]
    for i,start in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk=audio[start:start+chunk_length_ms]
        chunk_path=f"{wav_path}_chunk{i}.wav"
        chunk.export(chunk_path, format='wav')
        chunks.append(chunk_path)
    return chunks

def process_input(source:str)->list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube URL. Downloading audio...")
        audio_path=download_audio_from_youtube(source)
        print("Converting to WAV format...")
        wav_path=convert_audio_to_wav(audio_path)
    else:
        print("Detected local file. Processing audio(Converting to wav)...")
        wav_path=convert_audio_to_wav(source)
    
    print("Chunking audio")   
    chunk_paths=chunk_audio(wav_path)
    print(f"Audio ready -{len(chunk_paths)} chunks created.")
    
    return chunk_paths