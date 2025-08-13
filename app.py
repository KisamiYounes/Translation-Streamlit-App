import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
import streamlit.components.v1 as components

# Language codes dictionary
language = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "arabic": "ar",
    "chinese": "zh",
    "japanese": "ja",
    "russian": "ru",
    "portuguese": "pt"
}

translator = Translator()

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="centered")

st.title("🌐 Language Translation Tool")
st.write("Translate text between multiple languages instantly.")

text = st.text_area("Enter text to translate:")

# Detect language only if there's text
detected_lang_code = ""
detected_lang_name = ""
if text.strip():
    detected_lang_code = translator.detect(text).lang
    detected_lang_name = next((lang for lang, code in language.items() if code == detected_lang_code), "Unknown")
    st.info(f"Detected source language: **{detected_lang_name}** ({detected_lang_code})")

target_lang = st.selectbox("Select target language:", list(language.keys()))

# Store translation result in session state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            translated = translator.translate(
                text, 
                src=detected_lang_code,
                dest=language[target_lang]
            )
            st.session_state.translated_text = translated.text
            st.success(f"**Translated Text:** {translated.text}")

        except Exception as e:
            st.error(f"Translation failed: {e}")

# Text-to-speech button (independent)
if st.button("Convert to Speech"):
    if not st.session_state.translated_text:
        st.warning("Please translate text first.")
    else:
        try:
            tts = gTTS(text=st.session_state.translated_text, lang=language[target_lang])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                st.audio(tmp_file.name, format="audio/mp3")
            st.success("Text-to-speech conversion successful!")
        except Exception as e:
            st.error(f"Text-to-speech conversion failed: {e}")

# Show supported languages
st.write("### Supported Languages:")
for lang in language.keys():
    st.write(f" - {lang}")

st.write("---")
st.caption("Built for CodeAlpha AI Internship 🚀")
