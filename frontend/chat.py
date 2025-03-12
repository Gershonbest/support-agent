import streamlit as st
import requests
import time
from audio_recorder_streamlit import audio_recorder
from page_ui import UI
from utils import whisper_transcribe

# Streamlit UI Setup
st.set_page_config(page_title="VeraCLEAR Skincare Chatbot", page_icon="💆", layout="wide")

st.markdown(UI, unsafe_allow_html= True)

# Title and Description
st.title("💆 VeraCLEAR Skincare Chatbot")
st.write("Ask me anything about skincare routines, products, and tips!")

# Sidebar for User Preferences
st.sidebar.header("User Preferences")
skin_type = st.sidebar.selectbox("Select your skin type:", ["Normal", "Oily", "Dry", "Combination", "Sensitive"])
api_url = st.sidebar.text_input("Enter API URL:", value="http://127.0.0.1:8000/chat")
thread_id = int(st.sidebar.text_input("Chat thread ID:", value=324))
clear_chat = st.sidebar.button("Clear Chat History")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear Chat History
if clear_chat:
    st.session_state["messages"] = []  # Clear the chat history
    st.success("Chat history cleared!")  # Provide feedback to the user

user_input = None

# Display Chat History
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Text or Voice)
input_method = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True)

if input_method == "Text":
    user_input = st.chat_input("Type your message here...")
else:
    st.write("Click the microphone to record your message:")
    audio = audio_recorder()
    print(audio)
    if audio:
        # Process audio input (e.g., convert to text using a speech-to-text API)
        user_input = whisper_transcribe(audio)  # Convert audio to text
        if user_input:
            st.write(f"You said: {user_input}")
        else:
            st.write("Sorry, I couldn't understand the audio.")
        # st.write(user_input)  # Placeholder for audio processing

# Handle User Input
if user_input:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Show loading spinner while waiting for bot response
    with st.spinner("Thinking..."):
        try:
            response = requests.post(api_url, json={"message": user_input, "thread_id": thread_id})
            if response.status_code == 200:
                bot_reply = response.json().get("response", "Sorry, I couldn't process your request.")
            else:
                bot_reply = f"Error: Unable to connect to the chatbot API. Status code: {response.status_code}"
        except Exception as e:
            bot_reply = f"Error: {str(e)}"

    # Display bot response in a streaming manner
    with st.chat_message("assistant"):
        response_container = st.empty()
        displayed_text = ""
        for char in bot_reply:
            displayed_text += char
            response_container.markdown(displayed_text)
            time.sleep(0.01)  # Simulate streaming effect

    # Store bot response
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})