from google.cloud import speech_v1p1beta1 as speech
import os
from groq import Groq

# client = Groq(
#     api_key= os.environ["GROQ_API_KEY"]
# )

client = Groq(
    api_key= "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"
)
def transcribe_audio(audio_bytes):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return None



# Function to transcribe audio using Whisper
def whisper_transcribe(audio_bytes):
    # Save the audio bytes to a temporary file
    temp_file = "temp_audio.wav"
    with open(temp_file, "wb") as f:
        f.write(audio_bytes)

    # Transcribe the audio file using Whisper
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