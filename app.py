import streamlit as st
from deep_translator import GoogleTranslator

# Streamlit app title
st.title("Receipt Translator Demo")

# Input box for text
user_text = st.text_input("Enter text to translate:", "안녕하세요")

# Translate when user provides text
if user_text:
    translator = GoogleTranslator(source='auto', target='en')
    translated_text = translator.translate(user_text)
    st.write("Translated text:")
    st.success(translated_text)
