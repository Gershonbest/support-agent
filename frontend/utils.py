import os
from groq import Groq

# from src.utils.env_setup import _set_env
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from config.env_config import envs

client = Groq(api_key=envs.GROQ_API_KEY)
el_client = ElevenLabs(
    api_key=envs.ELEVEN_LAB_API_KEY,
)

# Function to transcribe audio using Whisper
def whisper_transcribe(audio_bytes):
    
    if not audio_bytes:
        raise ValueError("Error: Received empty audio data.")
    temp_file = "temp_audio.wav"
    #
    with open(temp_file, "wb") as f:
        f.write(audio_bytes)
    
    if not os.path.exists(temp_file):
        raise FileNotFoundError(f"Error: File {temp_file} was not created.")
    #
    with open(temp_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(temp_file, file.read()),
            model="whisper-large-v3",
            response_format="json",
            language="en",
            temperature=0.0,
        )

    # Clean up the temporary file
    os.remove(temp_file)

    return transcription.text


def text2speech(text):
    audio_stream = el_client.text_to_speech.convert_as_stream(
        text=text, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2"
    )

    stream(audio_stream)
