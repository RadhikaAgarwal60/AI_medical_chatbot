# Imports
import os
import logging
from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr
from groq import Groq

# ✅ Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Inject ffmpeg into PATH
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
print("FFmpeg will be used from:", os.environ["PATH"])

# ✅ Audio recording function
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"Recording error: {e}")

# ✅ Speech to text function
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    if not audio_filepath or not os.path.exists(audio_filepath):
        raise FileNotFoundError(f"Audio file '{audio_filepath}' not found!")

    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return None

# ✅ Main process
if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"
    
    # 🔊 Step 1: Record audio
    record_audio(file_path=audio_filepath)

    # 🧠 Step 2: Transcribe audio
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    stt_model = "whisper-large-v3"

    if GROQ_API_KEY:
        result = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
        if result:
            print("🔈 Transcription Result:")
            print(result)
        else:
            print("❌ Transcription failed.")
    else:
        print("❌ GROQ_API_KEY not found in environment.")
