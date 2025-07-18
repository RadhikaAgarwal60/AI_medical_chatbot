# voice_of_the_doctor.py

import os
import platform
import subprocess
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath="final.mp3"):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Autoplay based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            print("Unsupported OS for auto playback.")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
