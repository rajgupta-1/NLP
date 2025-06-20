
import streamlit as st
from PIL import Image
from gtts import gTTS
import tempfile
import random

st.title("🧠 AI Caption + Voice (Lite Version)")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Use mock captions (for demo)
mock_captions = [
    "A ripe tomato on a farm",
    "Wheat crop under sunlight",
    "A damaged leaf due to pests",
    "Healthy green cabbage plant",
    "Soil appears dry and cracked"
]

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)

    caption = random.choice(mock_captions)
    st.success(f"📝 Caption: {caption}")

    tts = gTTS(text=caption, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        audio_path = tmpfile.name
        tts.save(audio_path)
        st.audio(audio_path, format='audio/mp3')
