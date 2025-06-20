# app.py
import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Image Captioning with Voice")
st.title(" AI Image Captioning with Voice by Raj")

uploaded_file = st.file_uploader(" Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.info(" Generating caption...")

    # Device config
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Load model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    # Process image
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)

    st.success(f" Caption: {caption}")

    # Convert caption to speech
    tts = gTTS(text="This image looks like " + caption, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        st.audio(tmpfile.name, format="audio/mp3")
