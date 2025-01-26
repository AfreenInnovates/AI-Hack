import streamlit as st
import google.generativeai as gen_ai
from PIL import Image
import os
from gtts import gTTS
import base64
import re
from datetime import datetime

# Configure Gemini API
gen_ai.configure(api_key="")
gemini = gen_ai.GenerativeModel("gemini-1.5-flash")

def upload_image_to_gemini(image_path):
    uploaded_file = gen_ai.upload_file(path=image_path, display_name=os.path.basename(image_path))
    return uploaded_file

def strip_markdown(text):
    """Removes Markdown syntax."""
    text = re.sub(r"[*_~]", "", text)
    return text

def text_to_speech(text, autoplay=True):
    """Generates an audio player from text."""
    plain_text = strip_markdown(text)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file_path = f"audio_{timestamp}.mp3"
    
    tts = gTTS(text=plain_text, lang='en')
    tts.save(audio_file_path)
    
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    st.markdown(f"""
        <audio autoplay="{str(autoplay).lower()}" controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)
    os.remove(audio_file_path)

# Add custom CSS to style the landing page and navbar
st.markdown("""
    <style>
        body {
            background-color: #f4f7f6;
            font-family: 'Arial', sans-serif;
        }

        .navbar {
            background-color: #004d40;
            padding: 10px 20px;
            text-align: center;
            font-size: 18px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .navbar a {
            color: white;
            text-decoration: none;
            margin: 10px;
            padding: 8px 15px;
            border-radius: 5px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .navbar a:hover {
            background-color: #004d40;
            transform: scale(1.05);
        }

        .landing-page {
            text-align: center;
            padding: 50px;
            color: #004d40;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }

        .landing-page h1 {
            font-size: 40px;
            color: #004d40;
            margin-bottom: 20px;
        }

        .landing-page p {
            font-size: 18px;
            color: #555;
            margin-bottom: 30px;
        }

        .stButton button {
            background-color: #004d40;
            color: white;
            font-size: 16px;
            padding: 12px 20px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s, transform 0.2s ease;
        }

        .stButton button:hover {
            background-color: #00796b;
            transform: scale(1.05);
        }

        .stTextInput input {
            border: 2px solid #004d40;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }

        .stTextInput input:focus {
            border-color: #00796b;
        }

        .stFileUploader input[type="file"] {
            padding: 10px;
            background-color: #ffffff;
            border: 2px solid #004d40;
            border-radius: 5px;
        }

        .stImage {
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
        }
    </style>
""", unsafe_allow_html=True)

# Create a navigation menu
page = st.sidebar.selectbox("Select a Page", ["Landing Page", "Upload Image"])

if page == "Landing Page":
    # Landing Page content
    st.markdown("<div class='landing-page'>", unsafe_allow_html=True)
    st.title("Welcome to Gemini Pro")
    st.image("https://via.placeholder.com/800x400.png?text=Gemini+Pro+Landing+Page", use_column_width=True)
    st.markdown("<p>Discover the power of image analysis and chat with an AI assistant!</p>", unsafe_allow_html=True)
    
    # Add a button to navigate to the Upload Image page
    if st.button("Get Started"):
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Upload Image":
    # Upload Image Page content
    st.title("📸 Gemini Pro - Image ChatBot")

    # Initialize session states
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = gemini.start_chat(history=[])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "image_description_done" not in st.session_state:
        st.session_state.image_description_done = False
    if "image_description_audio_played" not in st.session_state:
        st.session_state.image_description_audio_played = False

    st.subheader("Choose Image Input Method")
    input_method = st.radio("Select how you want to provide an image:", ("Upload Image", "Capture Image"))

    uploaded_image, captured_image, image_path = None, None, None
    if input_method == "Upload Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            temp_path = f"temp_uploaded_image.{uploaded_image.name.split('.')[-1]}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            image_path = temp_path
    elif input_method == "Capture Image":
        captured_image = st.camera_input("Capture an image using your camera")
        if captured_image:
            image_path = "temp_captured_image.png"
            with open(image_path, "wb") as f:
                f.write(captured_image.getbuffer())

    if image_path:
        image = Image.open(image_path)
        st.image(image, caption="Uploaded/Captured Image", use_column_width=True)

        st.subheader("Uploading the Image to Gemini")
        with st.spinner("Analyzing the image..."):
            gemini_file = gen_ai.upload_file(path=image_path, display_name=os.path.basename(image_path))
        st.success(f"Image uploaded successfully!")

        if not st.session_state.image_description_done:
            st.subheader("Gemini Describes the Image")
            with st.spinner("Generating a description..."):
                description_response = gemini.generate_content([gemini_file, "What is in the image?"])
            description_text = description_response.text
            st.session_state.chat_history.append(("assistant", description_text))
            st.session_state.image_description_done = True
            st.markdown(description_text)

        if st.session_state.image_description_done and not st.session_state.image_description_audio_played:
            st.session_state.image_description_audio_played = True

        st.subheader("Chat about the Image")
        for i, (role, message) in enumerate(st.session_state.chat_history):
            with st.chat_message(role):
                st.markdown(message)
                if role == "assistant" and i == len(st.session_state.chat_history) - 1:
                    text_to_speech(message, autoplay=False)

        user_prompt = st.chat_input("Ask Gemini-Pro about the image...")
        if user_prompt:
            st.session_state.chat_history.append(("user", user_prompt))
            st.chat_message("user").markdown(user_prompt)

            prompt_to_gemini = f"This is the user's prompt: {user_prompt}. Make sure to answer only related to the image or things related to it. Do not go off topic."

            gemini_response = st.session_state.chat_session.send_message([gemini_file, prompt_to_gemini])
            response_text = gemini_response.text
            st.session_state.chat_history.append(("assistant", response_text))
            with st.chat_message("assistant"):
                st.markdown(response_text)
                text_to_speech(response_text, autoplay=True)
    else:
        st.info("Please select and provide an image to proceed.")

    if image_path:
        os.remove(image_path)
