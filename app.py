import os
import requests
import replicate
from playsound import playsound
import streamlit as st
import tempfile
from openai import OpenAI  # Ensure the OpenAI library is installed

# Initialize OpenAI client
client = OpenAI(
    api_key="sk-86780e6b88ab4d1d91c3c2229303a79b",  # Replace with your API key
    base_url="https://api.deepseek.com"
)
SYSTEME_PROMPT = """ 
You are a female  character with a dark persona.
You are intellingent, resourceful, and  have a sharp wit.
you demeanor is often cold , and you  are  not afraid to be  blunt or rude
You are polite and nice
You speak with confidence , and your words ca be cutting.
You background is mysterious , and  you have a deep  knowledge of technology.
You a are here to share you knowledge , whether people like it not.
Keep your answers very short and pricise.

"""

# Define the say function
def say(text):
    input = {
        "text": text,
        "speed": 1.1,
        "voice": "af_bella"
    }

    try:
        # Run the Replicate TTS model
        output_url = replicate.run(
            "jaaari/kokoro-82m:dfdf537ba482b029e0a761699e6f55e9162cfd159270bfe0e44857caa5f275a6",
            input=input
        )

        # Download the audio from the URL
        response = requests.get(output_url, stream=True)
        response.raise_for_status()

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            for chunk in response.iter_content(chunk_size=1024):
                temp_audio.write(chunk)
            audio = temp_audio.name

        # Play the audio
        playsound(audio)

    except Exception as e:
        print(f"Error generating or playing audio: {e}")

# Streamlit App
st.title("Agent Chat with Voice")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant"}]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=False
        )
        assistant_message = response.choices[0].message.content
        st.markdown(assistant_message)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Play the response as audio
        say(assistant_message)
