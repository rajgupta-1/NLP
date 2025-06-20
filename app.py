# app.py
import streamlit as st
import requests
from PIL import Image
from gtts import gTTS
import tempfile

# Hugging Face model endpoint
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
API_TOKEN = "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"  # Your actual token here
headers = {"Authorization": f"Bearer {API_TOKEN}"}

st.set_page_config(page_title="AI Image Captioning Raj")
st.title("📷 AI Image Captioning with Voice Raj")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    image_bytes = uploaded_file.read()

    st.info("🧠 Generating caption... please wait")
    response = requests.post(API_URL, headers=headers, files={"file": image_bytes})

    if response.status_code == 200:
        result = response.json()
        caption = result[0]["generated_text"]

        st.success(f"📝 Caption: {caption}")

        # Text-to-speech with gTTS
        tts = gTTS(text="This image looks like " + caption, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")
    else:
        st.error(f"❌ Failed to generate caption. Error: {response.status_code}")
        st.json(response.json())  # Show error message for debugging
