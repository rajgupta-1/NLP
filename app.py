# app.py
import streamlit as st
import requests
from PIL import Image
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Image Captioning (Lite)")
st.title("📷 AI Image Captioning with Voice")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Convert to bytes
    image_bytes = uploaded_file.read()

    # Call Hugging Face Inference API
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"}  # <-- Put your key here

    st.info("Generating caption... please wait")
    response = requests.post(API_URL, headers=headers, files={"file": image_bytes})

    if response.status_code == 200:
        result = response.json()
        caption = result[0]["generated_text"]
        st.success(f"📝 Caption: {caption}")

        # Voice with gTTS
        tts = gTTS(text="This image looks like " + caption, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")
    else:
        st.error("Failed to generate caption. Please try again later.")
