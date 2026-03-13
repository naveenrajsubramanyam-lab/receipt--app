import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import io

st.title("Receipt OCR + Translator + Excel Export")

# File uploader
uploaded_file = st.file_uploader("Upload receipt (image or PDF)", type=["jpg", "png", "pdf"])

if uploaded_file:
    text = ""

    # Handle PDF receipts
    if uploaded_file.type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

    # Handle image receipts
    else:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

    # Show original text
    st.subheader("Original Text")
    st.text(text)

    # Translate text
    translator = GoogleTranslator(source='auto', target='en')
    translated = translator.translate(text)

    st.subheader("Translated Text")
    st.success(translated)

    # Save to Excel
    df = pd.DataFrame({"Original": [text], "Translated": [translated]})
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Receipts")

    st.download_button(
        label="Download Excel",
        data=buffer.getvalue(),
        file_name="receipts.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
